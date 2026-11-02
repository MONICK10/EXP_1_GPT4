"""Product Module - finds the product the user is asking about and answers using its details (RAG).

Example: "Is the iPhone 15 waterproof?"  ->  retrieves iPhone 15 row  ->  "Yes, it is IP68 rated..."
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from llm import ask


class ProductModule:
    def __init__(self, products_df):
        self.df = products_df
        names = (self.df.product_name + " " + self.df.brand + " " + self.df.category).tolist()
        # character n-grams handle short names like "S24" or "XM5"
        self.tfidf = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
        self.matrix = self.tfidf.fit_transform([n.lower() for n in names])

    def find(self, query):
        scores = cosine_similarity(self.tfidf.transform([query.lower()]), self.matrix)[0]
        i = int(scores.argmax())
        return self.df.iloc[i], round(float(scores[i]), 3)

    def answer(self, query):
        p, score = self.find(query)
        info = (f"Name: {p.product_name}\nBrand: {p.brand}\nCategory: {p.category}\n"
                f"Price: Rs. {p.price}\nDescription: {p.description}")
        prompt = (f"Product information:\n{info}\n\nCustomer question: {query}\n\n"
                  "Answer the question directly in 2-4 sentences using ONLY the product information above. "
                  "If the information above answers the question, state it confidently and do not add doubts "
                  "or say that details are missing. Only if the detail is truly absent from the information, "
                  "say that it is not listed.")
        return {"answer": ask(prompt),
                "context": {"type": "product", "score": score,
                            "items": [{"product_id": p.product_id, "product_name": p.product_name,
                                       "price": int(p.price), "description": p.description}]}}
