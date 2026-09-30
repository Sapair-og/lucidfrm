"""Hybrid retrieval over the help corpus: dense embeddings + BM25, fused by rank.

The two retrievers fail differently, which is the reason for having both. BM25
is exact on the terms a form uses ("Form 60", "OVD", "Verhoeff") and useless on
a paraphrase; embeddings handle "pan card nahi hai toh kya karu" and can drift
on an exact identifier. Reciprocal rank fusion combines them without having to
calibrate one score against the other.

The embedder is injected. Live runs use Gemini; the offline suite uses a
deterministic hashing embedder so retrieval is testable without a key.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np
from rank_bm25 import BM25Okapi

from lucidform.help.corpus import Chunk

RRF_K = 60
_TOKEN = re.compile(r"\w+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.casefold())


class Embedder(Protocol):
    name: str
    dims: int

    def embed_documents(self, texts: list[str]) -> np.ndarray: ...

    def embed_query(self, text: str) -> np.ndarray: ...


def _normalise(v: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(norms == 0, 1.0, norms)


class HashEmbedder:
    """Bag-of-words hashed into a fixed vector. Deterministic; for tests only."""

    # Wide enough that hash collisions between unrelated words are rare; at 256
    # the offline stand-in ranked obvious matches below noise.
    def __init__(self, dims: int = 4096) -> None:
        self.dims = dims
        self.name = f"hash-{dims}"

    def _one(self, text: str) -> np.ndarray:
        v = np.zeros(self.dims, dtype=np.float32)
        for tok in tokenize(text):
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            v[h % self.dims] += 1.0 if (h >> 8) & 1 else -1.0
        return v

    def embed_documents(self, texts):
        return _normalise(np.stack([self._one(t) for t in texts]))

    def embed_query(self, text):
        return _normalise(self._one(text)[None, :])[0]


class GeminiEmbedder:
    """`gemini-embedding-001`, with the asymmetric document/query task types."""

    # The free tier limits tokens per minute, not just requests: 100 legal
    # paragraphs in one call exhausts it. Small batches with a pause make the
    # one-off index build slow but reliable.
    BATCH = 20
    PAUSE_S = 4.0

    def __init__(self, model: str | None = None, dims: int = 768, sdk=None, sleep=None) -> None:
        from lucidform.config import get_settings

        settings = get_settings()
        self.model = model or settings.embedding_model
        self.dims = dims
        self.name = f"{self.model}-{dims}"
        if sdk is None:
            from lucidform.llm import make_genai_client

            sdk = make_genai_client()
        self._sdk = sdk
        if sleep is None:
            import time

            sleep = time.sleep
        self._sleep = sleep

    def _embed(self, texts: list[str], task: str) -> np.ndarray:
        from google.genai import types

        from lucidform.llm import with_retries

        out = []
        for i in range(0, len(texts), self.BATCH):
            if i:
                self._sleep(self.PAUSE_S)
            batch = texts[i : i + self.BATCH]
            response = with_retries(
                lambda: self._sdk.models.embed_content(
                    model=self.model,
                    contents=batch,
                    config=types.EmbedContentConfig(
                        task_type=task, output_dimensionality=self.dims
                    ),
                ),
                max_retries=6,
                base_delay=5.0,
                sleep=self._sleep,
            )
            if len(response.embeddings) != len(batch):
                raise RuntimeError(
                    f"{self.model} returned {len(response.embeddings)} vectors for {len(batch)} texts"
                )
            out.extend(e.values for e in response.embeddings)
        # Truncated Matryoshka embeddings are not unit length; cosine needs them to be.
        return _normalise(np.asarray(out, dtype=np.float32))

    def embed_documents(self, texts):
        return self._embed(texts, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text):
        return self._embed([text], "RETRIEVAL_QUERY")[0]


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = RRF_K) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda item: (-scores[item], item))


@dataclass(frozen=True)
class Hit:
    chunk_id: str
    label: str
    url: str
    text: str
    rank: int


def _corpus_digest(chunks: list[Chunk]) -> str:
    h = hashlib.sha256()
    for c in chunks:
        h.update(c.chunk_id.encode("utf-8"))
    return h.hexdigest()


class HelpIndex:
    CANDIDATES = 20  # per retriever, before fusion

    def __init__(self, chunks: list[Chunk], vectors: np.ndarray, embedder: Embedder) -> None:
        self.chunks = chunks
        self.vectors = vectors
        self.embedder = embedder
        self._by_id = {c.chunk_id: c for c in chunks}
        self._bm25 = BM25Okapi([tokenize(f"{c.label} {c.text}") for c in chunks])

    @classmethod
    def build(cls, chunks: list[Chunk], embedder: Embedder) -> HelpIndex:
        vectors = embedder.embed_documents([f"{c.label}\n{c.text}" for c in chunks])
        return cls(chunks, vectors, embedder)

    def search(self, query: str, k: int = 4) -> list[Hit]:
        dense = self.vectors @ self.embedder.embed_query(query)
        dense_rank = [self.chunks[i].chunk_id for i in np.argsort(-dense)[: self.CANDIDATES]]
        sparse = self._bm25.get_scores(tokenize(query))
        sparse_rank = [self.chunks[i].chunk_id for i in np.argsort(-sparse)[: self.CANDIDATES]]
        hits: list[Hit] = []
        seen_text: set[str] = set()
        for cid in reciprocal_rank_fusion([dense_rank, sparse_rank]):
            chunk = self._by_id[cid]
            # UIDAI publishes the same FAQ on more than one page; a duplicate
            # passage spends a context slot and adds no evidence.
            key = " ".join(tokenize(chunk.text))
            if key in seen_text:
                continue
            seen_text.add(key)
            hits.append(Hit(cid, chunk.label, chunk.url, chunk.text, len(hits)))
            if len(hits) == k:
                break
        return hits

    def get(self, chunk_id: str) -> Chunk | None:
        return self._by_id.get(chunk_id)

    # -- persistence -------------------------------------------------------------

    def save(self, directory: Path) -> None:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "chunks.jsonl").open("w", encoding="utf-8") as fh:
            for c in self.chunks:
                fh.write(json.dumps(c.to_json(), ensure_ascii=False) + "\n")
        np.savez_compressed(directory / "index.npz", vectors=self.vectors)
        meta = {
            "embedder": self.embedder.name,
            "dims": int(self.vectors.shape[1]),
            "chunks": len(self.chunks),
            "corpus_digest": _corpus_digest(self.chunks),
        }
        (directory / "index_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, directory: Path, embedder: Embedder) -> HelpIndex:
        directory = Path(directory)
        meta = json.loads((directory / "index_meta.json").read_text(encoding="utf-8"))
        if meta["embedder"] != embedder.name:
            # Query vectors from one model are meaningless against another's.
            raise ValueError(
                f"index was built with {meta['embedder']}, not {embedder.name}; rebuild it"
            )
        chunks = [
            Chunk(**json.loads(line))
            for line in (directory / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if _corpus_digest(chunks) != meta["corpus_digest"]:
            raise ValueError("chunks.jsonl does not match the index it was saved with; rebuild it")
        vectors = np.load(directory / "index.npz")["vectors"]
        return cls(chunks, vectors, embedder)
