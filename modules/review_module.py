"""Review Module - sentiment analysis of reviews + LLM review summary and buying suggestion.

Example: "Excellent battery backup" -> Positive,  "Camera quality is poor" -> Negative
"""
import re

import pandas as pd

from llm import ask

POSITIVE = {"excellent", "great", "good", "best", "amazing", "love", "smooth", "fast", "happy", "worth",
            "stunning", "comfortable", "detailed", "bright", "value", "premium", "useful", "light",
            "silent", "decent", "insanely", "long"}
NEGATIVE = {"poor", "bad", "hot", "loud", "drains", "disappointed", "expensive", "costly", "annoying",
            "hurting", "limited", "bulky", "not", "average", "slow", "ads", "only", "inaccurate"}


def sentiment(text):
    """Count positive and negative words. More positive -> Positive, and so on."""
    words = re.findall(r"[a-z]+", text.lower())
    score = sum(w in POSITIVE for w in words) - sum(w in NEGATIVE for w in words)
    if score > 0:
        return "Positive", score
    if score < 0:
        return "Negative", score
    return "Neutral", score


class ReviewModule:
    def __init__(self, path, product_module):
        self.df = pd.read_csv(path)
        self.products = product_module

    def summarize(self, query):
        p, _ = self.products.find(query)
        rows = self.df[self.df.product_id == p.product_id]
        if rows.empty:
            return {"answer": f"There are no reviews yet for {p.product_name}.",
                    "context": {"type": "reviews", "items": []}}
        items = []
        for r in rows.itertuples():
            label, score = sentiment(r.review)
            items.append({"review": r.review, "rating": int(r.rating), "sentiment": label})
        counts = pd.Series([x["sentiment"] for x in items]).value_counts().to_dict()
        text = "\n".join(f"- ({x['sentiment']}, {x['rating']} stars) {x['review']}" for x in items)
        prompt = (f"Customer reviews for {p.product_name}:\n{text}\n\n"
                  "Write: 1) a 2-sentence overall summary, 2) Pros as bullets, 3) Cons as bullets, "
                  "4) a one-line buying suggestion. Use only these reviews.")
        return {"answer": ask(prompt),
                "context": {"type": "reviews", "product": p.product_name, "counts": counts,
                            "avg_rating": round(rows.rating.mean(), 1), "items": items}}
