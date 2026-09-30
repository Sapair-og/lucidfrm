"""Session setup shared by the whole suite.

The blank KYC template (`data/forms/ckyc_individual.pdf`) is a generated
artefact and is not committed. A fresh clone therefore has no PDF, and every
test that loads the schema would fail on a missing file rather than on anything
it tests. Generating it once per session keeps the suite runnable from a clean
checkout -- which is exactly what CI and a new teammate start from.
"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session", autouse=True)
def _blank_form_template():
    from lucidform.config import get_settings
    from lucidform.schema import make_form

    if not get_settings().form_pdf.exists():
        make_form.build()
