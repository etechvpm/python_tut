#!/usr/bin/env python3
"""
Generate the visual assets for Module 01 - Introduction to Python.

Uses the shared design system in tools/figlib.py.

Run:  python3 tools/make_figures.py
Out:  assets/01_intro/*.png + title_card.jpg
"""

import math
import os

from figlib import *          # design system: colours, C canvas, helpers
from figlib import S, _fonts   # noqa: F401  (S + font cache used locally)
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "01_intro")


# --------------------------------------------------------------------------
# figure 1 - timeline
# --------------------------------------------------------------------------
def fig_timeline():
    items = [
        ("1989", "Project begins", "Guido van Rossum starts Python at CWI, Amsterdam."),
        ("1991", "First public release", "Python 0.9.0 is posted to a Usenet newsgroup."),
        ("1994", "Python 1.0", "The language picks up real users and libraries."),
        ("2000", "Python 2.0", "List comprehensions and proper garbage collection."),
        ("2008", "Python 3.0", "A major redesign: cleaner, but breaks compatibility."),
        ("2018", "New governance", "Guido steps down after 28 years as BDFL."),
        ("2020", "Python 2 dies", "End of life: no more fixes, ever."),
        ("2025", "Python 3.14", "Free-threading, t-strings, multiple interpreters."),
        ("2026", "Today", "#1 on the TIOBE index; 3.14.x is the stable line."),
    ]
    accents = [NAVY, NAVY, BLUE, BLUE, BLUE, SLATEG, SLATEG, GOLD, GOLD]

    W = 1400
    x0, x1 = 118, 1292
    n = len(items)
    step = (x1 - x0) / (n - 1)
    colw = 172
    top_off, bot_off = 56, 66      # distance from axis to the date baseline

    # decide which side each card goes on (fewer lines wins)
    geo = []
    for date, title, desc in items:
        tl = wrap(title, 13.5, colw, "b")
        dl = wrap(desc, 11.5, colw)
        block = len(tl) * 17 + 5 + len(dl) * 15
        geo.append((tl, dl, block))

    max_top_blk = max_bot_blk = 0
    sides = []
    run_top = run_bot = 0
    for tl, dl, block in geo:
        up = run_top <= run_bot
        sides.append(up)
        if up:
            run_top += 1
            max_top_blk = max(max_top_blk, block)
        else:
            run_bot += 1
            max_bot_blk = max(max_bot_blk, block)

    head_h = 170
    axis_y = head_h + 50 + max_top_blk + 30
    H = int(axis_y + bot_off + 34 + max_bot_blk + 78)

    c = C(W, H)
    c.eyebrow(80, 52, "TIMELINE")
    c.text(80, 80, "35+ years of Python", 34, NAVY, "b")
    c.text(80, 126, "From a Christmas holiday project in Amsterdam to the world's "
                    "most-used programming language.", 15, SLATE)

    c.hgrad(x0, axis_y - 2, x1 - x0, 4, NAVY, GOLD)

    for i, (date, title, desc) in enumerate(items):
        x = x0 + i * step
        acc = accents[i]
        up = sides[i]
        tl, dl, _ = geo[i]
        c.circle(x, axis_y, 17, fill=acc, alpha=26)
        c.circle(x, axis_y, 8.5, fill=WHITE, outline=acc, width=3)
        if up:
            c.line(x, axis_y - 20, x, axis_y - top_off + 20, LINE, 2)
            yb = axis_y - top_off
            c.text(x, yb, date, 17, acc, "b", "ma")
            y = yb - 26
            for k in range(len(tl) - 1, -1, -1):
                c.text(x, y - (len(tl) - 1 - k) * 17, tl[k], 13.5, NAVY, "b", "ma")
            y -= (len(tl) - 1) * 17 + 20
            for k in range(len(dl) - 1, -1, -1):
                c.text(x, y - (len(dl) - 1 - k) * 15, dl[k], 11.5, MUTED, "r", "ma")
        else:
            c.line(x, axis_y + 20, x, axis_y + bot_off - 26, LINE, 2)
            yb = axis_y + bot_off
            c.text(x, yb, date, 17, acc, "b", "ma")
            y = yb + 22
            for k, ln in enumerate(tl):
                c.text(x, y + k * 17, ln, 13.5, NAVY, "b", "ma")
            y += len(tl) * 17 + 5
            for k, ln in enumerate(dl):
                c.text(x, y + k * 15, ln, 11.5, MUTED, "r", "ma")

    c.rr(80, H - 66, W - 160, 40, 12, fill=PANEL)
    c.text(104, H - 46, "Python is developed in the open: anyone can propose changes "
                        "through PEPs (Python Enhancement Proposals), reviewed by the community.",
           13, SLATE, "r", "lm")
    c.save("fig1_timeline.png", OUT)


# --------------------------------------------------------------------------
# figure 2 - version numbers + support lifecycle
# --------------------------------------------------------------------------
def fig_versioning():
    W, H = 1400, 968
    c = C(W, H)
    c.eyebrow(80, 52, "VERSION NUMBERS")
    c.text(80, 80, "How to read Python 3.14.7", 34, NAVY, "b")
    c.text(80, 126, "Every Python release uses the same three-part numbering.",
           15, SLATE)

    size = 76
    parts = [("3", NAVY, "MAJOR"), (".", None, None), ("14", BLUE, "MINOR"),
             (".", None, None), ("7", GOLD, "MICRO")]
    total = sum(TWL(p, size, "mb") for p, _, _ in parts)
    x = (W - total) / 2
    digit_y = 236
    centers = []
    for p, col, lab in parts:
        w = TWL(p, size, "mb")
        if lab and p != ".":
            centers.append((x + w / 2, col, lab))
        c.text(x, digit_y, p, size, col or FAINT, "mb")
        x += w

    for cx, col, lab in centers:
        c.line(cx, digit_y + 84, cx, digit_y + 102, col, 2, alpha=120)
        c.text(cx, digit_y + 106, lab, 13, col, "b", "ma")

    cards = [
        ("Changes almost never.",
         "One major version only since 2008: Python 3. The 2.x line was retired in 2020."),
        ("One every October.",
         "All new features arrive here: 3.11, 3.12, 3.13, 3.14 and 3.15 this month."),
        ("Fixes only, always safe.",
         "Bug and security patches. Going from 3.14.7 to 3.14.8 never breaks your code."),
    ]
    cw, gap = 380, 50
    cx0 = (W - (3 * cw + 2 * gap)) / 2
    card_y, card_h = 400, 172
    for i, (sub, desc) in enumerate(cards):
        acc = centers[i][1]
        tint = [BLUE_XL, GOLD_XL, TEAL_L][i]
        cxx = cx0 + i * (cw + gap)
        c.card(cxx, card_y, cw, card_h, 18)
        c.rr(cxx, card_y, cw, 7, 3.5, fill=acc)
        c.rr(cxx + 26, card_y + 28, 96, 30, 15, fill=tint)
        c.text(cxx + 74, card_y + 43, centers[i][2], 13, acc, "b", "mm")
        c.text(cxx + 134, card_y + 43, sub, 13.5, MUTED, "r", "lm")
        c.para(cxx + 26, card_y + 84, desc, 13.5, SLATE, maxw=cw - 52, lh=1.55)

    # ---- support lifecycle strip
    sec_y = 668
    c.text(80, sec_y, "Support lifecycle of a Python version", 21, NAVY, "b")
    c.text(80, sec_y + 30, "Each release gets about five years: two years of bug "
                           "fixes, then three more of security fixes.", 13.5, MUTED)

    bar_y, bar_h = sec_y + 82, 46
    bx0, bx1 = 130, 1270
    mid = bx0 + (bx1 - bx0) * (2 / 5)
    c.rr(bx0, bar_y, mid - bx0, bar_h, 0, fill=BLUE)
    c.rr(mid, bar_y, bx1 - mid, bar_h, 0, fill=GOLD_L)
    c.text((bx0 + mid) / 2, bar_y + bar_h / 2, "Bug fixes  \u00b7  new features",
           14.5, WHITE, "b", "mm")
    c.text((mid + bx1) / 2, bar_y + bar_h / 2, "Security fixes only",
           14.5, GOLD, "b", "mm")
    for xx, col in ((bx0, BLUE), (bx1, GOLD)):
        c.d.rectangle([(xx - 1.5) * S, bar_y * S, (xx + 1.5) * S,
                       (bar_y + bar_h) * S], fill=hex2rgb(col) + (255,))

    ticks = [(bx0, "Release", "3.14 \u2192 Oct 2025", "la"),
             (mid, "Year 2", "features stop \u2192 Oct 2027", "ma"),
             (bx1, "Year 5 \u2014 End of life", "3.14 \u2192 Oct 2030", "ra")]
    for tx, t1, t2, an in ticks:
        c.line(tx, bar_y + bar_h, tx, bar_y + bar_h + 14, LINE, 2)
        c.text(tx, bar_y + bar_h + 22, t1, 14, NAVY, "b", an)
        c.text(tx, bar_y + bar_h + 42, t2, 12.5, MUTED, "r", an)

    pill_y = H - 78
    c.rr(80, pill_y, W - 160, 52, 14, fill=BLUE_L)
    c.info_icon(122, pill_y + 26, 13, NAVY)
    c.text(148, pill_y + 26, 'If a tutorial shows  print "hello"  without parentheses, '
                             "it is Python 2 \u2014 more than a decade out of date.",
           14, NAVY, "r", "lm")
    c.save("fig2_versioning.png", OUT)


# --------------------------------------------------------------------------
# figure 3 - applications
# --------------------------------------------------------------------------
def fig_applications():
    W = 1400
    domains = [
        ("AI", "AI & Machine Learning", BLUE, BLUE_XL, True,
         "Training models, deep learning, LLMs and AI agents. The fastest-growing use of Python today."),
        ("DATA", "Data Science & Analytics", TEAL, TEAL_L, False,
         "Cleaning data, statistics, charts and business dashboards."),
        ("WEB", "Web & API Backends", PURPLE, PURPLE_L, False,
         "The server side of products. Used by Instagram, Spotify, Reddit and Dropbox."),
        ("AUTO", "Automation & Scripting", GOLD, GOLD_L, False,
         "Bulk file work, report generation, scheduling and IT operations."),
        ("SCI", "Scientific Computing", GREEN, GREEN_L, False,
         "Research, simulations and analysis \u2014 NASA, CERN and universities."),
        ("FIN", "Finance & FinTech", NAVY, PANEL, False,
         "Trading systems, risk models and banking back-office tooling."),
        ("SEC", "Cybersecurity", RED, RED_L, False,
         "Penetration testing, scanning and security tooling."),
        ("QA", "Testing & QA", SKY, SKY_L, False,
         "Automated checks that software still works after every change."),
        ("ETL", "Data Engineering", BLUE, BLUE_XL, False,
         "Pipelines that move and transform data between systems."),
        ("GUI", "Desktop Apps", SLATEG, SLATEG_L, False,
         "Cross-platform desktop tools with Tkinter, PyQt or Flet."),
        ("EDU", "Education", PURPLE, PURPLE_L, False,
         "The most widely taught first language at schools and universities."),
        ("IOT", "Embedded & IoT", TEAL, TEAL_L, False,
         "Raspberry Pi, MicroPython and small connected devices."),
    ]
    cols, cwid, chi, gx, gy = 4, 318, 200, 24, 24
    gx0 = (W - (cols * cwid + (cols - 1) * gx)) / 2
    gy0 = 190
    rows = math.ceil(len(domains) / cols)
    H = int(gy0 + rows * chi + (rows - 1) * gy + 96)

    c = C(W, H)
    c.eyebrow(80, 52, "WHERE PYTHON IS USED")
    c.text(80, 80, "One language, many industries", 34, NAVY, "b")
    c.text(80, 126, "The same skills transfer across all of these areas \u2014 "
                    "you are learning one language, not ten.", 15, SLATE)

    for i, (badge, title, acc, tint, star, desc) in enumerate(domains):
        r, col = divmod(i, cols)
        x = gx0 + col * (cwid + gx)
        y = gy0 + r * (chi + gy)
        c.card(x, y, cwid, chi, 18)
        c.rr(x, y, cwid, 6, 3, fill=acc)
        c.circle(x + 52, y + 52, 24, fill=tint)
        c.text(x + 52, y + 52, badge, fit_size(badge, 13.5, 42), acc, "b", "mm")
        if star:
            ch = 22
            lbl = "\u2605 TOP GROWTH"
            cwid_ch = 20 + TWL(lbl, 10.5, "b")
            c.rr(x + cwid - 24 - cwid_ch, y + 30, cwid_ch, ch, ch / 2, fill=GOLD_XL)
            c.text(x + cwid - 24 - cwid_ch / 2, y + 30 + ch / 2, lbl, 10.5, GOLD,
                   "b", "mm")
        ts = fit_size(title, 15.5, cwid - 48)
        c.text(x + 24, y + 100, title, ts, NAVY, "b")
        c.para(x + 24, y + 128, desc, 12.5, MUTED, maxw=cwid - 48, lh=1.5)

    c.rr(80, H - 72, W - 160, 46, 12, fill=PANEL)
    c.text(W / 2, H - 49, "Honest trade-off: pure Python is slower than C++ or Java \u2014 but in AI "
                          "and data work the heavy maths runs in C/C++ libraries underneath, "
                          "with Python as the control panel.", 13, SLATE, "r", "mm")
    c.save("fig3_applications.png", OUT)


# --------------------------------------------------------------------------
# figure 4 - ecosystem map
# --------------------------------------------------------------------------
def fig_ecosystem():
    W = 1400
    cats = [
        ("Web Development", BLUE, BLUE_XL,
         [("Django", 1), ("FastAPI", 1), ("Flask", 0), ("Django REST Framework", 0),
          ("Litestar", 0), ("Tornado", 0), ("Bottle", 0)]),
        ("Data & Visualization", TEAL, TEAL_L,
         [("NumPy", 1), ("pandas", 1), ("Matplotlib", 1), ("Polars", 0),
          ("SciPy", 0), ("Seaborn", 0), ("Plotly", 0), ("Jupyter", 0)]),
        ("AI & Machine Learning", PURPLE, PURPLE_L,
         [("PyTorch", 1), ("scikit-learn", 1), ("TensorFlow", 0), ("Keras", 0),
          ("Hugging Face", 0), ("LangChain", 0), ("OpenCV", 0), ("XGBoost", 0)]),
        ("Automation & Scraping", GOLD, GOLD_L,
         [("Requests", 1), ("BeautifulSoup", 0), ("Scrapy", 0), ("Selenium", 0),
          ("Playwright", 0), ("Airflow", 0), ("Ansible", 0), ("PyAutoGUI", 0)]),
        ("Testing & Quality", GREEN, GREEN_L,
         [("pytest", 1), ("unittest", 0), ("Robot Framework", 0), ("Ruff", 0),
          ("mypy", 0)]),
        ("Databases & Tasks", SKY, SKY_L,
         [("SQLAlchemy", 1), ("SQLModel", 0), ("Alembic", 0), ("Celery", 0),
          ("Redis", 0), ("psycopg", 0)]),
        ("Desktop & Games", SLATEG, SLATEG_L,
         [("Tkinter", 1), ("PyQt / PySide", 0), ("Pygame", 0), ("Pillow", 0),
          ("Kivy", 0), ("Flet", 0)]),
        ("Everyday Glue", NAVY, PANEL,
         [("Pydantic", 1), ("Rich", 0), ("Typer", 0), ("asyncio", 0), ("httpx", 0)]),
    ]

    label_w, chip_h, chip_vgap = 268, 40, 12
    area_x = 92 + label_w + 44
    area_w = W - area_x - 92

    layout, total_h = [], 0
    for name, acc, tint, chips in cats:
        rows, cur, cur_w = [], [], 0.0
        for label, star in chips:
            w = 32 + TWL(label, 14.5, "b") + (TWL("\u2605 ", 14.5, "b") if star else 0)
            if cur and cur_w + 12 + w > area_w:
                rows.append(cur)
                cur, cur_w = [], 0.0
            cur.append((label, star, w))
            cur_w += w + (12 if len(cur) > 1 else 0)
        if cur:
            rows.append(cur)
        block_h = max(len(rows) * chip_h + (len(rows) - 1) * chip_vgap, 56)
        layout.append((name, acc, tint, rows, block_h))
        total_h += block_h + 30

    H = int(250 + total_h + 30)
    c = C(W, H)
    c.eyebrow(92, 52, "ECOSYSTEM MAP")
    c.text(92, 80, "Frameworks & libraries you will hear about", 34, NAVY, "b")
    c.text(92, 126, "A map, not a checklist \u2014 you will not touch most of this "
                    "for months. Everything installs free from PyPI with  pip install <name>.",
           15, SLATE)

    y = 200
    for name, acc, tint, rows, block_h in layout:
        c.text(92, y + 12, name, 15.5, NAVY, "b")
        c.text(92, y + 36, f"{sum(len(r) for r in rows)} tools", 11.5, FAINT)
        c.d.rectangle([(92 + label_w + 10) * S, y * S, (92 + label_w + 14) * S,
                       (y + block_h) * S], fill=hex2rgb(acc) + (255,))
        for ri, row in enumerate(rows):
            cx = area_x
            cy = y + ri * (chip_h + chip_vgap)
            for label, star, w in row:
                c.chip(cx, cy, label, tint, NAVY, dot=acc, star=bool(star),
                       size=14.5, pad=15, h=chip_h)
                cx += w + 12
        y += block_h + 30

    c.rr(92, H - 46, W - 184, 30, 15, fill=PANEL)
    c.text(120, H - 31, "\u2605 = the most widely used option in its category today (2026)",
           12.5, SLATE, "r", "lm")
    c.save("fig4_ecosystem.png", OUT)


# --------------------------------------------------------------------------
# figure 5 - by the numbers
# --------------------------------------------------------------------------
def fig_numbers():
    W, H = 1400, 300
    c = C(W, H)
    stats = [
        ("#1", BLUE, "Rank on the TIOBE index, September 2026"),
        ("35+", GOLD, "Years since the first public release (1991)"),
        ("3.14.x", NAVY, "Current stable version; 3.14.8 is the latest patch"),
        ("5", TEAL, "Years of support per release: 2 bug fixes + 3 security"),
        ("500K+", PURPLE, "Packages on PyPI, installed with a single command"),
    ]
    n = len(stats)
    cwid, gap = 248, 20
    x0 = (W - (n * cwid + (n - 1) * gap)) / 2
    for i, (val, acc, label) in enumerate(stats):
        x = x0 + i * (cwid + gap)
        c.card(x, 46, cwid, 208, 18)
        c.rr(x, 46, cwid, 6, 3, fill=acc)
        c.text(x + cwid / 2, 118, val, 42, acc, "b", "mm")
        lines = wrap(label, 13, cwid - 44)
        for k, ln in enumerate(lines):
            c.text(x + cwid / 2, 160 + k * 20, ln, 13, MUTED, "r", "ma")
    c.save("fig5_numbers.png", OUT)


# --------------------------------------------------------------------------
# title card
# --------------------------------------------------------------------------
def fig_session_plan():
    rows = [
        ("Opening & objectives", 3, BLUE),
        ("1. What Python is", 5, BLUE),
        ("2. Origins of Python", 6, PURPLE),
        ("3. Versions & lifecycle", 7, PURPLE),
        ("4. Where Python is used", 8, TEAL),
        ("5. The ecosystem", 8, GOLD),
        ("6. Python by the numbers", 2, GOLD),
        ("7-8. Takeaways & knowledge check", 6, GREEN),
    ]
    total = sum(m for _, m, _ in rows)
    W, H = 1340, 700
    c = C(W, H)
    c.eyebrow(90, 52, "TRAINER NOTES")
    c.text(90, 80, "Session plan at a glance", 32, NAVY, "b")
    c.text(90, 124, f"A {total}-minute module. Adjust the two optional sections first "
                    "if your slot is shorter or longer.", 14.5, SLATE)

    lx, bx0, bx1 = 90, 470, 1200
    y = 182
    bar_h, gap = 34, 18
    for label, mins, acc in rows:
        c.text(lx, y + bar_h / 2, label, 14.5, NAVY, "r", "lm")
        w = (bx1 - bx0) * mins / max(m for _, m, _ in rows)
        c.rr(bx0, y, w, bar_h, 8, fill=acc)
        lab = f"{mins} min"
        if w > 90:
            c.text(bx0 + w - 16, y + bar_h / 2, lab, 13.5, WHITE, "b", "rm")
        else:
            c.text(bx0 + w + 14, y + bar_h / 2, lab, 13.5, acc, "b", "lm")
        y += bar_h + gap

    c.line(bx0, y + 8, bx1, y + 8, LINE, 2)
    c.text(bx1, y + 30, f"Total: {total} minutes", 15.5, NAVY, "b", "ra")
    c.text(bx0, y + 30, "Bars are scaled to the longest section (8 min).",
           12.5, MUTED, "r", "la")

    c.rr(90, H - 84, W - 180, 52, 14, fill=BLUE_XL)
    c.text(W / 2, H - 58, "30-minute version: drop section 6 and the glossary; keep 1\u20133 and 5.      "
                          "60-minute version: add a live demo of running a .py file.",
           13, NAVY, "r", "mm")
    c.save("fig6_session_plan.png", OUT)


def title_card():
    """Light corporate cover: soft blue gradient, mock code window, navy type."""
    W, H = 1400, 700
    c = C(W, H, bg="#FFFFFF")

    # background gradient
    for i in range(H):
        t = i / (H - 1)
        col = tuple(int(hex2rgb("#FFFFFF")[k] + (hex2rgb("#E8F1FE")[k] -
                     hex2rgb("#FFFFFF")[k]) * t ** 1.35) for k in range(3))
        c.d.rectangle([0, i * S, W * S, (i + 1) * S], fill=col + (255,))

    # soft decorative shapes on the right
    c.circle(1290, 60, 250, fill=BLUE_L, alpha=110)
    c.circle(1390, 660, 210, fill=GOLD_L, alpha=110)
    c.circle(1120, 640, 120, fill=BLUE_L, alpha=70)

    # ---- mock code window
    win_x, win_y, win_w, win_h = 742, 168, 566, 386
    c.card(win_x, win_y, win_w, win_h, 20, fill=WHITE, outline="#D8E3F3", shadow=True)
    c.d.rounded_rectangle([win_x * S, win_y * S, (win_x + win_w) * S,
                           (win_y + 54) * S], radius=20 * S,
                          fill=hex2rgb("#F7FAFF") + (255,))
    c.d.rectangle([win_x * S, (win_y + 40) * S, (win_x + win_w) * S,
                   (win_y + 54) * S], fill=hex2rgb("#F7FAFF") + (255,))
    c.line(win_x, win_y + 54, win_x + win_w, win_y + 54, "#E2E8F0", 1.5)
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        c.circle(win_x + 30 + i * 22, win_y + 27, 6.5, fill=col)
    c.text(win_x + 104, win_y + 27, "hello.py", 13, MUTED, "m", "lm")
    # run button
    c.rr(win_x + win_w - 104, win_y + 14, 80, 27, 13.5, fill=GREEN_L)
    c.text(win_x + win_w - 64, win_y + 27.5, "Run", 12.5, GREEN, "b", "mm")

    lines = [
        ("1", [("# hello.py", MUTED)]),
        ("2", []),
        ("3", [("print", BLUE), ("(", INK), ('"Hello, Python!"', "#B45309"),
               (")", INK)]),
        ("4", []),
        ("5", [("# that's it - Python just ran it", MUTED)]),
    ]
    ly = win_y + 92
    for num, parts in lines:
        c.text(win_x + 44, ly, num, 13, "#C2CCDA", "m", "rm")
        tx = win_x + 66
        for txt, col in parts:
            c.text(tx, ly, txt, 15, col, "mb" if txt == "print" else "m", "lm")
            tx += TWL(txt, 15, "mb" if txt == "print" else "m")
        ly += 42
    c.line(win_x + 58, win_y + 76, win_x + 58, win_y + win_h - 52, "#EDF2F8", 1.5)

    # ---- left content
    c.text(96, 274, track("CORPORATE TRAINING  \u00b7  MODULE 01"), 12.5, GOLD, "b")
    tsize = fit_size("Introduction to Python", 50, 600)
    c.text(96, 302, "Introduction to Python", tsize, NAVY, "b")
    c.rr(96, 388, 84, 5, 2.5, fill=GOLD)
    c.text(96, 414, "Origins  \u00b7  Versions  \u00b7  Applications  \u00b7  Ecosystem",
           16.5, SLATE)
    c.text(96, 470, "Python Foundation Series", 14, NAVY, "b")
    c.text(96, 494, "Prepared for new joiners  |  45-minute module  |  2026",
           13, MUTED)

    # footnote strip
    c.rr(0, H - 8, W, 8, 0, fill=NAVY)
    c.rr(0, H - 8, 300, 8, 0, fill=GOLD)

    path = os.path.join(OUT, "title_card.jpg")
    c.img.convert("RGB").resize((W, H), Image.LANCZOS).save(
        path, "JPEG", quality=90, optimize=True)
    print(f"  title_card.jpg  {W}x{H}  {os.path.getsize(path) / 1024:.0f} KB")


if __name__ == "__main__":
    print("Generating Module 01 visual assets ->", OUT)
    fig_timeline()
    fig_versioning()
    fig_applications()
    fig_ecosystem()
    fig_numbers()
    fig_session_plan()
    title_card()
    print("Done.")
