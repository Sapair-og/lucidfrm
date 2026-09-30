"""The LangGraph orchestrator: parity with the loop it replaced, and its shape.

Parity is the claim that matters. The golden file was recorded from the
pre-LangGraph loop, so a persona session producing byte-identical events and
transcripts on the graph is evidence the swap changed nothing observable -- the
same evidence the paper needs for "replacing the orchestrator did not weaken the
guarantee".
"""

from __future__ import annotations

import json

import pytest

from lucidform.orchestrate import graph as session_graph
from tests.golden_sessions import GOLDEN, record


@pytest.fixture(scope="module")
def golden():
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


@pytest.mark.parametrize("lang", ["en", "hi"])
def test_persona_sessions_match_the_pre_langgraph_loop(golden, lang):
    now = record(lang)
    for pid, expected in golden[lang].items():
        assert now[pid]["events"] == expected["events"], f"{lang}/{pid}: event stream differs"
        assert now[pid]["said"] == expected["said"], f"{lang}/{pid}: what the user heard differs"


def test_the_graph_has_the_pipeline_stages_as_nodes():
    nodes = set(session_graph.node_names())
    for stage in ("ask", "listen", "extract", "explain", "gate", "readback", "confirm", "commit"):
        assert stage in nodes


def test_commit_is_reachable_only_through_confirm():
    """The graph-level statement of the thesis: no edge skips confirmation.

    FormState.commit re-verifies the receipt regardless, so a wrong edge would be
    blocked and logged -- but the graph should not have one in the first place.
    """
    into_commit = {src for src, dst in session_graph.edges() if dst == "commit"}
    assert into_commit == {"confirm"}


def test_the_graph_draws_as_mermaid_for_the_paper():
    text = session_graph.mermaid()
    assert "commit" in text and "confirm" in text
