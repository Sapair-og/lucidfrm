"""String tables.

A missing key must fail loudly. Falling back to another language surfaces to the
user as the assistant switching language mid-sentence, which for someone who
cannot read the screen is indistinguishable from the system malfunctioning --
and is far harder to notice in testing than an exception.
"""

from __future__ import annotations

import pytest

from lucidform import i18n
from lucidform.i18n import MissingString, Strings

LANGS = ("en", "hi")


def test_both_languages_are_available():
    assert set(LANGS).issubset(set(i18n.available()))


@pytest.mark.parametrize("lang", LANGS)
def test_every_language_has_the_same_keys(lang):
    """A key present in one table and absent from another is a runtime failure
    waiting for the first user who selects that language."""
    english = set(i18n.load("en"))
    assert set(i18n.load(lang)) == english


@pytest.mark.parametrize("lang", LANGS)
def test_no_string_is_empty(lang):
    for key, text in i18n.load(lang).items():
        assert text and text.strip(), f"{lang}: {key} is empty"


@pytest.mark.parametrize("lang", LANGS)
def test_placeholders_match_across_languages(lang):
    """A translation that drops a placeholder raises at format time; one that
    invents a placeholder raises too. Both are caught here instead.

    Compared as sorted multisets, not sequences: Hindi puts the total before
    the count where English does the reverse, and that is correct translation
    rather than an error. Only the set of placeholders is fixed; their order is
    the translator's to choose.
    """
    import re

    pattern = re.compile(r"\{(\w+)\}")
    english = i18n.load("en")
    table = i18n.load(lang)
    for key, text in english.items():
        assert sorted(pattern.findall(text)) == sorted(pattern.findall(table[key])), (
            f"{lang}: placeholders in {key!r} do not match English"
        )


def test_a_missing_key_raises_rather_than_falling_back():
    strings = Strings("en")
    with pytest.raises(MissingString, match="no_such_key"):
        strings.get("no_such_key")


def test_a_missing_placeholder_raises_with_the_key_named():
    strings = Strings("en")
    with pytest.raises(MissingString, match="readback"):
        strings.say("readback", label="PAN")  # value= omitted


def test_an_unknown_language_fails_with_a_useful_message():
    with pytest.raises(FileNotFoundError, match="no string table"):
        i18n.load("xx")


@pytest.mark.parametrize("lang", LANGS)
def test_the_greeting_explains_the_confirmation_step(lang):
    """The user has to know a value is not saved until they say so; otherwise
    the read-back sounds like narration rather than a question they must answer.
    """
    greeting = Strings(lang).get("greeting")
    assert len(greeting) > 80
    marker = "correct" if lang == "en" else "सही"
    assert marker in greeting


@pytest.mark.parametrize("lang", LANGS)
def test_every_schema_field_has_a_prompt_and_gloss_in_this_language(lang):
    """Field wording lives in the schema overlay, not the string table -- but
    the completeness requirement is the same, so it is checked the same way."""
    from lucidform.schema import loader

    for field in loader.load():
        assert field.prompt.get(lang), f"{field.id}: no {lang} prompt"
        assert field.gloss.get(lang), f"{field.id}: no {lang} gloss"


def test_hindi_strings_are_actually_devanagari():
    """Guards against a table copied from English and left untranslated."""
    table = i18n.load("hi")
    for key, text in table.items():
        assert any("ऀ" <= ch <= "ॿ" for ch in text), (
            f"hi: {key!r} contains no Devanagari -- is it still English?"
        )


@pytest.mark.parametrize("lang", LANGS)
def test_every_field_has_a_spoken_label_in_this_language(lang):
    """The read-back names the field, so an English label inside a Hindi
    read-back is the one place a language slip actually costs something: it
    appears in the sentence the user is asked to attest to."""
    from lucidform.schema import loader

    for field in loader.load():
        spoken = field.name(lang)
        assert spoken, f"{field.id}: no spoken label for {lang}"
        if lang == "hi":
            assert any("ऀ" <= ch <= "ॿ" for ch in spoken), (
                f"{field.id}: spoken Hindi label {spoken!r} is still English"
            )


def test_the_canonical_label_stays_english_for_the_pdf_and_logs():
    """`label` is the identifier used in the document and the results table;
    only what the user hears is translated."""
    from lucidform.schema import loader

    pan = loader.load().by_id("pan")
    assert pan.label == "PAN"
    assert pan.name("en") == "PAN"
    assert pan.name("hi") != pan.label
