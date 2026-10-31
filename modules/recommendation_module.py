"""Recommendation Module - TF-IDF finds the top-3 similar products, Ollama picks the best.

Example: "gaming laptop under 80000"  ->  top-3 = Lenovo LOQ 15, ...  ->  LLM recommends one.
"""
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from llm import ask


def extract_budget(text):
    """'under 80000' -> 80000, 'below 50k' -> 50000, no budget -> None"""
    m = re.search(r"(?:under|below|less than|within|upto|up to|budget)\s*(?:rs\.?|₹)?\s*([\d,]+)\s*(k)?",
                  text.lower())
    if not m:
        return None
    value = int(m.group(1).replace(",", ""))
    return value * 1000 if m.group(2) else value


CATEGORY_WORDS = {
    "laptop": "Laptop", "notebook": "Laptop", "phone": "Mobile", "mobile": "Mobile", "smartphone": "Mobile",
    "headphone": "Headphones", "earbud": "Earbuds", "earphone": "Earbuds", "watch": "Smartwatch",
    "console": "Gaming Console", "tv": "Television", "television": "Television",
    "mouse": "Accessories", "ssd": "Accessories",
}


def extract_category(text):
    """'gaming laptop under 80000' -> 'Laptop'"""
    t = text.lower()
    for word, cat in CATEGORY_WORDS.items():
        if re.search(rf"\b{word}s?\b", t):
            return cat
    return None


class RecommendationModule:
    def __init__(self, products_df):
        self.df = products_df
        docs = (self.df.product_name + " " + self.df.brand + " " + self.df.category + " " +
                self.df.description).tolist()
        self.tfidf = TfidfVectorizer(stop_words="english")
        self.matrix = self.tfidf.fit_transform(docs)

    def top_k(self, query, k=3):
        scores = cosine_similarity(self.tfidf.transform([query]), self.matrix)[0]
        df = self.df.assign(score=scores.round(3))
        category = extract_category(query)
        if category:
            df = df[df.category == category]
        budget = extract_budget(query)
        if budget:
            df = df[df.price <= budget]
        return df.sort_values("score", ascending=False).head(k), budget, category

    def recommend(self, query):
        top, budget, category = self.top_k(query)
        if top.empty or top.score.max() == 0:
            return {"answer": "Sorry, I could not find a matching product. Try another description.",
                    "context": {"type": "products", "items": []}}
        listing = "\n".join(f"- {r.product_name} ({r.brand}), Rs. {r.price}: {r.description}"
                            for r in top.itertuples())
        prompt = (f"Customer request: {query}\n\nTop matching products from our store:\n{listing}\n\n"
                  "Recommend the single best product for this customer. Start with the product name in bold, "
                  "then give 2-3 bullet points on why it fits. Mention one alternative from the list. "
                  "Use only the products listed.")
        items = top[["product_id", "product_name", "brand", "price", "score"]].to_dict("records")
        return {"answer": ask(prompt),
                "context": {"type": "products", "method": "TF-IDF + cosine similarity",
                            "budget": budget, "category": category, "items": items}}
