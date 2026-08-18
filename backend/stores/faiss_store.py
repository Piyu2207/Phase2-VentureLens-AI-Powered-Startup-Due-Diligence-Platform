import json, pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer
from backend.config import FAISS_DIR, EMBEDDING_MODEL

class FAISSStore:
    def __init__(self, directory=FAISS_DIR):
        self.directory = Path(directory)
        self.index_path = self.directory / "index.faiss"
        self.metadata_path = self.directory / "metadata.json"
        self.bm25_path = self.directory / "bm25.pkl"
        self._model = self._index = self._metadata = self._bm25 = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(EMBEDDING_MODEL)
        return self._model

    def build(self, chunks):
        self.directory.mkdir(parents=True, exist_ok=True)
        texts = [x["text"] for x in chunks]
        vectors = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True).astype("float32")
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        faiss.write_index(index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
        from rank_bm25 import BM25Okapi
        bm25 = BM25Okapi([t.lower().split() for t in texts])
        with open(self.bm25_path, "wb") as f:
            pickle.dump(bm25, f)
        self._index, self._metadata, self._bm25 = index, chunks, bm25

    def load(self):
        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError("FAISS artifacts missing. Run scripts/build_indexes.py.")
        if self._index is None:
            self._index = faiss.read_index(str(self.index_path))
        if self._metadata is None:
            self._metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        if self._bm25 is None:
            with open(self.bm25_path, "rb") as f:
                self._bm25 = pickle.load(f)
        return self

    def dense_search(self, query, k=10):
        self.load()
        q = self.model.encode([query], normalize_embeddings=True).astype("float32")
        scores, ids = self._index.search(q, k)
        return [{"rank": i+1, "score": float(scores[0][i]), **self._metadata[idx]}
                for i, idx in enumerate(ids[0]) if idx >= 0]

    def bm25_search(self, query, k=10):
        self.load()
        scores = self._bm25.get_scores(query.lower().split())
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [{"rank": i+1, "score": float(scores[idx]), **self._metadata[idx]}
                for i, idx in enumerate(ranked)]

    def hybrid_search(self, query, startup_name, k=5):
        dense = self.dense_search(query, max(10, k*3))
        sparse = self.bm25_search(query, max(10, k*3))
        dr = {x["chunk_id"]: x["rank"] for x in dense}
        br = {x["chunk_id"]: x["rank"] for x in sparse}
        items = {x["chunk_id"]: x for x in dense + sparse}
        fused = []
        for cid, item in items.items():
            score = (1/(60+dr[cid]) if cid in dr else 0) + (1/(60+br[cid]) if cid in br else 0)
            if item["startup"].lower() == startup_name.lower():
                score += 0.02
            fused.append({**item, "rrf_score": score})
        return sorted(fused, key=lambda x: x["rrf_score"], reverse=True)[:k]
