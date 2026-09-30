"""Form schema loading: parse the AcroForm, merge the semantic overlay.

Two sources, deliberately kept separate (METHODOLOGY M0.4):

  * the PDF's field dictionary -- names, widget types, max lengths, option
    lists. Machine-read, deterministic, no OCR.
  * `ckyc_form.yaml` -- what a field *means*, how to ask for it in plain
    language, and what makes a value valid. Human-authored, auditable.

The merge is strict on purpose. A field in the overlay with no matching PDF
widget, or a PDF widget with no overlay entry, raises rather than being skipped:
a silently dropped field is a field the gate never validates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pypdf import PdfReader

from lucidform.config import get_settings
from lucidform.models import FieldSpec, FieldType


class SchemaError(RuntimeError):
    """The parsed form and the overlay disagree. Always fatal."""


@dataclass(frozen=True)
class FormSchema:
    form_id: str
    version: int
    title: str
    fields: tuple[FieldSpec, ...]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self) -> int:
        return len(self.fields)

    def by_id(self, field_id: str) -> FieldSpec:
        for f in self.fields:
            if f.id == field_id:
                return f
        raise KeyError(field_id)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(f.id for f in self.fields)


def _inherited(obj: Any, key: str, depth: int = 8) -> Any:
    """Read a field attribute, following /Parent.

    AcroForm attributes are inheritable: a widget may omit /FT and take it from
    its parent field. Reading only the leaf silently mistypes such fields.
    """
    node = obj
    while node is not None and depth > 0:
        if key in node:
            return node[key]
        parent = node.get("/Parent")
        node = parent.get_object() if parent is not None else None
        depth -= 1
    return None


def parse_acroform(pdf_path: Path) -> dict[str, dict[str, Any]]:
    """Structure only. Returns {acroform_name: {widget, max_length, options}}.

    Reads the widget annotations on each page rather than pypdf's
    `get_fields()`. `get_fields()` collapses to the field level and does not
    surface `/MaxLen`, which lives on the widget -- so a parser built on it
    reports no length constraint for any field and quietly falls back to
    whatever the overlay asserts. Reading annotations keeps the PDF as the
    authority for the one constraint it genuinely carries.

    pypdf reports field *names*, not labels: labels are drawn text with no
    machine-readable link to the widget. That gap is what the overlay fills,
    and why this function returns so little.
    """
    reader = PdfReader(str(pdf_path))
    parsed: dict[str, dict[str, Any]] = {}

    for page in reader.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            name = obj.get("/T")
            if name is None:
                continue
            max_len = _inherited(obj, "/MaxLen")
            options = _inherited(obj, "/Opt")
            parsed[str(name)] = {
                "widget": _inherited(obj, "/FT"),
                "max_length": int(max_len) if max_len is not None else None,
                "options": tuple(str(o) for o in options) if options else (),
            }

    if not parsed:
        raise SchemaError(f"no AcroForm widget annotations found in {pdf_path}")
    return parsed


def load_overlay(path: Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load(
    pdf_path: Path | None = None,
    overlay_path: Path | None = None,
    *,
    strict: bool = True,
) -> FormSchema:
    settings = get_settings()
    pdf_path = Path(pdf_path or settings.form_pdf)
    overlay_path = Path(overlay_path or settings.schema_overlay)

    if not pdf_path.exists():
        raise SchemaError(
            f"{pdf_path} not found. Generate it with: "
            "python -m lucidform.schema.make_form"
        )

    parsed = parse_acroform(pdf_path)
    overlay = load_overlay(overlay_path)

    declared = {f["acroform_name"] for f in overlay["fields"]}
    if strict:
        missing = declared - parsed.keys()
        if missing:
            raise SchemaError(
                f"overlay declares fields absent from the PDF: {sorted(missing)}"
            )
        extra = parsed.keys() - declared
        if extra:
            raise SchemaError(
                f"PDF has widgets with no overlay entry, so nothing would "
                f"validate them: {sorted(extra)}"
            )

    fields: list[FieldSpec] = []
    for entry in overlay["fields"]:
        structure = parsed.get(entry["acroform_name"], {})
        ftype = FieldType(entry["type"])
        enum_values = tuple(entry.get("enum_values", ()))
        raw_names = entry.get("enum_names") or {}
        for option, names in raw_names.items():
            if not isinstance(names, list):
                # `Male: purush` would otherwise be iterated letter by letter,
                # declaring every single character a name for the option.
                raise SchemaError(f"{entry['id']}: enum_names for {option!r} must be a list")
        enum_names = {option: tuple(str(n) for n in names) for option, names in raw_names.items()}
        canonical = {v.casefold(): v for v in enum_values}
        for option, names in enum_names.items():
            for name in names:
                other = canonical.get(name.casefold())
                if other is not None and other != option:
                    raise SchemaError(
                        f"{entry['id']}: {name!r} declared for {option!r} is another option's value"
                    )
        unknown = set(enum_names) - set(enum_values)
        if unknown:
            raise SchemaError(f"{entry['id']}: enum_names for non-options {sorted(unknown)}")
        seen: dict[str, str] = {}
        for option, names in enum_names.items():
            for name in names:
                other = seen.setdefault(name.casefold(), option)
                if other != option:
                    # One spoken name for two options would make the gate choose.
                    raise SchemaError(
                        f"{entry['id']}: {name!r} is declared for both {other!r} and {option!r}"
                    )

        if strict and ftype is FieldType.ENUM:
            pdf_options = structure.get("options", ())
            if pdf_options and tuple(pdf_options) != enum_values:
                raise SchemaError(
                    f"{entry['id']}: PDF option list {pdf_options} disagrees "
                    f"with overlay enum_values {enum_values}"
                )

        fields.append(
            FieldSpec(
                id=entry["id"],
                acroform_name=entry["acroform_name"],
                label=entry["label"],
                type=ftype,
                required=entry.get("required", True),
                prompt=dict(entry.get("prompt", {})),
                gloss=dict(entry.get("gloss", {})),
                labels=dict(entry.get("labels", {})),
                # The PDF's own /MaxLen wins where present -- it is the
                # constraint the document actually enforces.
                max_length=structure.get("max_length") or entry.get("max_length"),
                pattern=entry.get("pattern"),
                enum_values=enum_values,
                enum_names=enum_names,
                depends_on=tuple(entry.get("depends_on", ())),
                decline_value=entry.get("decline_value"),
                decline_offer=dict(entry.get("decline_offer", {})),
            )
        )

    ids = [f.id for f in fields]
    if len(set(ids)) != len(ids):
        raise SchemaError("duplicate field ids in overlay")

    known = set(ids)
    for f in fields:
        unknown = set(f.depends_on) - known
        if unknown:
            raise SchemaError(f"{f.id}: depends_on unknown field(s) {sorted(unknown)}")

    return FormSchema(
        form_id=overlay["form_id"],
        version=int(overlay["version"]),
        title=overlay["title"],
        fields=tuple(fields),
    )
