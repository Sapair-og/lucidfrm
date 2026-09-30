"""Settings. Model id is config, never hardcoded -- the extraction-accuracy
sweep across model tiers depends on being able to swap it from the environment.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_prefix="LUCIDFORM_",
        extra="ignore",
    )

    # Read without the LUCIDFORM_ prefix -- they are the SDKs' own variable names.
    # The alias is what makes that true: env_prefix applies to every field
    # otherwise, and a key set in .env would be silently ignored.
    anthropic_api_key: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")
    gemini_api_key: str = Field(
        default="", validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY")
    )

    # Which client the extractor talks to. Model ids per provider are config so
    # the accuracy sweep across tiers is an environment change, not a code change.
    extraction_provider: str = "gemini"
    extraction_model: str = "claude-opus-5-5"
    gemini_model: str = "gemini-3.5-flash-lite"

    # Help agent: retrieval embeddings and the model that phrases the answer.
    embedding_model: str = "gemini-embedding-001"
    help_model: str = "gemini-3.5-flash-lite"
    lang: str = "en"

    # Below this, the gate rejects as LOW_CONFIDENCE rather than passing a value
    # the extractor was unsure of. Tuned against the false-positive rate, not
    # guessed -- see METHODOLOGY M0.7.
    min_confidence: float = 0.55

    data_dir: Path = REPO_ROOT / "data"

    @property
    def form_pdf(self) -> Path:
        return self.data_dir / "forms" / "ckyc_individual.pdf"

    @property
    def personas_dir(self) -> Path:
        return self.data_dir / "personas"

    @property
    def runs_dir(self) -> Path:
        return self.data_dir / "runs"

    @property
    def results_dir(self) -> Path:
        return self.data_dir / "results"

    @property
    def schema_overlay(self) -> Path:
        return Path(__file__).resolve().parent / "schema" / "ckyc_form.yaml"


@lru_cache
def get_settings() -> Settings:
    return Settings()
