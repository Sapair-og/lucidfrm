"""Use a PDF the user brings, instead of the built-in forms (ISSUES.md LF-014).

Three cases, decided from the file itself:

  * **The official CKYC form** (same print as the bundled AMFI copy): the full
    official flow, written onto the user's own copy.
  * **A fillable PDF** (it has AcroForm fields): the fields are read from the
    file. A field recognised by its name, tooltip or printed label (name, PAN,
    Aadhaar, PIN, mobile...) takes that field's human-written prompt and rules
    from the template overlay, so it is validated exactly like the built-in
    form. Anything else is asked by its printed label, as plain text, and may
    be skipped -- nothing is invented about what it must contain.
  * **A flat or scanned PDF**: there is nothing to say where a value goes
    without OCR and layout analysis, which is not built. Refused with a reason.

Recognition is keyword matching, not a model: a mis-recognised field would get
the wrong rules, and the rules are the safety claim. When unsure, a field stays
generic text.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from lucidform.config import get_settings
from lucidform.schema.loader import FormSchema, SchemaError, _build, _inherited, load_overlay

OFFICIAL_TITLE = "Know Your Customer (KYC) Application Form"

# template field id -> pattern over "name tooltip label", normalised. Order
# matters: the first pattern that matches wins, and each id is used once.
KNOWN: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (fid, re.compile(p))
    for fid, p in (
        ("father_name", r"\b(father|spouse|husband)"),
        ("dob", r"\b(dob|date of birth|birth ?date|d o b)\b"),
        ("pan", r"\bpan\b"),
        ("aadhaar", r"\b(aadhaa?r|adhaa?r|uid)\b"),
        ("mobile", r"\b(mobile|phone|cell|contact (no|number))\b"),
        ("email", r"\be ?mail\b"),
        ("pin", r"\b(pin ?code|pin|postal ?code|zip ?code|zip)\b"),
        ("gender", r"\b(gender|sex)\b"),
        ("city", r"\b(city|town)\b"),
        ("state", r"\bstate\b"),
        ("occupation", r"\b(occupation|profession)\b"),
        ("address_line", r"\baddress\b"),
        # Last, and only a bare "name": first/middle/last or someone else's
        # name must not be given full-name semantics.
        ("full_name", r"^(full |applicant s |applicant |your |customer )?name( of (the )?applicant)?$"),
    )
)
_OTHER_PERSON = re.compile(r"\b(mother|nominee|guardian|bank|branch|company|employer|first|middle|last|sur)\b")


@dataclass(frozen=True)
class CustomForm:
    kind: str  # "official" | "acroform"
    schema: FormSchema
    pdf: Path
    skipped: tuple[str, ...] = ()  # fields found but not asked (tick boxes, signatures)
    note: str = ""


def _norm(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text or "")  # camelCase -> words
    text = re.sub(r"[^a-z0-9]+", " ", text.casefold())
    return " ".join(text.split())


def _slug(text: str, taken: set[str]) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", (text or "field").casefold()).strip("_")[:40] or "field"
    base = f"f_{base}" if base[0].isdigit() else base
    slug, n = base, 2
    while slug in taken:
        slug, n = f"{base}_{n}", n + 1
    return slug


def _texts(page) -> list[tuple[str, float, float]]:
    out: list[tuple[str, float, float]] = []

    def visit(text, cm, tm, font, size):
        t = text.strip()
        if t:
            out.append((t, tm[4] * cm[0] + cm[4], tm[5] * cm[3] + cm[5]))

    try:
        page.extract_text(visitor_text=visit)
    except Exception:  # noqa: BLE001 - a label is a nicety; the name is the fallback
        pass
    return out


def _label(rect, texts) -> str:
    """The printed text just left of the box on its line, else just above it."""
    x0, y0, x1, y1 = rect
    mid = (y0 + y1) / 2
    left = [(x, t) for t, x, y in texts if x < x0 - 1 and abs(y - mid) <= max(6, (y1 - y0) / 2 + 3)]
    if left:
        return max(left)[1]
    above = [(y - y1, t) for t, x, y in texts if 0 <= y - y1 <= 16 and x0 - 20 <= x <= x1]
    return min(above)[1] if above else ""


def _clean(label: str) -> str:
    label = re.sub(r"[:*_.\s]+$", "", label.strip())
    return label[:60]


def _widgets(reader: PdfReader) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for page in reader.pages:
        texts = None
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            name = _inherited(obj, "/T")
            if name is None or str(name) in found:
                continue
            if texts is None:
                texts = _texts(page)
            rect = [float(v) for v in obj.get("/Rect", [0, 0, 0, 0])]
            max_len = _inherited(obj, "/MaxLen")
            options = _inherited(obj, "/Opt")
            found[str(name)] = {
                "name": str(name),
                "ft": str(_inherited(obj, "/FT") or ""),
                "tooltip": str(_inherited(obj, "/TU") or ""),
                "label": _clean(_label(rect, texts)),
                "max_length": int(max_len) if max_len is not None else None,
                "options": tuple(
                    str(o[1] if isinstance(o, list) and len(o) > 1 else o) for o in options
                ) if options else (),
            }
    return list(found.values())


def _same_file(a: Path, b: Path) -> bool:
    return b.exists() and hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()


def _is_official(reader: PdfReader, path: Path) -> bool:
    if _same_file(path, get_settings().official_pdf):
        return True
    try:
        first = reader.pages[0].extract_text() or ""
    except Exception:  # noqa: BLE001
        return False
    return OFFICIAL_TITLE in first and len(reader.pages) == 4


def open_form(path: str | Path) -> CustomForm:
    """Read a user's PDF and build a schema for it, or raise SchemaError saying why not."""
    path = Path(str(path).strip().strip('"').strip("'")).expanduser()
    if not path.exists():
        raise SchemaError(f"no file at {path}")
    if path.suffix.casefold() != ".pdf":
        raise SchemaError(f"{path.name} is not a PDF")
    try:
        reader = PdfReader(str(path))
    except Exception as exc:  # noqa: BLE001
        raise SchemaError(f"could not open {path.name} as a PDF ({type(exc).__name__})") from exc
    if reader.is_encrypted:
        raise SchemaError(f"{path.name} is password-protected")

    if _is_official(reader, path):
        from lucidform.schema.loader import load_official

        same = _same_file(path, get_settings().official_pdf)
        return CustomForm(
            kind="official",
            schema=load_official(),
            pdf=path if same else get_settings().official_pdf,
            note="" if same else (
                "This looks like the official CKYC form but a different print of it, "
                "so it is filled on the built-in copy, whose box positions are measured."
            ),
        )

    widgets = _widgets(reader)
    if not widgets:
        raise SchemaError(
            f"{path.name} has no fillable fields. Filling a flat or scanned form needs "
            "OCR and layout detection, which is not built yet."
        )

    template = {f["id"]: f for f in load_overlay(get_settings().schema_overlay)["fields"]}
    entries: list[dict[str, Any]] = []
    parsed: dict[str, dict[str, Any]] = {}
    used: set[str] = set()
    skipped: list[str] = []

    for w in widgets:
        shown = w["label"] or w["tooltip"] or w["name"]
        if w["ft"] in ("/Btn", "/Sig"):
            # Tick boxes and signatures: not asked in this version.
            skipped.append(shown)
            continue
        parsed[w["name"]] = {"widget": w["ft"], "max_length": w["max_length"], "options": w["options"]}
        haystack = " | ".join(_norm(t) for t in (w["name"], w["tooltip"], w["label"]) if t)
        match = None
        if not _OTHER_PERSON.search(haystack):
            for fid, pattern in KNOWN:
                if fid not in used and any(pattern.search(part) for part in haystack.split(" | ")):
                    match = fid
                    break

        if match:
            used.add(match)
            entry = {k: v for k, v in template[match].items() if k not in ("max_length", "depends_on")}
            entry["acroform_name"] = w["name"]
            if w["options"]:
                # The PDF's own choices are the options; the template's spoken
                # names may not correspond to them, so they are not carried over.
                entry["enum_values"] = list(w["options"])
                entry["type"] = "enum"
                for key in ("enum_names", "suggest_names", "amount_bands"):
                    entry.pop(key, None)
                # The template's question names the template's options; ask
                # with this PDF's own choices instead.
                choices = ", ".join(w["options"])
                entry["prompt"] = {
                    "en": f"What is your {entry['label'].lower()}? Choose one of: {choices}.",
                    "hi": f"{entry.get('labels', {}).get('hi', entry['label'])} क्या है? इनमें से चुनें: {choices}।",
                }
            entries.append(entry)
            continue

        label = shown.strip() or w["name"]
        taken = {e["id"] for e in entries} | set(template)
        is_date = re.search(r"\bdate\b", _norm(label + " " + w["name"])) is not None
        entry = {
            "id": _slug(label, taken),
            "acroform_name": w["name"],
            "label": label,
            "type": "enum" if w["options"] else ("date" if is_date else "text"),
            # Nothing says whether an unrecognised box is required; the user
            # may skip it rather than be trapped by a guess.
            "required": False,
            "prompt": {
                "en": f'What should I write for "{label}"?',
                "hi": f'"{label}" में क्या लिखूँ?',
            },
            "gloss": {
                "en": f'This is the box labelled "{label}" on your form. Say what should be written there, or say skip.',
                "hi": f'यह आपके फॉर्म पर "{label}" वाला खाना है। उसमें क्या लिखना है बताएँ, या छोड़ें कहें।',
            },
            "aliases": [_norm(label)] if _norm(label) else [],
        }
        if w["options"]:
            entry["enum_values"] = list(w["options"])
        if re.search(r"\b(expiry|valid (till|upto|until))\b", _norm(label)):
            entry["date_future"] = True
        entries.append(entry)

    if not entries:
        raise SchemaError(
            f"{path.name} only has tick boxes or signature fields, which are not supported yet."
        )

    # Cross-field rules refer to template ids; keep only references that exist.
    ids = {e["id"] for e in entries}
    for e in entries:
        e["depends_on"] = [d for d in e.get("depends_on", []) if d in ids]
    overlay = {
        "form_id": f"custom_{_slug(path.stem, set())}",
        "version": 1,
        "title": path.stem,
        "fields": entries,
    }
    return CustomForm(
        kind="acroform",
        schema=_build(overlay, parsed, strict=False),
        pdf=path,
        skipped=tuple(skipped),
    )
