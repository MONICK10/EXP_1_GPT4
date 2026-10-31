"""FAQ Module - semantic search on FAQs using embeddings + cosine similarity.

Example: "Where is my parcel?"  ->  matches FAQ "How do I track my order?" (score 0.6)
"""
import pandas as pd

from llm import ask
from semantic import SemanticIndex


class FAQModule:
    def __init__(self, path):
        self.df = pd.read_csv(path)
        # index question + answer so more words can match
        self.index = SemanticIndex((self.df["question"] + " " + self.df["answer"]).tolist())
        # TF-IDF scores are lower than embedding scores, so use a lower cut-off
        self.threshold = 0.35 if self.index.model is not None else 0.15

    def answer(self, query):
        matches = self.index.search(query, k=3)
        context = [{"question": self.df.question[i], "answer": self.df.answer[i], "score": s}
                   for i, s in matches]
        best = context[0]
        if best["score"] < self.threshold:
            text = ("Sorry, I could not find this in our FAQs. "
                    "Please contact support at 1800-123-4567.")
        else:
            prompt = (f"You are a polite e-commerce support assistant.\n"
                      f"Customer question: {query}\n"
                      f"Matched FAQ: {best['question']}\nFAQ answer: {best['answer']}\n\n"
                      "Reply to the customer in 2-3 short sentences using ONLY the FAQ answer.")
            text = ask(prompt)
        return {"answer": text, "context": {"type": "faq", "method": self.index.method, "items": context}}
