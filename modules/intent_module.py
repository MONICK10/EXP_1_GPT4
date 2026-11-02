"""Intent Module - uses the LLM to decide which module should answer.

Example: "Recommend a gaming laptop"            -> RECOMMENDATION
         "How do I return my order?"            -> FAQ
         "Is the Galaxy S24 waterproof?"        -> PRODUCT_QA
         "What do customers say about XM5?"     -> REVIEW
"""
from llm import LLMError, ask_json

INTENTS = ["FAQ", "RECOMMENDATION", "PRODUCT_QA", "REVIEW"]

PROMPT = """Classify the e-commerce customer message into exactly one intent.

FAQ            - store policy or the customer's own order: delivery, returns, refunds, payment,
                 cancellation, warranty, tracking, support.
RECOMMENDATION - wants the store to suggest a product: recommend, suggest, best, which should I buy,
                 looking for, under a budget.
PRODUCT_QA     - asks a factual specification of one named product: price, storage, battery hours,
                 camera megapixels, waterproof rating, processor.
REVIEW         - asks about other customers' experience of a product: reviews, ratings, opinions,
                 feedback, pros and cons, "what do people say".

Rule: if the message contains the word review, rating, opinion, feedback, pros or cons, the intent is
REVIEW even when a product is named. Only use PRODUCT_QA when a specification is asked for.

Examples:
"Where is my parcel? I want to track it"            -> FAQ
"Recommend a gaming laptop under 80000"             -> RECOMMENDATION
"Is the Samsung Galaxy S24 waterproof?"             -> PRODUCT_QA
"Show reviews of Sony WH-1000XM5"                   -> REVIEW
"What do customers think about the Pixel 8a?"       -> REVIEW
"What is the battery life of MacBook Air M3?"       -> PRODUCT_QA

Message: "{q}"

Return JSON: {{"intent": "<one of FAQ, RECOMMENDATION, PRODUCT_QA, REVIEW>",
"reason": "<why THIS message fits that intent, max 12 words. Describe the message itself.
Do not copy the rules or the intent descriptions above.>"}}"""


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
