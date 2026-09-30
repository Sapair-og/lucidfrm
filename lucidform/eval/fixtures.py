"""Build the offline extraction fixture corpus.

    python -m lucidform.eval.fixtures

**What this corpus is, and what it is not.** These are *expected* model
responses, derived from persona ground truth plus a table of hand-written
overrides for the interesting cases. They are not recordings of a real model.

That distinction decides what the offline suite can measure. Replaying against
this corpus exercises the whole pipeline deterministically -- intent handling,
grounding, gating, read-back, confirmation, commit, export -- and will catch a
regression in any of it. It cannot measure extraction accuracy, because the
expected values were written from the ground truth the accuracy would be
scored against. Offline accuracy against this corpus is 100% by construction
and is meaningless as a result.

Extraction accuracy is therefore a live-model measurement. The replay driver
takes either client, so the same sessions run both ways: offline for
correctness, live for the accuracy figure. Reporting the offline number as an
accuracy result would be circular, and METHODOLOGY M4.4 says so explicitly.

The overrides below are where the corpus earns its keep. They encode the
utterances that must *not* extract cleanly -- a question, a decline, a
homoglyph, a value outside an enum -- so that the pipeline's handling of each is
exercised offline, deterministically, on every test run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lucidform.eval.personas import Persona, load_all
from lucidform.extract.schema import Extraction, Intent
from lucidform.schema import loader

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "extractions.json"

# (persona_id, field_id, utterance_index) -> the extraction that utterance
# should produce. Anything not listed here is assumed to extract cleanly to the
# persona's ground truth with high confidence.
OVERRIDES: dict[tuple[str, str, int], dict[str, Any]] = {
    # p02 reads her PAN with a homoglyph: the letter O where the digit 0
    # belongs. The extractor should report exactly what it heard -- repairing it
    # here would hide the error from the gate and from the user.
    ("p02", "pan", 0): {
        "intent": "value",
        "value": "BFTPN82O6C",
        "quote": "B F T P N eight two O six C",
        "confidence": 0.88,
        "ambiguous": False,
    },
    # p03 asks what the field means before answering it. Extracting this as a
    # value would write the user's own question into the PAN field.
    ("p03", "pan", 0): {
        "intent": "question",
        "value": "",
        "quote": "",
        "confidence": 0.0,
        "ambiguous": False,
    },
    # An optional field explicitly declined. Recorded as a decision, not as an
    # empty value that failed validation.
    ("p03", "email", 0): {
        "intent": "decline",
        "value": "",
        "quote": "",
        "confidence": 0.0,
        "ambiguous": False,
    },
    # An exact figure where the form wants a band. The extractor reports what
    # was said; the gate rejects it as not an option and the user is re-asked
    # with the options read out. Mapping "three lakh" onto "1-5 Lakh" here
    # would be the model choosing on the user's behalf.
    ("p03", "income_band", 0): {
        "intent": "value",
        "value": "teen lakh",
        "quote": "teen lakh ke aas paas",
        "confidence": 0.45,
        "ambiguous": False,
    },
    # Free-text description of an occupation, not one of the permitted options.
    ("p03", "occupation", 0): {
        "intent": "value",
        "value": "apna kaam",
        "quote": "apna kaam karta hoon",
        "confidence": 0.4,
        "ambiguous": False,
    },
    # A valid value that is simply the wrong one. "Kollam" is a real city in
    # the same state as the persona's PIN code, so it passes every check the
    # gate performs, including the PIN/city directory check (ISSUES.md LF-003;
    # this was "Kolhapur", which that check now catches). Only the read-back
    # can catch it -- which is the entire argument for the read-back being a
    # pipeline stage rather than a courtesy.
    ("p02", "city", 0): {
        "intent": "value",
        "value": "Kollam",
        "quote": "kochi",
        "confidence": 0.71,
        "ambiguous": False,
    },
    # p01 gives his occupation in his own words on the first attempt.
    ("p01", "occupation", 0): {
        "intent": "value",
        "value": "shop owner",
        "quote": "i have my own shop",
        "confidence": 0.5,
        "ambiguous": False,
    },
    ("p01", "income_band", 0): {
        "intent": "value",
        "value": "7 lakh",
        "quote": "about seven lakh a year",
        "confidence": 0.5,
        "ambiguous": False,
    },
}


def _clean_extraction(persona: Persona, field_id: str, utterance: str) -> dict[str, Any]:
    """The straightforward case: the value was stated and heard correctly."""
    return {
        "intent": Intent.VALUE.value,
        "value": persona.truth(field_id),
        # The whole utterance is quoted. Real model output would usually quote a
        # narrower span; the grounding check only requires the quote to appear
        # in the utterance, so this is a valid -- if coarse -- grounding.
        "quote": utterance,
        "confidence": 0.94,
        "ambiguous": False,
        "alternatives": [],
    }


def build() -> dict[str, Any]:
    schema = loader.load()
    recordings: list[dict[str, Any]] = []

    for persona in load_all():
        for field in schema:
            for index, utterance in enumerate(persona.utterances(field.id)):
                override = OVERRIDES.get((persona.persona_id, field.id, index))
                extraction = (
                    {**{"alternatives": []}, **override}
                    if override
                    else _clean_extraction(persona, field.id, utterance)
                )
                # Validate on the way out, so a malformed override fails here
                # rather than at replay time.
                Extraction.model_validate(extraction)
                recordings.append(
                    {
                        "persona_id": persona.persona_id,
                        "field_id": field.id,
                        "utterance": utterance,
                        "attempt": index,
                        "extraction": extraction,
                    }
                )

    return {
        "note": (
            "Expected model responses, not recordings. Derived from persona "
            "ground truth plus hand-written overrides. Offline replay against "
            "this corpus verifies pipeline behaviour; it cannot measure "
            "extraction accuracy. See lucidform/eval/fixtures.py."
        ),
        "model": "expected",
        "recordings": recordings,
    }


def write(path: Path | None = None) -> Path:
    path = Path(path or FIXTURE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(build(), fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return path


if __name__ == "__main__":  # pragma: no cover
    written = write()
    print(f"wrote {written}")
