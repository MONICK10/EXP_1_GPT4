"""
build_record.py - Builds the complete lab record PDF:
front page, certificate, table of contents and all 6 experiment records
(with architecture diagrams and screenshots from tools/capture.py).

Run (from the repo folder):
    python tools/build_record.py
Output:
    Separate experiment repo -> ExpN_Record_URK23CS1167.pdf
    python tools/build_record.py --front -> Front_Page_URK23CS1167.pdf
"""
import glob
import importlib.metadata as md
import json
import os
import platform
import re
import shutil
import subprocess
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (CondPageBreak, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_content import EXPERIMENTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
LOGO = os.path.join(ROOT, "docs", "karunya_header.png")
W, H = A4
CONTENT_W = W - 4.2 * cm

# ---------- styles (Times, like the college template) ----------
BASE = dict(fontName="Times-Roman", fontSize=12, leading=16)
sN = ParagraphStyle("n", **BASE, alignment=TA_JUSTIFY)
sH = ParagraphStyle("h", fontName="Times-Bold", fontSize=12.5, leading=17, spaceBefore=9, spaceAfter=4)
sC = ParagraphStyle("c", **{**BASE, "fontName": "Times-Bold"}, alignment=TA_CENTER)
sCap = ParagraphStyle("cap", fontName="Times-Italic", fontSize=10.5, leading=13, alignment=TA_CENTER, spaceAfter=10)
sCell = ParagraphStyle("cell", fontName="Times-Roman", fontSize=11, leading=14)
sCellB = ParagraphStyle("cellb", fontName="Times-Bold", fontSize=11, leading=14)
sLink = ParagraphStyle("link", **BASE)
# header-block GitHub row: smaller so a long repo URL stays on one line
sGh = ParagraphStyle("gh", fontName="Times-Roman", fontSize=10.5, leading=13, alignment=TA_CENTER)


def P(text, style=sN):
    return Paragraph(text, style)


# ---------- software versions (auto-detected on your laptop) ----------
def detect_versions():
    fb = CFG["versions_fallback"]
    v = {"Python": platform.python_version()}

    def pkg(name):
        try:
            return md.version(name)
        except md.PackageNotFoundError:
            return None

    v["Pandas"] = pkg("pandas") or fb["Pandas"]
    v["Sentence Transformers"] = pkg("sentence-transformers") or fb["Sentence Transformers"]
    v["Flask"] = pkg("flask") or fb["Flask"]

    def cmd(args, pattern):
        exe = shutil.which(args[0])
        if not exe:
            return None
        try:
            out = subprocess.run([exe] + args[1:], capture_output=True, text=True, timeout=20).stdout
            m = re.search(pattern, out)
            return m.group(1) if m else None
        except Exception:
            return None

    v["Ollama"] = cmd(["ollama", "--version"], r"(\d+\.\d+\.\d+)") or fb["Ollama"]
    v["VS Code"] = cmd(["code", "--version"], r"^(\d+\.\d+\.\d+)") or fb["VS Code"]
    return v


# ---------- page decorations ----------
def border(canvas, doc):
    canvas.saveState()
    canvas.setLineWidth(1)
    canvas.rect(1.2 * cm, 1.2 * cm, W - 2.4 * cm, H - 2.4 * cm)
    canvas.setFont("Times-Italic", 8.5)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(W - 1.6 * cm, 1.45 * cm, f"{CFG['register_number']} – {CFG['name']}")
    canvas.restoreState()


def plain(canvas, doc):
    pass


def logo(width=15 * cm):
    img = Image(LOGO)
    img.drawWidth = width
    img.drawHeight = width * img.imageHeight / img.imageWidth
    return img


# ---------- front matter ----------
def front_page():
    big = ParagraphStyle("big", fontName="Times-Bold", fontSize=15, leading=20, alignment=TA_CENTER)
    mid = ParagraphStyle("mid", fontName="Times-Bold", fontSize=13, leading=18, alignment=TA_CENTER)
    info = Table([[P(f"<b>{k}</b>", ParagraphStyle("i", **{**BASE, "fontSize": 13})), P(":"),
                   P(v, ParagraphStyle("iv", **{**BASE, "fontSize": 13}))]
                  for k, v in [("Name", CFG["name"]), ("Register Number", CFG["register_number"]),
                               ("Course Code", CFG["course_code"]), ("Course Name", CFG["course_name"])]],
                 colWidths=[4.6 * cm, 0.6 * cm, 10 * cm])
    info.setStyle(TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    return [Spacer(1, 0.6 * cm), logo(), Spacer(1, 1.6 * cm),
            P("DIVISION OF COMPUTER SCIENCE AND ENGINEERING", big), Spacer(1, 0.3 * cm),
            P("SCHOOL OF COMPUTER SCIENCE AND TECHNOLOGY", mid), Spacer(1, 2 * cm),
            P("LABORATORY RECORD", big), Spacer(1, 1 * cm),
            P(f"Academic Year {CFG['academic_year']}", mid), Spacer(1, 0.8 * cm),
            P(CFG["semester"], mid), Spacer(1, 2.2 * cm), info, Spacer(1, 2.2 * cm),
            P(CFG["record_month"], big), PageBreak()]


def certificate():
    mid = ParagraphStyle("mid", fontName="Times-Bold", fontSize=13, leading=18, alignment=TA_CENTER)
    body = ParagraphStyle("body", fontName="Times-Roman", fontSize=13, leading=24, alignment=TA_JUSTIFY,
                          firstLineIndent=1.2 * cm)
    exam = CFG["exam_date"] or "____________________"
    sign = Table([[P("<b>Faculty-in-charge Signature</b>"), P("")], [P(""), P("")],
                  [P("<b>Faculty-in-charge Name</b>"), P("")]], colWidths=[8 * cm, 7 * cm], rowHeights=[1, 1.4 * cm, 1])
    return [Spacer(1, 0.6 * cm), logo(), Spacer(1, 1 * cm),
            P("DIVISION OF COMPUTER SCIENCE AND ENGINEERING", mid), Spacer(1, 0.2 * cm),
            P("SCHOOL OF COMPUTER SCIENCE AND TECHNOLOGY", ParagraphStyle("s", parent=mid, fontSize=11.5)),
            Spacer(1, 0.6 * cm), P("LABORATORY RECORD", mid), Spacer(1, 0.4 * cm),
            P(f"Academic Year {CFG['academic_year']}", mid), Spacer(1, 1 * cm),
            P(f"Course Code: <u>{CFG['course_code']}</u>", mid), Spacer(1, 0.6 * cm),
            P(f"Course Name: <u>{CFG['course_name']}</u>", mid), Spacer(1, 0.6 * cm),
            P(f"Register No.: <u>{CFG['register_number']}</u>", mid), Spacer(1, 1.2 * cm),
            P(f"It is hereby certified that this is the bonafide record of work done by Mr. <b><u>{CFG['name']}</u></b> "
              f"during the Odd semester of the academic year {CFG['academic_year']} and submitted for the University "
              f"Practical Examination held on {exam}.", body),
            Spacer(1, 2.4 * cm), sign, PageBreak()]


def toc():
    rows = [[P("<b>#</b>", sCellB), P("<b>Date</b>", sCellB), P("<b>Name of the Exercise</b>", sCellB),
             P("<b>Marks</b>", sCellB), P("<b>Signature</b>", sCellB)]]
    for e in EXPERIMENTS:
        rows.append([P(f"{e['no']}.", sCell), P(CFG["dates"][str(e["no"])], sCell), P(e["title"], sCell), "", ""])
    t = Table(rows, colWidths=[1.1 * cm, 2.6 * cm, 8 * cm, 1.8 * cm, 2.7 * cm], rowHeights=[0.9 * cm] + [1.9 * cm] * 6)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.8, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee"))]))
    return [Spacer(1, 1 * cm), P("Table of Contents", ParagraphStyle("t", fontName="Times-Bold", fontSize=16,
                                                                     alignment=TA_CENTER, leading=22)),
            Spacer(1, 0.8 * cm), t, Spacer(1, 2.5 * cm),
            P("<b>Faculty-in-charge Signature</b>", ParagraphStyle("r", **BASE, alignment=2)), PageBreak()]


# ---------- one experiment ----------
def grid_table(head, rows, widths):
    data = [[P(f"<b>{head[0]}</b>", sCellB), P(f"<b>{head[1]}</b>", sCellB)]] + \
           [[P(a, sCell), P(b, sCell)] for a, b in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def fit_image(path, max_w, max_h):
    img = Image(path)
    r = min(max_w / img.imageWidth, max_h / img.imageHeight)
    img.drawWidth, img.drawHeight = img.imageWidth * r, img.imageHeight * r
    return img


def nice(name):
    return re.sub(r"^\d+_", "", os.path.splitext(os.path.basename(name))[0]).replace("_", " ").title() \
        .replace("Qa", "QA").replace("Faq", "FAQ").replace("Seo", "SEO").replace("Gpt 4", "GPT-4").replace("Ai ", "AI ")


def experiment(e, versions):
    n = e["no"]
    date = CFG["dates"][str(n)]
    repo = CFG["github_repo"].rstrip("/")
    gh = repo if CFG.get("exp_no") else f"{repo}/tree/main/{e['folder']}"
    # third row of the header block: the repository this experiment lives in
    gh_cell = P(f"<b>GitHub Link:</b> <link href='{gh}' color='blue'>{gh}</link>", sGh)
    head = Table([[P(f"<b>Ex. No.:{n}</b>", sC), P(f"<b>{e['short']}</b>", sC), P(f"<b>{CFG['register_number']}</b>", sC)],
                  [P(f"<b>{date}</b>", sC), "", ""],
                  [gh_cell, "", ""]],
                 colWidths=[3 * cm, 9.6 * cm, 3.8 * cm], rowHeights=[0.9 * cm, 0.9 * cm, 0.9 * cm])
    head.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.8, colors.black), ("SPAN", (1, 0), (1, 1)),
                              ("SPAN", (2, 0), (2, 1)), ("SPAN", (0, 2), (2, 2)),
                              ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    f = [Spacer(1, 0.2 * cm), head, Spacer(1, 0.3 * cm),
         P("Aim:", sH), P(e["aim"]), P("Problem Statement:", sH), P(e["problem"]),
         P("Software Requirements:", sH)]
    soft = [(k, versions[k]) for k in ("Python", "Ollama", "VS Code", "Pandas", "Sentence Transformers", "Flask")]
    soft.append(("LLM Model", CFG["llm_model"]))
    f += [grid_table(("Software", "Version"), soft, [6.5 * cm, 6.5 * cm]),
          P(f"{e['table_title']}:", sH), grid_table(e["table_head"], e["table"], [4.2 * cm, 11.6 * cm])]
    arch = os.path.join(ROOT, "docs", "architecture", f"exp{n}_architecture.png")
    f += [CondPageBreak(9 * cm), P("System Architecture:", sH), fit_image(arch, CONTENT_W - 0.6 * cm, 15 * cm),
          P(f"Fig. {n}.1 System architecture", sCap),
          P("Module Design:", sH), grid_table(("Module", "Responsibility"), e["modules"], [4.6 * cm, 11.2 * cm])]
    li = CFG["linkedin"].get(str(n)) or "&lt;add LinkedIn post link in config.json&gt;"
    f += [P("Implementation:", sH),
          P(f"&bull; GitHub Link - <link href='{gh}' color='blue'>{gh}</link>", sLink),
          P(f"&bull; LinkedIn Post Link - {li if li.startswith('&lt;') else f'<link href=\"{li}\" color=blue>{li}</link>'}",
            sLink),
          P(f"&bull; Run: <font face='Courier'>{'' if CFG.get('exp_no') else 'cd ' + e['folder'] + ' ; '}python app.py</font> &rarr; "
            f"<font face='Courier'>http://localhost:500{n}</font>", sLink),
          CondPageBreak(8 * cm), P("Output Screenshots:", sH)]
    shots = sorted(glob.glob(os.path.join(ROOT, "screenshots", f"exp{n}", "*.png")))
    if not shots:
        f.append(P("<i>Screenshots not captured yet. Run: python tools/capture.py " + str(n) + "</i>"))
    for i, s in enumerate(shots, 1):
        # small cards are not stretched: about 0.45 pt per captured pixel at most
        from reportlab.lib.utils import ImageReader
        px_w = ImageReader(s).getSize()[0]
        img = fit_image(s, min(CONTENT_W - 0.6 * cm, px_w * 0.45), 18 * cm)
        img.hAlign = "CENTER"
        frame = Table([[img]], colWidths=[img.drawWidth + 4])
        frame.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.grey), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        f.append(KeepTogether([frame, Spacer(1, 3), P(f"Fig. {n}.{i + 1} {nice(s)}", sCap)]))
    if 0 < len(shots) <= 3:
        f.append(P("<i>[Draft] The AI output screenshots are added automatically when you run "
                   f"python tools/capture.py {n} on your laptop with Ollama.</i>"))
    f += [KeepTogether([P("Result:", sH), P(e["result"])]), PageBreak()]
    return f


def main():
    versions = detect_versions()
    print("Software versions:", versions)
    single = CFG.get("exp_no")
    front_only = "--front" in sys.argv
    if single:
        out = os.path.join(ROOT, f"Exp{single}_Record_{CFG['register_number']}.pdf")
    elif front_only:
        out = os.path.join(ROOT, f"Front_Page_{CFG['register_number']}.pdf")
    else:
        out = os.path.join(ROOT, f"Lab_Record_{CFG['register_number']}_{CFG['name'].replace(' ', '_')}.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2.1 * cm, rightMargin=2.1 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.9 * cm, title=f"Lab Record - {CFG['course_name']}",
                            author=f"{CFG['name']} ({CFG['register_number']})")
    if single:  # separate experiment repo: only this record
        story = experiment(next(e for e in EXPERIMENTS if e["no"] == single), versions)
        n_front = 0
    elif front_only:  # front page + certificate + contents only
        story = front_page() + certificate() + toc()
        n_front = 3
    else:
        story = front_page() + certificate() + toc()
        for e in EXPERIMENTS:
            story += experiment(e, versions)
        n_front = 3
    story = story[:-1]  # drop last page break

    def on_page(canvas, d):
        (plain if canvas.getPageNumber() <= n_front else border)(canvas, d)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("PDF created:", out)


if __name__ == "__main__":
    main()
