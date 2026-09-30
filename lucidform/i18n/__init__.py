"""String table loading.

Keys are looked up strictly. A missing key raises rather than falling back to
another language, because a silent fallback surfaces to the user as the
assistant switching language mid-sentence -- which for someone who cannot read
the screen is indistinguishable from the system malfunctioning.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

STRINGS_DIR = Path(__file__).resolve().parent
DEFAULT_LANG = "en"


class MissingString(KeyError):
    """A string key is absent from the requested language's table."""


@lru_cache
def load(lang: str = DEFAULT_LANG) -> dict[str, str]:
    path = STRINGS_DIR / f"strings_{lang}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"no string table for language {lang!r}; expected {path}"
        )
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def available() -> tuple[str, ...]:
    return tuple(
        sorted(p.stem.removeprefix("strings_") for p in STRINGS_DIR.glob("strings_*.yaml"))
    )


class Strings:
    """The system's own wording, in one language."""

    def __init__(self, lang: str = DEFAULT_LANG) -> None:
        self.lang = lang
        self._table = load(lang)

    def __contains__(self, key: object) -> bool:
        return key in self._table

    def get(self, key: str) -> str:
        try:
            return self._table[key].strip()
        except KeyError as exc:
            raise MissingString(
                f"{key!r} is missing from strings_{self.lang}.yaml"
            ) from exc

    def say(self, key: str, **kw: object) -> str:
        """Look up a key and fill in its placeholders."""
        template = self.get(key)
        try:
            return template.format(**kw)
        except KeyError as exc:
            raise MissingString(
                f"strings_{self.lang}.yaml key {key!r} needs placeholder {exc}"
            ) from exc
