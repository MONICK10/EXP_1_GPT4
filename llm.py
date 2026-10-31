"""
llm.py - Small helper to talk to a local Ollama server.

Example:
    ask("Write one line about AI")  ->  "AI helps machines learn from data."

Ollama runs on your laptop at http://localhost:11434.
Change the model with an environment variable:
    PowerShell:  $env:OLLAMA_MODEL = "qwen2.5"
"""
import json
import os
import re

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


class LLMError(RuntimeError):
    pass


def ask(prompt, system=None, temperature=0.3, json_mode=False, timeout=600):
    """Send one prompt to Ollama and return the text answer."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if system:
        payload["system"] = system
    if json_mode:
        payload["format"] = "json"
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
    except requests.exceptions.ConnectionError:
        raise LLMError("Ollama is not running. Start it with:  ollama serve")
    if r.status_code == 404:
        raise LLMError(f"Model '{MODEL}' not found. Run:  ollama pull {MODEL}")
    r.raise_for_status()
    return r.json().get("response", "").strip()


def ask_json(prompt, system=None, temperature=0.2, default=None):
    """Ask for JSON and parse it safely. Returns `default` if parsing fails."""
    text = ask(prompt, system=system, temperature=temperature, json_mode=True)
    return parse_json(text, default)


def parse_json(text, default=None):
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"(\{.*\}|\[.*\])", text, re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
    return default


def status():
    """Check whether Ollama is reachable and the model is pulled."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        names = [m["name"] for m in r.json().get("models", [])]
        ok = any(n == MODEL or n.startswith(MODEL + ":") for n in names)
        return {"online": True, "model": MODEL, "model_ready": ok}
    except Exception:
        return {"online": False, "model": MODEL, "model_ready": False}


def as_list(value):
    """Make sure we get a list. "a, b" -> ["a", "b"];  ["a"] -> ["a"]"""
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [p.strip(" -•\t") for p in re.split(r"[\n,;]", value) if p.strip(" -•\t")]
    return []
