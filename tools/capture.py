"""
capture.py - Runs every experiment automatically, takes all the screenshots the lab record
needs, and records a demo video of each app.

Before running:
    1. Ollama is running and the model is pulled:   ollama pull llama3.2
    2. pip install -r requirements.txt
    3. python -m playwright install chromium

Run (from the repo folder):
    python tools/capture.py            -> all 6 experiments
    python tools/capture.py 3 5        -> only Exp 3 and Exp 5
    python tools/capture.py --home-only -> only screens that do not need the LLM

Output:
    screenshots/exp1/01_home_screen.png ...
    videos/Exp1_ECommerce_Chatbot.webm ...
"""
import os
import shutil
import socket
import subprocess
import sys
import time

import requests
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")
VIDEOS = os.path.join(ROOT, "videos")
try:
    import json
    CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
except Exception:
    CFG = {}
SINGLE = CFG.get("exp_no")  # set in each separate experiment repo


def app_dir(folder):
    """Separate repo: app is in the repo root. Combined repo: app is in its own folder."""
    return ROOT if SINGLE else os.path.join(ROOT, folder)
LLM_TIMEOUT = 15 * 60 * 1000  # 15 minutes per step (slow laptops)
VIEW = {"width": 1366, "height": 768}


# ---------- helpers ----------
def wait_ai(pg):
    """Wait until every button spinner is finished (the AI has answered)."""
    pg.wait_for_timeout(300)
    pg.wait_for_function("() => (window.__busy || 0) === 0", timeout=LLM_TIMEOUT)
    pg.wait_for_timeout(700)


def type_into(pg, sel, text):
    pg.fill(sel, "")
    pg.locator(sel).press_sequentially(text, delay=12)


def ai(fn):
    """Mark a step that needs the LLM (used by --home-only mode)."""
    fn.ai = True
    return fn


def click_wait(sel):
    @ai
    def f(pg):
        pg.click(sel)
        wait_ai(pg)
    return f


def port_open(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


# ---------- steps for each experiment ----------
# Each step: (screenshot name, action(page) or None, selector to capture or "page")

def exp1():
    def ask(text):
        @ai
        def f(pg):
            type_into(pg, "#msg", text)
            pg.click("#send")
            wait_ai(pg)
        return f
    right = "main > section:nth-of-type(2)"
    return [
        ("Home Screen", None, "page"),
        ("FAQ", ask("Where is my parcel? I want to track it"), right),
        ("Recommendation", ask("Recommend a gaming laptop under 80000"), right),
        ("Product QA", ask("Is the Samsung Galaxy S24 waterproof?"), right),
        ("Review Summary", ask("What do customers think about the OnePlus Nord CE 4?"), right),
        ("Intent Detection", None, "#card-intent"),
    ]


def exp2():
    def fill(pg):
        type_into(pg, "#topic", "Electric Vehicles in India")
        pg.select_option("#style", "Informative")
        pg.select_option("#tone", "Friendly")
        pg.fill("#audience", "Engineering students")
        pg.fill("#words", "400")
        type_into(pg, "#extra", "Include benefits, challenges and the future of EVs in India.")

    @ai
    def intent(pg):
        type_into(pg, "#ask", "suggest some catchy headings for this blog")
        pg.click("#btn-ask")
        wait_ai(pg)
    return [
        ("Home Screen", None, "page"),
        ("User Input", fill, "#card-input"),
        ("Blog Generation", click_wait("#btn-generate"), "#card-blog"),
        ("Prompt Engineering", None, "#card-prompt"),
        ("Blog Title Generation", click_wait("#btn-titles"), "#card-titles"),
        ("Summary Generation", click_wait("#btn-summary"), "#card-summary"),
        ("SEO Keywords", click_wait("#btn-seo"), "#card-seo"),
        ("Meta Description", click_wait("#btn-meta"), "#card-meta"),
        ("Blog Saved Successfully", click_wait("#btn-save"), "#card-saved"),
        ("Intent Detection", intent, "#card-ask"),
    ]


def exp3():
    def fill(pg):
        type_into(pg, "#name", "John")
        type_into(pg, "#subject", "Delivery Delay")
        type_into(pg, "#email", "My package has not arrived yet. It was supposed to come 3 days ago. Please help.")

    @ai
    def tone(pg):
        pg.click("button.tone[data-tone='Empathetic']")
        wait_ai(pg)
    return [
        ("Home Screen", None, "page"),
        ("Customer Email", fill, "#card-input"),
        ("Intent Detection", click_wait("#btn-process"), "#card-intent"),
        ("Similar Email Retrieval", None, "#card-similar"),
        ("AI Reply", None, "#card-reply"),
        ("Tone Improvement", tone, "#card-tone"),
        ("Conversation Summary", click_wait("#btn-summary"), "#card-summary"),
        ("Saved Reply", click_wait("#btn-save"), "#card-saved"),
    ]


def exp4():
    def fill(pg):
        type_into(pg, "#name", "Monick")
        pg.fill("#age", "21")
        pg.fill("#interests", "Artificial Intelligence, Python, Cloud")
        pg.select_option("#level", "Beginner")
        pg.select_option("#category", "Any")

    def feedback(pg):
        type_into(pg, "#fb", "I am more interested in Generative AI and projects than cloud certifications.")
    return [
        ("Home Screen", None, "page"),
        ("User Profile Input", fill, "#card-input"),
        ("Collected User Profile", click_wait("#btn-go"), "#card-profile"),
        ("Preference Analysis", None, "#card-pref"),
        ("Prompt Generation", None, "#card-prompt"),
        ("GPT-4 Recommendation", None, "#card-llm"),
        ("Recommendation Ranking", None, "#card-rank"),
        ("Recommendation Explanation", None, "#card-explain"),
        ("User Feedback", feedback, "#card-feedback"),
        ("Intent Detection", click_wait("#btn-fb"), "#card-feedback"),
        ("Refined Recommendations", None, "#card-refined"),
        ("Recommendation Saved Successfully", click_wait("#btn-save"), "#card-saved"),
    ]


def exp5():
    sample = os.path.join(app_dir("Exp5_Legal_Analyzer"), "samples", "employment_agreement.txt")

    def upload(pg):
        pg.set_input_files("#file", sample)
        pg.select_option("#atype", "Complete")
    return [
        ("Home Screen", None, "page"),
        ("Document Upload", upload, "#card-input"),
        ("Extracted Text", click_wait("#btn-extract"), "#card-extracted"),
        ("Preprocessing and Chunking", None, "#card-pre"),
        ("Prompt Generation", click_wait("#btn-analyze"), "#card-prompt"),
        ("Document Summary", None, "#card-summary"),
        ("Key Clauses", None, "#card-clauses"),
        ("Obligations, Payment and Dates", None, "#card-obligations"),
        ("Complete Structured Analysis", None, "#card-report"),
        ("Report Saved", click_wait("#btn-save"), "#card-saved"),
    ]


def exp6():
    def patient(pg):
        pg.fill("#age", "20")
        pg.select_option("#sex", "Female")
        pg.fill("#history", "None")

    def symptoms(pg):
        type_into(pg, "#symptoms", "I have had a fever and sore throat since yesterday. I also have a cough and feel tired.")
        pg.fill("#duration", "1 day")
        pg.select_option("#severity", "Mild")
    return [
        ("Home Screen", None, "page"),
        ("Patient Information Input", patient, "#card-input"),
        ("Symptom Input", symptoms, "#symptom-box"),
        ("Extracted Symptoms", click_wait("#btn-go"), "#card-symptoms"),
        ("Context Analysis", None, "#card-context"),
        ("Prompt Generation", None, "#card-prompt"),
        ("GPT-4 Response", None, "#card-response"),
        ("Possible Conditions", None, "#card-conditions"),
        ("Follow-up Questions", None, "#card-questions"),
        ("Medical Attention Guidance", None, "#card-safety"),
        ("Complete Structured Analysis", None, "#card-report"),
        ("Disclaimer", None, "#disclaimer"),
        ("Saved Report", click_wait("#btn-save"), "#card-saved"),
    ]


EXPS = {
    1: ("Exp1_ECommerce_Chatbot", 5001, exp1),
    2: ("Exp2_Blog_Generator", 5002, exp2),
    3: ("Exp3_Email_Assistant", 5003, exp3),
    4: ("Exp4_Recommendation_System", 5004, exp4),
    5: ("Exp5_Legal_Analyzer", 5005, exp5),
    6: ("Exp6_Medical_Assistant", 5006, exp6),
}


def slug(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")


def run_exp(p, no, home_only=False):
    folder, port, steps_fn = EXPS[no]
    out = os.path.join(SHOTS, f"exp{no}")
    os.makedirs(out, exist_ok=True)
    proc = None
    if not port_open(port):
        print(f"  starting {folder}/app.py ...")
        proc = subprocess.Popen([sys.executable, "app.py"], cwd=app_dir(folder),
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for _ in range(240):  # first start may download the embedding model
            if port_open(port):
                break
            time.sleep(0.5)
        else:
            raise RuntimeError(f"{folder} did not start. Run it manually to see the error.")
    vid_dir = os.path.join(VIDEOS, "_tmp")
    browser = p.chromium.launch(slow_mo=120)
    ctx = browser.new_context(viewport=VIEW, device_scale_factor=1.5,
                              **({} if home_only else {"record_video_dir": vid_dir, "record_video_size": VIEW}))
    pg = ctx.new_page()
    try:
        pg.goto(f"http://localhost:{port}")
        pg.wait_for_timeout(2500)
        for i, (name, action, target) in enumerate(steps_fn(), 1):
            if home_only and getattr(action, "ai", False):
                break  # stop before the first step that needs the LLM
            if action:
                action(pg)
            path = os.path.join(out, f"{i:02d}_{slug(name)}.png")
            if target == "page":
                pg.screenshot(path=path)
            else:
                loc = pg.locator(target).first
                loc.scroll_into_view_if_needed()
                pg.wait_for_timeout(600)
                loc.screenshot(path=path)
            print(f"  [ok] {name}")
        pg.wait_for_timeout(1500)
    finally:
        video = pg.video
        ctx.close()
        browser.close()
        if video and not home_only:
            os.makedirs(VIDEOS, exist_ok=True)
            final = os.path.join(VIDEOS, f"{folder}_{CFG.get('register_number', '')}.webm")
            shutil.move(video.path(), final)
            print(f"  [video] {final}")
        if proc:
            proc.terminate()


def main():
    home_only = "--home-only" in sys.argv
    wanted = [SINGLE] if SINGLE else ([int(a) for a in sys.argv[1:] if a.isdigit()] or list(EXPS))
    if not home_only:
        try:
            tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
            names = [m["name"] for m in tags.get("models", [])]
            model = os.getenv("OLLAMA_MODEL", "llama3.2")
            if not any(n.startswith(model) for n in names):
                sys.exit(f"Model {model} not found. Run:  ollama pull {model}")
        except requests.exceptions.ConnectionError:
            sys.exit("Ollama is not running. Open the Ollama app or run:  ollama serve")
    with sync_playwright() as p:
        for no in wanted:
            print(f"\n=== Experiment {no}: {EXPS[no][0]} ===")
            run_exp(p, no, home_only)
    shutil.rmtree(os.path.join(VIDEOS, "_tmp"), ignore_errors=True)
    print("\nDone. Now build the record:  python tools/build_record.py")


if __name__ == "__main__":
    main()
