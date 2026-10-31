"""Chatbot - joins all modules. Detect intent, then route the query to the right module."""
import os

import pandas as pd

from .faq_module import FAQModule
from .intent_module import detect_intent
from .product_module import ProductModule
from .recommendation_module import RecommendationModule
from .review_module import ReviewModule

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


class Chatbot:
    def __init__(self):
        products = pd.read_csv(os.path.join(DATA, "products.csv"))
        self.faq = FAQModule(os.path.join(DATA, "faqs.csv"))
        self.recommender = RecommendationModule(products)
        self.product = ProductModule(products)
        self.review = ReviewModule(os.path.join(DATA, "reviews.csv"), self.product)
        self.routes = {
            "FAQ": ("FAQ Module", self.faq.answer),
            "RECOMMENDATION": ("Recommendation Module", self.recommender.recommend),
            "PRODUCT_QA": ("Product Module", self.product.answer),
            "REVIEW": ("Review Module", self.review.summarize),
        }

    def chat(self, query, forced_intent=None):
        intent = ({"intent": forced_intent, "reason": "Selected manually", "source": "user"}
                  if forced_intent in self.routes else detect_intent(query))
        module_name, handler = self.routes[intent["intent"]]
        result = handler(query)
        return {"query": query, "intent": intent, "module": module_name, **result}
