"""Synthetic persona loading.

A persona is a fabricated user: ground-truth field values plus the utterances
they produce when asked for each field. The replay driver (Phase 5) uses them to
run the pipeline headlessly, which is what makes extraction accuracy measurable
-- accuracy is only defined against a known-correct answer.

Every persona is fictional. See METHODOLOGY M0.8.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import yaml

from lucidform.config import get_settings


class PersonaError(RuntimeError):
    """A persona is internally inconsistent. Always fatal.

    A persona whose ground truth is invalid would be scored against a wrong
    answer, quietly corrupting every accuracy figure derived from it.
    """


@dataclass(frozen=True)
class Persona:
    persona_id: str
    name: str
    lang: str
    profile: dict[str, str]
    ground_truth: dict[str, str]
    turns: dict[str, tuple[str, ...]]
    affirm: str
    deny: str
    source: Path

    def utterances(self, field_id: str) -> tuple[str, ...]:
        return self.turns.get(field_id, ())

    def truth(self, field_id: str) -> str:
        return self.ground_truth.get(field_id, "")

    def expects_skip(self, field_id: str) -> bool:
        """True when this persona has no value for an optional field."""
        return self.ground_truth.get(field_id, "") == ""


def load_persona(path: Path) -> Persona:
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    responses = raw.get("responses", {})
    turns = {
        field_id: tuple(str(u) for u in utterances)
        for field_id, utterances in (raw.get("turns") or {}).items()
    }

    persona = Persona(
        persona_id=raw["persona_id"],
        name=raw.get("name", raw["persona_id"]),
        lang=raw.get("lang", "en"),
        profile=dict(raw.get("profile", {})),
        ground_truth={k: ("" if v is None else str(v)) for k, v in raw["ground_truth"].items()},
        turns=turns,
        affirm=responses.get("affirm", "yes"),
        deny=responses.get("deny", "no"),
        source=path,
    )

    missing = set(persona.ground_truth) - set(persona.turns)
    speaking = {k for k in missing if persona.ground_truth[k] != ""}
    if speaking:
        raise PersonaError(
            f"{path.name}: ground truth for {sorted(speaking)} but no utterances -- "
            "the replay driver would have nothing to say when asked"
        )
    return persona


def load_all(directory: Path | None = None) -> list[Persona]:
    directory = Path(directory or get_settings().personas_dir)
    return [load_persona(p) for p in sorted(directory.glob("*.yaml"))]


def __iter__() -> Iterator[Persona]:  # pragma: no cover - convenience only
    return iter(load_all())
