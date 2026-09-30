"""Normalization and single-field rules.

The adversarial suite checks verdicts. These check the machinery underneath,
and in particular the property that normalization *reshapes but never repairs*.
A normalizer that quietly fixed a value would commit something the user never
said, which is the same failure as a silent write with extra steps.
"""

from __future__ import annotations

import datetime as dt

import pytest

from lucidform.gate import rules
from lucidform.models import FieldType
from lucidform.schema import loader


@pytest.fixture(scope="module")
def schema():
    return loader.load()


@pytest.fixture(scope="module")
def field(schema):
    return schema.by_id


# -- normalization: reshaping ------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("akqps3417m", "AKQPS3417M"),
        ("AKQPS 3417 M", "AKQPS3417M"),
        ("AKQPS-3417-M", "AKQPS3417M"),
        ("  AKQPS3417M  ", "AKQPS3417M"),
    ],
)
def test_pan_separators_and_case_are_reshaped(field, raw, expected):
    assert rules.normalize(raw, field("pan")) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("+91 98123 45607", "9812345607"),
        ("09812345607", "9812345607"),
        ("919812345607", "9812345607"),
        ("98123-45607", "9812345607"),
    ],
)
def test_phone_country_and_trunk_prefixes_are_stripped(field, raw, expected):
    """Reshaping: the subscriber number is unchanged, only the prefix goes."""
    assert rules.normalize(raw, field("mobile")) == expected


def test_phone_prefix_stripping_does_not_eat_real_digits(field):
    """A ten-digit number starting 9 must not lose its leading 9 as a "91".

    The prefix rule only fires when removing it leaves exactly ten digits, so
    a genuine 91-prefixed subscriber number survives.
    """
    assert rules.normalize("9112345607", field("mobile")) == "9112345607"


def test_enum_matching_is_case_and_space_insensitive_only(field):
    """Case folding is reshaping. Picking the nearest option is not.

    "shopkeeper" is a reasonable answer whose nearest option is "Business" --
    choosing it for the user would be the system deciding on their behalf, so
    the value is left alone for the enum check to reject.
    """
    occupation = field("occupation")
    assert rules.normalize("business", occupation) == "Business"
    assert rules.normalize("  BUSINESS  ", occupation) == "Business"
    assert rules.normalize("shopkeeper", occupation) == "shopkeeper"


def test_dates_normalize_to_iso_from_every_accepted_form(field):
    dob = field("dob")
    for raw in ("1987-03-14", "14/03/1987", "14-03-1987", "14.03.1987", "14 March 1987"):
        assert rules.normalize(raw, dob) == "1987-03-14", raw


def test_ambiguous_dates_resolve_day_first(field):
    """Indian convention. 03/04/1987 is 3 April, not 4 March."""
    assert rules.normalize("03/04/1987", field("dob")) == "1987-04-03"


def test_unparseable_dates_are_returned_unchanged(field):
    """So the format check can report what the user actually said."""
    assert rules.normalize("1987-13-45", field("dob")) == "1987-13-45"


def test_whitespace_is_collapsed_not_stripped_out(field):
    assert rules.normalize("  Ramesh   Kumar  Sharma ", field("full_name")) == (
        "Ramesh Kumar Sharma"
    )


# -- normalization: what it must NOT do --------------------------------------


def test_normalization_never_repairs_a_bad_checksum(field):
    bad = "747910984993"
    assert rules.normalize(bad, field("aadhaar")) == bad


def test_normalization_never_transliterates_devanagari_digits(field):
    """The user said a number; the system cannot be sure which one it heard.

    Converting them would commit a value derived by guesswork from a script
    the recognizer may have mangled.
    """
    assert rules.normalize("३०२०१५", field("pin")) == "३०२०१५"


def test_normalization_does_not_pad_or_truncate(field):
    short = "74791098499"
    assert rules.normalize(short, field("aadhaar")) == short
    long = "7479109849922"
    assert rules.normalize(long, field("aadhaar")) == long


# -- invisible characters ----------------------------------------------------


@pytest.mark.parametrize(
    "raw",
    [
        "​​",  # zero-width spaces
        "  ",  # non-breaking spaces
        "﻿",  # BOM
        "⁠",  # word joiner
        "‎‏",  # bidi marks
        " \t\n ",
    ],
)
def test_values_made_only_of_invisible_characters_become_empty(raw):
    """Otherwise they are non-empty to a length check and blank to the user,
    who would confirm an empty field believing they had filled it."""
    assert rules.strip_invisible(raw) == ""


def test_invisible_characters_inside_a_value_are_removed(field):
    assert rules.normalize("AKQPS​3417M", field("pan")) == "AKQPS3417M"


def test_full_width_digits_are_folded_to_ascii(field):
    """NFKC folding, so a full-width digit cannot slip past an ASCII range."""
    assert rules.normalize("３０２０１５", field("pin")) == "302015"


# -- the ASCII-digit trap ----------------------------------------------------


def test_devanagari_digits_do_not_satisfy_the_numeric_patterns():
    """`str.isdigit()` and `\\d` both accept these. The rules must not.

    This is the trap the module docstring warns about, pinned as a test: a
    validator built on either would accept Devanagari digits as a PIN code.
    """
    assert "३०२०१५".isdigit(), "precondition: Python considers these digits"
    assert not rules.PATTERNS[FieldType.PIN].match("३०२०१५")
    assert not rules.PATTERNS[FieldType.AADHAAR].match("७४७९१०९८४९९२")
    assert not rules.PATTERNS[FieldType.PHONE].match("९८१२३४५६०७")


# -- length and format -------------------------------------------------------


def test_fixed_length_fields_require_an_exact_length(field):
    assert rules.length_error("74791098499", field("aadhaar"))
    assert rules.length_error("7479109849922", field("aadhaar"))
    assert rules.length_error("747910984992", field("aadhaar")) is None


def test_free_text_fields_have_an_upper_bound_only(field):
    city = field("city")
    assert rules.length_error("Kochi", city) is None
    assert rules.length_error("K" * 41, city)


def test_format_errors_explain_themselves_in_plain_language(field):
    """The detail reaches the user, so it has to be usable by someone who does
    not know what a regular expression is."""
    detail = rules.format_error("AKQPS34I7M", field("pan"))
    assert detail and "five letters" in detail
    assert "[A-Z]" not in detail and "regex" not in detail.lower()


# -- range -------------------------------------------------------------------


def test_future_dates_are_out_of_range(field):
    detail = rules.range_error(
        "2030-01-01", field("dob"), today=dt.date(2026, 9, 6)
    )
    assert detail and "future" in detail


def test_minors_are_out_of_range(field):
    detail = rules.range_error(
        "2015-06-01", field("dob"), today=dt.date(2026, 9, 6)
    )
    assert detail and "18" in detail


def test_the_age_boundary_is_exact(field):
    """Someone turning 18 today is 18. Someone turning 18 tomorrow is not.

    An off-by-one here either bars an eligible adult or admits a minor.
    """
    today = dt.date(2026, 9, 6)
    dob = field("dob")
    assert rules.range_error("2008-09-06", dob, today=today) is None
    assert rules.range_error("2008-09-07", dob, today=today) is not None


def test_range_is_silent_on_unparseable_dates(field):
    """Already reported as a format error -- reporting it twice would mean the
    reason depends on check order rather than on the defect."""
    assert rules.range_error("not a date", field("dob")) is None


def test_range_does_not_apply_to_non_date_fields(field):
    assert rules.range_error("AKQPS3417M", field("pan")) is None


# -- declared enum names (review findings) --------------------------------------


def _enum_field(names):
    from lucidform.models import FieldSpec, FieldType

    return FieldSpec(
        id="g", acroform_name="g", label="G", type=FieldType.ENUM,
        enum_values=("Male", "Female"), enum_names=names,
    )


def test_a_declared_name_is_compared_after_the_same_unicode_normalisation():
    """U+095B (precomposed ज़) is NFKC-decomposed in the value; the name must be too."""
    field = _enum_field({"Male": ("ज़",)})
    assert rules.normalize("ज़", field) == "Male"
    assert rules.normalize("ज़", field) == "Male"


def test_a_declared_name_does_not_leak_across_options():
    field = _enum_field({"Male": ("purush",)})
    assert rules.normalize("purush", field) == "Male"
    assert rules.normalize("mahila", field) == "mahila"  # undeclared: left for the enum check
