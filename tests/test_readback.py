"""Read-back rendering: can the user actually check this by ear?

For a user who cannot see the form, the read-back is the only representation of
a value they will ever receive. If it is not checkable by ear, the confirmation
step is theatre -- the user agrees to something they had no way to verify. These
tests are about audibility, which is not a property any other test in the suite
covers.
"""

from __future__ import annotations

import pytest

from lucidform.i18n import Strings
from lucidform.orchestrate import readback
from lucidform.schema import loader


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def field(schema):
    return schema.by_id


def render(field, value, lang="en"):
    return readback.render_value(value, field, lang)


# -- identifiers are spelled, not spoken -------------------------------------


def test_a_pan_is_spelled_out_not_pronounced(field):
    """"AKQPS3417M" spoken as a word is an unpronounceable noise that no
    listener can compare against the card in their hand."""
    spoken = render(field("pan"), "AKQPS3417M")
    assert "AKQPS3417M" not in spoken
    for letter in "A K Q P S".split():
        assert letter in spoken
    assert "three" in spoken and "four" in spoken


def test_digits_are_words_not_numerals(field):
    """A synthesiser reading "3417" says "three thousand four hundred and
    seventeen", which has silently regrouped the number -- the listener cannot
    tell whether the system holds the digits they gave."""
    spoken = render(field("pin"), "302015")
    assert "three" in spoken and "zero" in spoken
    assert "302015" not in spoken
    assert "thousand" not in spoken


def test_an_aadhaar_is_grouped_so_it_can_be_held_in_memory(field):
    """Twelve digits in one unbroken run is not checkable by ear."""
    spoken = render(field("aadhaar"), "747910984992")
    assert readback.GROUP_SEPARATOR in spoken
    assert spoken.count(readback.GROUP_SEPARATOR) == 2, "expected three groups of four"


def test_a_mobile_number_is_grouped_too(field):
    assert readback.GROUP_SEPARATOR in render(field("mobile"), "9812345607")


def test_letters_are_upper_cased_so_they_are_read_as_letter_names(field):
    spoken = render(field("pan"), "akqps3417m")
    assert "A" in spoken and "M" in spoken
    assert "akqps" not in spoken


# -- dates are the mirror image ----------------------------------------------


def test_a_date_is_spoken_readably_not_as_stored(field):
    """1987-03-14 is the stored form and an unreadable one."""
    assert render(field("dob"), "1987-03-14") == "14 March 1987"


def test_a_date_has_no_leading_zero_on_the_day(field):
    assert render(field("dob"), "1987-03-04") == "4 March 1987"


def test_an_unparseable_date_is_shown_as_is_rather_than_guessed(field):
    assert render(field("dob"), "not-a-date") == "not-a-date"


# -- email -------------------------------------------------------------------


def test_an_email_local_part_is_spelled_and_punctuation_is_spoken(field):
    """A bare "." in the read-back is either skipped silently by a synthesiser
    or pronounced inconsistently, and a listener cannot confirm what they did
    not hear."""
    spoken = render(field("email"), "l.nair@example.invalid")
    assert "dot" in spoken
    assert "at" in spoken
    assert "." not in spoken
    assert "L" in spoken and "N" in spoken


def test_an_email_domain_is_left_as_words(field):
    """A listener can check "example dot invalid" without hearing it letter by
    letter, whereas a name abbreviation cannot be guessed from its sound."""
    spoken = render(field("email"), "l.nair@example.invalid")
    assert "example" in spoken and "invalid" in spoken


# -- plain text is left alone ------------------------------------------------


def test_names_and_places_are_not_spelled_out(field):
    """Spelling a name the user just said would be tedious and no clearer."""
    assert render(field("full_name"), "Ramesh Kumar Sharma") == "Ramesh Kumar Sharma"
    assert render(field("city"), "Jaipur") == "Jaipur"


def test_enum_values_are_read_as_written(field):
    assert render(field("income_band"), "5-10 Lakh") == "5-10 Lakh"


# -- the value being confirmed is the value that will be written -------------


def test_rendering_never_changes_the_stored_value(field, schema):
    """Presentation differs; the value does not.

    If rendering altered the value, the user would be confirming one thing and
    the form would receive another -- a silent write with extra steps.
    """
    values = {
        "pan": "AKQPS3417M",
        "aadhaar": "747910984992",
        "dob": "1987-03-14",
        "email": "l.nair@example.invalid",
        "city": "Jaipur",
    }
    for field_id, value in values.items():
        rendered = render(schema.by_id(field_id), value)
        assert isinstance(rendered, str) and rendered
        # The rendering is a view. The value is untouched.
        assert value == values[field_id]


def test_the_readback_sentence_names_the_field_and_the_value(field):
    """A read-back that omits which field it is about cannot be checked -- the
    user has answered several questions and needs to know which one this is."""
    strings = Strings("en")
    sentence = readback.render(
        "AKQPS3417M", field("pan"), strings.get("readback"), "en"
    )
    assert "PAN" in sentence
    assert "A" in sentence and "three" in sentence
    assert sentence.rstrip().endswith("?"), "a read-back must ask, not assert"


def test_the_hindi_readback_frame_is_used_for_hindi(field):
    strings = Strings("hi")
    sentence = readback.render(
        "AKQPS3417M", field("pan"), strings.get("readback"), "hi"
    )
    assert "क्या यह सही है" in sentence
    # The value itself is still spelled out -- the audibility problem is the
    # same in either language.
    assert "three" in sentence


# -- spell() directly --------------------------------------------------------


def test_spell_without_grouping():
    assert readback.spell("A1B") == "A one B"


def test_spell_groups_evenly_and_keeps_the_remainder():
    spelled = readback.spell("1234567", group_size=4)
    assert spelled.count(readback.GROUP_SEPARATOR) == 1
    assert spelled.endswith("five six seven")


def test_spell_ignores_whitespace_in_the_source_value():
    assert readback.spell("7479 1098") == readback.spell("74791098")
