"""The help agent's corpus: official KYC documents, chunked by their own structure.

Chunk boundaries follow the documents rather than a fixed token count: one FAQ
question with its answer, or one numbered paragraph of the Master Direction.
A structural chunk is something a citation can point at ("RBI KYC FAQ, Q10"),
which is what lets a user -- or a reviewer -- check the answer against its
source. Long legal paragraphs are windowed, keeping their label.

Every source file is pinned by SHA-256 in `manifest.json`; the corpus is part of
the evaluation, and a silently edited source would be a different corpus.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

MAX_CHARS = 1400
MIN_ANSWER_CHARS = 20


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    label: str
    url: str
    text: str

    def to_json(self) -> dict:
        return asdict(self)


def _clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    return text.strip()


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _html_text(raw: str) -> str:
    body = re.sub(r"(?is)<(script|style|noscript).*?</\1>", "", raw)
    body = re.sub(r"(?i)<br\s*/?>|</(p|tr|td|div|li|h\d|dt|dd)>", "\n", body)
    return _clean(html.unescape(re.sub(r"<[^>]+>", "", body)))


def _pdf_text(path: Path) -> str:
    from pypdf import PdfReader

    return _clean("\n".join(page.extract_text() or "" for page in PdfReader(path).pages))


def _window(text: str, limit: int = MAX_CHARS) -> list[str]:
    """Split on sentence boundaries into pieces of at most ~limit characters."""
    text = _flat(text)
    if len(text) <= limit:
        return [text]
    pieces, current = [], ""
    for sentence in re.split(r"(?<=[.;:])\s+", text):
        if current and len(current) + len(sentence) + 1 > limit:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
        while len(current) > limit:  # a single sentence longer than the window
            pieces.append(current[:limit])
            current = current[limit:]
    if current:
        pieces.append(current)
    return pieces


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


# -- per-source chunkers ------------------------------------------------------------


def _rbi_faq(text: str):
    parts = re.split(r"(?=\bQ\s*\d+\.\s)", text)
    for part in parts:
        m = re.match(r"Q\s*(\d+)\.\s", part)
        if m:
            yield f"RBI KYC FAQ, Q{m.group(1)}", part


def _pan_faq(text: str):
    section = ""
    for block in re.split(r"(?m)^(?=## )", text):
        header = re.match(r"## (?:[A-Z]: )?Form No\. (\d+)", block)
        if header:
            section = f" (Form {header.group(1)})"
        elif block.startswith("## "):
            section = ""
        for m in re.finditer(r"(?ms)^(\d+)\. (.+?)(?=^\d+\. |\Z)", block):
            yield f"Income Tax PAN FAQ{section}, Q{m.group(1)}", m.group(0)


def _question_lines(text: str, title: str):
    """FAQ pages where a question is a line ending in '?' followed by its answer."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    question, answer = None, []

    def emit():
        body = " ".join(answer)
        if question and len(body) >= MIN_ANSWER_CHARS:
            return (f"{title}: {question}", f"{question}\n{body}")
        return None

    for line in lines:
        if line.endswith("?") and 15 <= len(line) <= 250:
            done = emit()
            if done:
                yield done
            question, answer = line, []
        elif question:
            answer.append(line)
    done = emit()
    if done:
        yield done


def _master_direction(text: str):
    start = text.find("1INTRODUCTION")
    text = text[start:] if start >= 0 else text
    # Top-level paragraphs are "N. " at the start of a line; footnote markers
    # glued to words ("1INTRODUCTION") are not.
    parts = re.split(r"(?m)^(?=\d{1,3}\.\s)", text)
    for part in parts:
        m = re.match(r"(\d{1,3})\.\s", part)
        label = f"RBI KYC Master Direction, para {m.group(1)}" if m else "RBI KYC Master Direction, introduction"
        yield label, part


def _cersai(text: str):
    parts = re.split(r"(?m)^\s*(?=(?:[IVX]+|[A-H])\.\s+[A-Z])", text)
    for part in parts:
        m = re.match(r"([IVX]+|[A-H])\.\s+([^\n]{0,60})", part)
        head = f"{m.group(1)}. {m.group(2).strip()}" if m else "preamble"
        yield f"CERSAI CKYC Operating Guidelines, {head}", part


CHUNKERS = {
    "rbi_kyc_faq_2025.pdf": ("pdf", _rbi_faq),
    "rbi_kyc_master_direction.html": ("html", _master_direction),
    "incometax_pan_faq.md": ("md", _pan_faq),
    "uidai_faq_update.md": ("md", lambda t: _question_lines(t, "UIDAI Aadhaar Update FAQ")),
    "uidai_faq_enrolment.html": ("html", lambda t: _question_lines(t, "UIDAI Aadhaar Enrolment FAQ")),
    "cersai_ckyc_guidelines_2016.pdf": ("pdf", _cersai),
}


def _read(path: Path, kind: str) -> str:
    if kind == "pdf":
        return _pdf_text(path)
    raw = path.read_text(encoding="utf-8", errors="ignore")
    return _html_text(raw) if kind == "html" else _clean(raw)


def load_manifest(sources: Path) -> list[dict]:
    return json.loads((Path(sources) / "manifest.json").read_text(encoding="utf-8-sig"))


def load_chunks(sources: Path) -> list[Chunk]:
    sources = Path(sources)
    chunks: list[Chunk] = []
    for entry in load_manifest(sources):
        name = entry["file"]
        kind, chunker = CHUNKERS[name]
        text = _read(sources / name, kind)
        seen: dict[str, int] = {}
        for label, body in chunker(text):
            for piece in _window(body):
                if len(piece) < MIN_ANSWER_CHARS:
                    continue
                n = seen.get(label, 0)
                seen[label] = n + 1
                slug = _slug(label)[:80]
                digest = hashlib.sha1(piece.encode("utf-8")).hexdigest()[:8]
                chunk_id = f"{slug}-{n}-{digest}" if n else f"{slug}-{digest}"
                chunks.append(Chunk(chunk_id, name, label, entry["url"], piece))
    return chunks
