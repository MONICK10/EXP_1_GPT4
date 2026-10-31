"""Intent Module - uses the LLM to decide which module should answer.

Example: "Recommend a gaming laptop"            -> RECOMMENDATION
         "How do I return my order?"            -> FAQ
         "Is the Galaxy S24 waterproof?"        -> PRODUCT_QA
         "What do customers say about XM5?"     -> REVIEW
"""
from llm import LLMError, ask_json

INTENTS = ["FAQ", "RECOMMENDATION", "PRODUCT_QA", "REVIEW"]

PROMPT = """Classify the e-commerce customer message into exactly one intent:
FAQ            - orders, delivery, returns, refunds, payment, cancellation, warranty, support
RECOMMENDATION - wants a product suggestion (recommend, suggest, best, which should I buy, under budget)
PRODUCT_QA     - asks a specific fact about a named product (price, specs, waterproof, battery, camera)
REVIEW         - asks what customers think, reviews, ratings, opinions, pros and cons

Message: "{q}"

Return JSON: {{"intent": "<one of FAQ, RECOMMENDATION, PRODUCT_QA, REVIEW>", "reason": "<short reason>"}}"""


def keyword_intent(q):
    """Backup rule-based intent, used only if the LLM reply is not valid."""
    q = q.lower()
    if any(w in q for w in ["review", "think", "opinion", "rating", "feedback", "pros", "cons", "customers say"]):
        return "REVIEW"
    if any(w in q for w in ["recommend", "suggest", "best", "which", "under", "budget", "looking for"]):
        return "RECOMMENDATION"
    if any(w in q for w in ["order", "return", "refund", "deliver", "cancel", "payment", "track", "warranty", "coupon", "emi"]):
        return "FAQ"
    return "PRODUCT_QA"


def detect_intent(query):
    try:
        data = ask_json(PROMPT.format(q=query), default={}) or {}
    except LLMError:
        raise
    intent = str(data.get("intent", "")).upper().strip()
    if intent not in INTENTS:
        return {"intent": keyword_intent(query), "reason": "Keyword fallback", "source": "rules"}
    return {"intent": intent, "reason": data.get("reason", ""), "source": "LLM"}
