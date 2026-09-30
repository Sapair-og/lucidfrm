"""Measure the help agent against the hand-written question set.

Four numbers, each answering a different question:

  * retrieval hit@k    -- did a passage that answers the question reach the model?
  * answer rate        -- how often an in-scope question got a cited answer
                          rather than the gloss fallback
  * gold citation rate -- of the cited answers, how many cite a gold passage
  * control refusal    -- of the out-of-corpus controls, how many were refused

Refusal on controls is reported beside the answer rate for the same reason gate
recall is reported beside its false-positive rate: an agent that answers
everything maximises one number by failing the other. Whether an answer's prose
is *correct* is not scored automatically -- the citations make it checkable by
a reader, and the transcript CSV exists for that review.
"""

from __future__ import annotations

import csv
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path

import yaml

from lucidform.help.answer import HelpAgent


_NUMBERED = re.compile(r"Q\d+$")


def gold_matches(gold: str, label: str) -> bool:
    """A numbered gold ("RBI KYC FAQ, Q1") must equal the label -- a substring
    test would also accept Q10-Q19. A phrase gold (a UIDAI question) may sit
    inside a longer label."""
    return label == gold if _NUMBERED.search(gold) else gold in label


@dataclass
class Row:
    qid: str
    kind: str  # "question" or "control"
    field: str
    lang: str
    question: str
    gold: list[str]
    retrieved: list[str]
    cited: list[str]
    source: str
    fallback_reason: str
    spoken: str
    latency_ms: float

    @property
    def hit(self) -> bool:
        return any(gold_matches(g, label) for g in self.gold for label in self.retrieved)

    @property
    def cited_gold(self) -> bool:
        return any(gold_matches(g, label) for g in self.gold for label in self.cited)

    @property
    def errored(self) -> bool:
        return self.fallback_reason.startswith("error")


def load_set(path: Path) -> list[dict]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    items = [dict(q, kind="question") for q in raw["questions"]]
    items += [dict(c, kind="control", gold=[]) for c in raw["controls"]]
    return items


def run(agent: HelpAgent, schema, items: list[dict], pause_s: float = 0.0) -> list[Row]:
    rows = []
    for item in items:
        field = schema.by_id(item["field"])
        started = time.perf_counter()
        answer = agent.answer(field, item["q"], item["lang"])
        elapsed = (time.perf_counter() - started) * 1000
        labels = [agent.index.get(cid).label for cid in answer.retrieved_ids]
        rows.append(
            Row(
                qid=item["id"],
                kind=item["kind"],
                field=item["field"],
                lang=item["lang"],
                question=item["q"],
                gold=list(item.get("gold", [])),
                retrieved=labels,
                cited=answer.cited_labels,
                source=answer.source,
                fallback_reason=answer.fallback_reason or "",
                spoken=answer.spoken,
                latency_ms=round(elapsed, 1),
            )
        )
        if pause_s:
            time.sleep(pause_s)
    return rows


def summarise(rows: list[Row]) -> dict:
    qs = [r for r in rows if r.kind == "question"]
    # A control that hit an API error was never asked; counting its fallback as
    # a refusal would report an outage as perfect behaviour.
    cs = [r for r in rows if r.kind == "control" and not r.errored]
    answered = [r for r in qs if r.source == "rag"]
    lat = sorted(r.latency_ms for r in rows)

    def pct(n, d):
        return round(100 * n / d, 1) if d else None

    return {
        "questions": len(qs),
        "controls": sum(r.kind == "control" for r in rows),
        "controls_scored": len(cs),
        "errors": sum(r.errored for r in rows),
        "retrieval_hit_at_k": pct(sum(r.hit for r in qs), len(qs)),
        "answer_rate": pct(len(answered), len(qs)),
        "gold_citation_rate": pct(sum(r.cited_gold for r in answered), len(answered)),
        "control_refusal_rate": pct(sum(r.source == "gloss" for r in cs), len(cs)),
        "fallbacks": {
            reason: sum(r.fallback_reason == reason for r in rows)
            for reason in sorted({r.fallback_reason for r in rows if r.fallback_reason})
        },
        "latency_ms_p50": lat[len(lat) // 2] if lat else None,
        "latency_ms_p95": lat[min(len(lat) - 1, int(0.95 * len(lat)))] if lat else None,
    }


def write(rows: list[Row], summary: dict, out_dir: Path, meta: dict) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows_path = out_dir / "help_eval.csv"
    with rows_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "kind", "field", "lang", "question", "hit", "cited_gold", "source",
                    "fallback_reason", "retrieved", "cited", "latency_ms", "spoken"])
        for r in rows:
            w.writerow([r.qid, r.kind, r.field, r.lang, r.question, r.hit, r.cited_gold, r.source,
                        r.fallback_reason, " | ".join(r.retrieved), " | ".join(r.cited),
                        r.latency_ms, r.spoken])
    summary_path = out_dir / "help_summary.json"
    summary_path.write_text(json.dumps({**meta, **summary}, indent=2, ensure_ascii=False), encoding="utf-8")
    return rows_path, summary_path
