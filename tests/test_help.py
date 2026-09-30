"""The help agent: corpus, retrieval, and the answer check -- offline.

Retrieval is exercised with BM25 plus a deterministic hashing embedder, so none
of this needs a key. What the live embedding model and answer model actually do
is measured by `lucidform help eval`, not asserted here.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from lucidform.help import corpus
from lucidform.help.answer import HelpAgent, HelpReply, ScriptedAnswerClient
from lucidform.help.index import HashEmbedder, HelpIndex, reciprocal_rank_fusion
from lucidform.schema import loader

SOURCES = Path(__file__).resolve().parents[1] / "data" / "help" / "sources"


@pytest.fixture(scope="module")
def chunks():
    return corpus.load_chunks(SOURCES)


@pytest.fixture(scope="module")
def index(chunks):
    return HelpIndex.build(chunks, HashEmbedder())


@pytest.fixture(scope="module")
def schema():
    return loader.load()


# -- corpus ----------------------------------------------------------------------


def test_every_source_file_matches_its_manifest_hash():
    """The corpus is part of the evaluation; a silently edited source is a different corpus."""
    manifest = json.loads((SOURCES / "manifest.json").read_text(encoding="utf-8-sig"))
    assert len(manifest) == 6
    for entry in manifest:
        digest = hashlib.sha256((SOURCES / entry["file"]).read_bytes()).hexdigest()
        assert digest == entry["sha256"], entry["file"]


def test_the_rbi_faq_is_chunked_one_question_per_chunk(chunks):
    rbi = [c for c in chunks if c.source == "rbi_kyc_faq_2025.pdf"]
    labels = [c.label for c in rbi]
    assert len(rbi) == 37
    assert "RBI KYC FAQ, Q10" in labels
    q10 = next(c for c in rbi if c.label == "RBI KYC FAQ, Q10")
    assert "Aadhaar number mandatory" in q10.text


def test_the_pan_faq_keeps_its_form_sections_apart(chunks):
    pan = {c.label: c for c in chunks if c.source == "incometax_pan_faq.md"}
    assert "Income Tax PAN FAQ, Q1" in pan
    assert "Income Tax PAN FAQ (Form 93), Q4" in pan
    assert "Aadhaar is mandatory" in pan["Income Tax PAN FAQ (Form 93), Q4"].text


def test_uidai_pages_yield_question_answer_chunks_not_navigation(chunks):
    uidai = [c for c in chunks if c.source.startswith("uidai_")]
    assert len(uidai) >= 30
    assert any("Aadhaar number will always remain the same" in c.text for c in uidai)
    assert not any(c.text.strip().startswith(("My Aadhaar Downloads", "Menu")) for c in uidai)


def test_long_legal_text_is_windowed(chunks):
    md = [c for c in chunks if c.source == "rbi_kyc_master_direction.html"]
    assert len(md) > 50
    assert max(len(c.text) for c in md) <= corpus.MAX_CHARS + 200
    assert any("Officially Valid Document" in c.text for c in md)


def test_chunk_ids_are_unique_and_every_chunk_carries_its_url(chunks):
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))
    assert all(c.url.startswith("https://") for c in chunks)
    assert all(c.text.strip() for c in chunks)


def test_chunking_is_deterministic():
    a = [c.chunk_id for c in corpus.load_chunks(SOURCES)]
    b = [c.chunk_id for c in corpus.load_chunks(SOURCES)]
    assert a == b


# -- retrieval -----------------------------------------------------------------


def test_duplicate_passages_are_returned_once(index):
    hits = index.search("Will my Aadhaar number get changed after updation?", k=4)
    texts = [" ".join(h.text.split()).casefold() for h in hits]
    assert len(texts) == len(set(texts))


def test_reciprocal_rank_fusion_rewards_agreement():
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "a", "d"]], k=60)
    assert fused[:2] == ["a", "b"] or fused[:2] == ["b", "a"]
    assert set(fused) == {"a", "b", "c", "d"}
    assert fused.index("d") > fused.index("a")


# The offline embedder is a bag-of-words stand-in, so these queries share
# distinctive words with their source. Retrieval quality on paraphrased and
# code-mixed questions is a live measurement (`lucidform help eval`), not a
# unit-test assertion.
@pytest.mark.parametrize(
    "query, expected_label",
    [
        ("Is Aadhaar number mandatory for purposes of KYC?", "RBI KYC FAQ, Q10"),
        ("documents required for opening a bank account by an individual", "RBI KYC FAQ, Q5"),
        ("Is Aadhaar mandatory for applying PAN?", "Income Tax PAN FAQ (Form 93), Q4"),
        ("Will my Aadhaar number get changed after updation?", None),
    ],
)
def test_keyword_questions_retrieve_their_source(index, query, expected_label):
    hits = index.search(query, k=4)
    assert len(hits) == 4
    if expected_label:
        assert expected_label in [h.label for h in hits]
    else:
        assert any("always remain the same" in h.text for h in hits)


def test_the_index_round_trips_through_disk(index, tmp_path):
    index.save(tmp_path)
    loaded = HelpIndex.load(tmp_path, HashEmbedder())
    q = "Is Aadhaar number mandatory for KYC?"
    assert [h.chunk_id for h in loaded.search(q, k=4)] == [h.chunk_id for h in index.search(q, k=4)]


def test_an_index_built_with_another_embedder_is_refused(index, tmp_path):
    index.save(tmp_path)
    with pytest.raises(ValueError):
        HelpIndex.load(tmp_path, HashEmbedder(dims=128))


# -- the evaluation set and its scoring ----------------------------------------------


def test_every_gold_label_exists_in_the_corpus(chunks):
    """A gold label that matches nothing would score a correct retrieval as a miss."""
    from lucidform.help.evaluate import load_set

    labels = [c.label for c in chunks]
    items = load_set(SOURCES.parent / "eval_questions.yaml")
    assert sum(i["kind"] == "question" for i in items) == 30
    assert sum(i["kind"] == "control" for i in items) == 6
    for item in items:
        for g in item["gold"]:
            assert any(g in label for label in labels), f"{item['id']}: gold {g!r} matches no chunk"


def test_scoring_counts_hits_answers_and_refusals():
    from lucidform.help.evaluate import Row, summarise

    def row(kind, source, retrieved, cited, gold):
        return Row("x", kind, "pan", "en", "q", gold, retrieved, cited, source, "", "", 10.0)

    rows = [
        row("question", "rag", ["A", "B"], ["A"], ["A"]),      # hit, answered, gold cited
        row("question", "rag", ["B", "C"], ["B"], ["A"]),      # miss, answered, wrong cite
        row("question", "gloss", ["A"], [], ["A"]),            # hit, not answered
        row("control", "gloss", ["Z"], [], []),                # refused
        row("control", "rag", ["Z"], ["Z"], []),               # answered a control: bad
    ]
    s = summarise(rows)
    assert s["retrieval_hit_at_k"] == 66.7
    assert s["answer_rate"] == 66.7
    assert s["gold_citation_rate"] == 50.0
    assert s["control_refusal_rate"] == 50.0


# -- the answer and its check -------------------------------------------------------


def agent(index, *replies):
    return HelpAgent(index, ScriptedAnswerClient(list(replies)))


def test_a_cited_answer_is_spoken_with_its_source(index, schema):
    field = schema.by_id("aadhaar")
    question = "Is Aadhaar number mandatory for purposes of KYC?"
    # The agent adds the field label to the query; search the same way.
    hits = index.search(f"{question}\n{field.label}", k=4)
    cited = next(h for h in hits if h.label == "RBI KYC FAQ, Q10").chunk_id
    reply = agent(
        index,
        HelpReply(answer="No, Aadhaar is not mandatory for KYC.", cited_ids=[cited], answerable=True),
    ).answer(field, question, "en")

    assert reply.source == "rag"
    assert reply.cited_labels == ["RBI KYC FAQ, Q10"]
    assert "not mandatory" in reply.spoken and "RBI KYC FAQ, Q10" in reply.spoken


def test_a_citation_to_a_passage_that_was_not_retrieved_falls_back(index, schema):
    """The model is never trusted to cite truthfully; the check verifies it."""
    field = schema.by_id("pan")
    reply = agent(
        index, HelpReply(answer="Made up.", cited_ids=["no-such-chunk"], answerable=True)
    ).answer(field, "pan kya hota hai", "en")
    assert reply.source == "gloss"
    assert reply.fallback_reason == "citation_not_retrieved"
    assert field.explain("en") in reply.spoken


def test_an_uncited_answer_falls_back(index, schema):
    field = schema.by_id("pan")
    reply = agent(index, HelpReply(answer="Trust me.", cited_ids=[], answerable=True)).answer(
        field, "pan kya hota hai", "en"
    )
    assert reply.source == "gloss"
    assert reply.fallback_reason == "no_citation"


def test_an_unanswerable_question_falls_back_and_says_so(index, schema):
    field = schema.by_id("pan")
    reply = agent(index, HelpReply(answer="", cited_ids=[], answerable=False)).answer(
        field, "which bank has the best interest rate?", "en"
    )
    assert reply.source == "gloss"
    assert reply.fallback_reason == "not_answerable"
    assert field.explain("en") in reply.spoken


def test_a_model_failure_never_breaks_the_session(index, schema):
    field = schema.by_id("pan")
    reply = agent(index, RuntimeError("quota")).answer(field, "pan kya hota hai", "en")
    assert reply.source == "gloss"
    assert reply.fallback_reason.startswith("error")


def test_the_hindi_fallback_uses_the_hindi_gloss(index, schema):
    field = schema.by_id("pan")
    reply = agent(index, HelpReply(answer="", cited_ids=[], answerable=False)).answer(
        field, "pan kya hota hai", "hi"
    )
    assert field.explain("hi") in reply.spoken


def test_a_retrieval_failure_never_breaks_the_session(index, schema):
    """The embedding call is a live API call too; it sits inside the fallback."""

    class BrokenEmbedder:
        name = index.embedder.name
        dims = index.embedder.dims

        def embed_query(self, text):
            raise RuntimeError("embedding quota")

    broken = HelpIndex(index.chunks, index.vectors, BrokenEmbedder())
    field = schema.by_id("pan")
    reply = HelpAgent(broken, ScriptedAnswerClient([])).answer(field, "pan kya hota hai", "en")
    assert reply.source == "gloss"
    assert reply.fallback_reason == "error:RuntimeError"
    assert reply.retrieved_ids == []


def test_a_numbered_gold_label_matches_only_that_number():
    """'RBI KYC FAQ, Q1' is not a hit for Q10-Q19 (found in review)."""
    from lucidform.help.evaluate import Row

    def row(retrieved, cited=()):
        return Row("x", "question", "pan", "en", "q", ["RBI KYC FAQ, Q1"], list(retrieved), list(cited), "rag", "", "", 1.0)

    assert not row(["RBI KYC FAQ, Q10", "RBI KYC FAQ, Q12"]).hit
    assert row(["RBI KYC FAQ, Q12", "RBI KYC FAQ, Q1"]).hit
    assert not row([], ["RBI KYC FAQ, Q17"]).cited_gold
    # Phrase golds (UIDAI questions) still match inside a longer label.
    phrase = Row("y", "question", "aadhaar", "en", "q", ["Will my Aadhaar number get changed"],
                 ["UIDAI Aadhaar Update FAQ: Will my Aadhaar number get changed after updation?"], [], "rag", "", "", 1.0)
    assert phrase.hit


def test_an_error_on_a_control_is_not_a_refusal():
    """An outage must not read as perfect refusal behaviour (found in review)."""
    from lucidform.help.evaluate import Row, summarise

    rows = [
        Row("c1", "control", "pan", "en", "q", [], [], [], "gloss", "not_answerable", "", 1.0),
        Row("c2", "control", "pan", "en", "q", [], [], [], "gloss", "error:ClientError", "", 1.0),
    ]
    s = summarise(rows)
    assert s["control_refusal_rate"] == 100.0  # 1 of 1 scorable control
    assert s["errors"] == 1
    assert s["controls_scored"] == 1
