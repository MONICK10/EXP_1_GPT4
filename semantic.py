"""
semantic.py - Semantic search using embeddings + cosine similarity.

Example:
    index = SemanticIndex(["How do I track my order?", "How do I cancel my order?"])
    index.search("Where is my parcel?", k=1)  ->  [(0, 0.71)]

It uses Sentence Transformers (all-MiniLM-L6-v2) when installed.
If not available, it falls back to TF-IDF vectors, so the app still works.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_MODEL = None
_MODEL_FAILED = False


def _get_model():
    global _MODEL, _MODEL_FAILED
    if _MODEL is None and not _MODEL_FAILED:
        try:
            from sentence_transformers import SentenceTransformer
            _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:  # no internet / not installed
            print("[semantic] Sentence Transformers unavailable, using TF-IDF:", e)
            _MODEL_FAILED = True
    return _MODEL


class SemanticIndex:
    def __init__(self, texts):
        self.texts = list(texts)
        model = _get_model()
        if model is not None:
            self.method = "Sentence Transformers (all-MiniLM-L6-v2)"
            self.model = model
            self.vectors = model.encode(self.texts, normalize_embeddings=True)
        else:
            self.method = "TF-IDF"
            self.model = None
            self.tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.vectors = self.tfidf.fit_transform(self.texts)

    def _embed(self, query):
        if self.model is not None:
            return self.model.encode([query], normalize_embeddings=True)
        return self.tfidf.transform([query])

    def scores(self, query):
        return cosine_similarity(self._embed(query), self.vectors)[0]

    def search(self, query, k=3):
        s = self.scores(query)
        top = np.argsort(-s)[:k]
        return [(int(i), round(float(s[i]), 3)) for i in top]
