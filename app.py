"""
Ex. No. 1 - AI-Powered E-Commerce Chatbot (RAG) using Ollama
Monick S - URK23CS1167

Run:  python app.py    then open  http://localhost:5001
"""
import pandas as pd
from flask import Flask, jsonify, render_template, request

from llm import LLMError, status
from modules.chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()


@app.errorhandler(LLMError)
def llm_error(e):
    return jsonify(error=str(e)), 503


@app.get("/")
def home():
    return render_template("index.html", exp_no=1, title="ShopSmart AI – E-Commerce Chatbot",
                           n_products=len(bot.product.df), n_faqs=len(bot.faq.df),
                           n_reviews=len(bot.review.df), embed_method=bot.faq.index.method)


@app.get("/api/status")
def api_status():
    return jsonify(status())


@app.post("/api/chat")
def api_chat():
    data = request.get_json()
    query = (data.get("message") or "").strip()
    if not query:
        return jsonify(error="Please type a message."), 400
    return jsonify(bot.chat(query, data.get("intent")))


@app.get("/api/products")
def api_products():
    return jsonify(bot.product.df.to_dict("records"))


if __name__ == "__main__":
    app.run(port=5001, debug=False)
