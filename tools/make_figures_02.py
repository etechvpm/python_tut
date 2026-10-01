#!/usr/bin/env python3
"""
Generate the visual assets for Module 02 - How Python Runs
(interpreted languages, bytecode compilation and the PVM).

Uses the shared design system in tools/figlib.py.

Run:  python3 tools/make_figures_02.py
Out:  assets/02_how_python_runs/*.png + title_card.jpg
"""

import os

from figlib import *                      # design system: colours, C, helpers
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "02_how_python_runs")


# --------------------------------------------------------------------------
# figure 1 - two paths: compiled vs interpreted
# --------------------------------------------------------------------------
def fig_two_paths():
    W, H = 1400, 660
    c = C(W, H)
    c.eyebrow(80, 52, "TWO FAMILIES OF LANGUAGES")
    c.text(80, 80, "Two ways to run a program", 34, NAVY, "b")
    c.text(80, 126, "The difference is when the translation happens \u2014 and what "
                    "you have to ship to the machine that runs it.", 15, SLATE)

    def lane(y, title, tint, accent, boxes, note, tag):
        c.card(80, y, W - 160, 176, 18)
        c.rr(80, y, 6, 176, 3, fill=accent)
        c.rr(104, y + 18, TWL(title, 13, "b") + 30, 28, 14, fill=tint)
        c.text(104 + (TWL(title, 13, "b") + 30) / 2, y + 32, title, 13, accent,
               "b", "mm")
        c.text(104 + TWL(title, 13, "b") + 44, y + 32, tag, 12.5, FAINT, "r", "lm")
        # flow
        bx = 116
        for i, (label, sub, bcol, bw) in enumerate(boxes):
            c.rr(bx, y + 60, bw, 58, 12, fill=bcol)
            bold = sub == ""
            c.text(bx + bw / 2, y + (89 if bold else 82), label,
                   14 if bw < 240 else 13.5, WHITE, "b", "mm")
            if not bold:
                c.text(bx + bw / 2, y + 101, sub, 11.5, WHITE, "r", "mm")
            bx += bw
            if i < len(boxes) - 1:
                c.arrow(bx + 12, y + 89, bx + 46, y + 89, FAINT, 2, 8)
                bx += 58
        c.text(116, y + 142, note, 13, MUTED, "r", "lm")

    lane(178, "COMPILED", BLUE_XL, BLUE, [
        ("hello.c", "source code", NAVY, 150),
        ("Compiler", "translates once", BLUE, 176),
        ("hello.exe", "machine code", BLUE, 168),
        ("CPU", "runs directly", SLATEG, 130),
    ], "Translate once, ahead of time. The executable carries the machine code, so the "
       "target machine needs neither the compiler nor the language installed.",
        "C, C++, Go, Rust")

    lane(382, "INTERPRETED", GOLD_XL, GOLD, [
        ("hello.py", "source code", NAVY, 150),
        ("Python interpreter", "translates every run", GOLD, 238),
        ("Output", "\u2192 Hello, Python!", GREEN, 168),
    ], "Translate as you go, every run. You ship the source file itself, so the "
       "interpreter must be installed on every machine that runs it.",
        "Python, JavaScript, Ruby")

    c.rr(80, H - 74, W - 160, 46, 12, fill=PANEL)
    c.text(W / 2, H - 51, "Practical consequence:  a C++ program needs its .exe.   "
                          "A Python program needs Python \u2014 which is why we ship "
                          "containers and virtual environments, not loose .py files.",
           13, SLATE, "r", "mm")
    c.save("fig1_two_paths.png", OUT)


# --------------------------------------------------------------------------
# figure 2 - the Python execution pipeline
# --------------------------------------------------------------------------
def fig_pipeline():
    W, H = 1400, 672
    c = C(W, H)
    c.eyebrow(80, 52, "UNDER THE HOOD")
    c.text(80, 80, "What actually happens when you run python hello.py", 32, NAVY, "b")
    c.text(80, 126, "One command at the terminal, six steps inside the interpreter "
                    "\u2014 and it all happens automatically.", 15, SLATE)

    stages = [
        ("Source code", "hello.py", NAVY, NAVY),
        ("Lexer", "reads characters", BLUE, BLUE),
        ("Parser", "builds an AST", BLUE, BLUE),
        ("Compiler", "emits bytecode", BLUE, BLUE),
        ("PVM", "executes it", PURPLE, PURPLE),
        ("Output", "Hello, Python!", GREEN, GREEN),
    ]
    y = 208
    bw, bh, gap = 176, 122, 34
    x0 = 90
    cx = x0
    for i, (name, sub, col, _) in enumerate(stages):
        c.card(cx, y, bw, bh, 16)
        c.rr(cx, y, bw, 6, 3, fill=col)
        c.circle(cx + 28, y + 34, 13, fill=col)
        c.text(cx + 28, y + 34, str(i + 1), 13, WHITE, "b", "mm")
        ts = fit_size(name, 16.5, bw - 56, "b", 12)
        c.text(cx + 50, y + 26, name, ts, NAVY, "b", "lm")
        c.para(cx + 22, y + 60, sub, 12.5, MUTED, maxw=bw - 44, lh=1.45)
        if i < len(stages) - 1:
            c.chevron(cx + bw + gap / 2, y + bh / 2, 11, 20, FAINT, 2.5)
        cx += bw + gap

    # phase bands
    band_y = y + bh + 34
    c.band(x0 + bw + gap, band_y, 3 * bw + 2 * gap, 34,
           "COMPILE PHASE  \u00b7  automatic, microseconds, nothing runs yet",
           BLUE, BLUE_XL, 12.5)
    c.band(x0 + 4 * (bw + gap), band_y, bw, 34,
           "RUNTIME", PURPLE, PURPLE_L, 12.5)

    # cache branch
    cache_y = band_y + 55
    kw = 340
    cache_x = x0 + 3 * (bw + gap) + bw / 2 - kw / 2     # centred under "Compiler"
    c.line(cache_x + kw / 2, y + bh + 6, cache_x + kw / 2, cache_y - 8, GOLD, 1.5)
    c.card(cache_x, cache_y, kw, 104, 14, fill=GOLD_XL, outline="#F3DFAE",
           shadow=False)
    c.circle(cache_x + 32, cache_y + 30, 13, fill=GOLD)
    c.text(cache_x + 32, cache_y + 30, "\u21bb", 14, WHITE, "b", "mm")
    c.text(cache_x + 54, cache_y + 22, "__pycache__/hello.cpython-314.pyc", 12.5,
           NAVY, "mb", "lm")
    c.text(cache_x + 54, cache_y + 42, "Bytecode is cached on disk.", 12, MUTED,
           "r", "lm")
    c.text(cache_x + 54, cache_y + 60, "Next run skips steps 2-4: faster startup.",
           12, MUTED, "r", "lm")
    c.text(cache_x + 54, cache_y + 78, "Not an executable \u2014 only Python can run it.",
           12, FAINT, "r", "lm")

    c.rr(80, H - 74, W - 160, 46, 12, fill=PANEL)
    c.text(W / 2, H - 51, "Your source code is never executed directly. Steps 2-4 turn "
                          "it into bytecode; step 5 executes that bytecode.",
           13.5, SLATE, "r", "mm")
    c.save("fig2_pipeline.png", OUT)


# --------------------------------------------------------------------------
# figure 3 - what you write vs what the PVM runs
# --------------------------------------------------------------------------
def fig_code_vs_bytecode():
    W, H = 600, 736
    c = C(W, H)
    c.eyebrow(60, 46, "SAME PROGRAM, TWO LEVELS")
    c.text(60, 74, "Your code vs the bytecode", 28, NAVY, "b")
    c.text(60, 114, "Both halves describe the same three lines.", 14, SLATE)

    # left panel - source
    c.card(60, 162, 480, 230, 16)
    c.rr(60, 162, 480, 46, 16, fill=BLUE_XL)
    c.d.rectangle([60 * 2, 190 * 2, 540 * 2, 208 * 2], fill=hex2rgb(BLUE_XL) + (255,))
    c.text(84, 185, "What you write", 14, BLUE, "b", "lm")
    c.text(516, 185, "hello.py", 12.5, FAINT, "m", "rm")
    src = [("1", "x = 5"), ("2", "y = 10"), ("3", "print(x + y)")]
    ly = 240
    for n, code in src:
        c.text(92, ly, n, 13, "#C2CCDA", "m", "rm")
        c.text(112, ly, code, 15.5, INK, "m", "lm")
        ly += 38
    c.text(84, 358, "3 lines \u00b7 readable by humans", 12.5, MUTED, "r", "lm")

    # right panel - bytecode
    c.card(60, 424, 480, 226, 16)
    c.rr(60, 424, 480, 44, 16, fill=PURPLE_L)
    c.d.rectangle([60 * 2, 450 * 2, 540 * 2, 468 * 2], fill=hex2rgb(PURPLE_L) + (255,))
    c.text(84, 446, "What the PVM runs", 14, PURPLE, "b", "lm")
    c.text(516, 446, "dis output", 12.5, FAINT, "m", "rm")
    bc = [
        ("1", "LOAD_CONST", "5"),
        ("", "STORE_NAME", "x"),
        ("2", "LOAD_CONST", "10"),
        ("", "STORE_NAME", "y"),
        ("3", "LOAD_NAME", "print"),
        ("", "LOAD_NAME", "x"),
        ("", "LOAD_NAME", "y"),
        ("", "BINARY_OP", "+"),
    ]
    ly = 492
    for n, op, arg in bc:
        c.text(92, ly, n, 12, "#C2CCDA", "m", "rm")
        c.text(112, ly, op, 12.5, PURPLE, "mb", "lm")
        c.text(112 + 108, ly, arg, 12.5, INK, "m", "lm")
        ly += 16.5

    c.rr(60, H - 54, 480, 42, 12, fill=PANEL)
    c.text(W / 2, H - 33, "Platform-independent \u2014 any Python 3.14 can run it.",
           12.5, SLATE, "r", "mm")
    c.save("fig3_code_vs_bytecode.png", OUT)


# --------------------------------------------------------------------------
# figure 4 - compiled vs interpreted vs Python
# --------------------------------------------------------------------------
def fig_comparison():
    W, H = 1400, 800
    c = C(W, H)
    c.eyebrow(80, 52, "SIDE BY SIDE")
    c.text(80, 80, "Compiled, interpreted \u2014 and where Python sits", 32, NAVY, "b")
    c.text(80, 124, "Python is a hybrid: it compiles to bytecode, then interprets that bytecode.",
           15, SLATE)

    cols = [
        ("Compiled", "C, C++, Go, Rust", BLUE),
        ("Interpreted", "classic scripting", GOLD),
        ("Python", "CPython 3.14", PURPLE),
    ]
    rows = [
        ("Translation happens", "once, before shipping", "every run, line by line",
         "every run \u2014 then bytecode"),
        ("Artifact produced", "machine code (.exe)", "nothing is saved",
         "bytecode (.pyc cache)"),
        ("What you ship", "the executable", "the source", "the source"),
        ("Needed on target machine", "nothing extra", "the interpreter", "the interpreter"),
        ("Execution speed", "fastest", "slowest", "in between"),
        ("Edit \u2192 run loop", "slow (rebuild step)", "instant", "fast (no build step)"),
        ("Syntax errors appear", "at compile time", "at runtime", "before anything runs"),
    ]
    label_w, col_w, gap = 264, 328, 18
    x0 = 80
    head_y, row_y = 176, 244
    row_h, head_h = 66, 62

    for i, (name, sub, acc) in enumerate(cols):
        x = x0 + label_w + gap + i * (col_w + gap)
        c.rr(x, head_y, col_w, head_h, 14, fill=acc)
        c.text(x + col_w / 2, head_y + 22, name, 16, WHITE, "b", "mm")
        c.text(x + col_w / 2, head_y + 44, sub, 12.5, WHITE, "r", "mm", 210)

    y = row_y
    for ri, (label, a, b, d) in enumerate(rows):
        if ri % 2 == 0:
            c.rr(x0, y - 6, W - 160, row_h, 10, fill="#F8FAFC")
        c.text(x0 + 8, y + row_h / 2 - 6, label, 13.5, NAVY, "b", "lm")
        for i, cell in enumerate((a, b, d)):
            x = x0 + label_w + gap + i * (col_w + gap)
            acc = cols[i][2]
            c.text(x + col_w / 2, y + row_h / 2 - 6, cell, 13.5,
                   NAVY if i == 2 else SLATE, "b" if i == 2 else "r", "mm")
        y += row_h

    c.rr(80, H - 84, W - 160, 52, 12, fill=PANEL)
    c.text(W / 2, H - 58, "\u201cInterpreted\u201d describes how bytecode is executed "
                          "\u2014 it does not mean Python skips compilation.",
           14, NAVY, "b", "mm")
    c.save("fig4_comparison.png", OUT)


# --------------------------------------------------------------------------
# figure 5 - myths and facts
# --------------------------------------------------------------------------
def fig_myths():
    pairs = [
        ("Python isn\u2019t a compiled language.",
         "Every run compiles your source to bytecode before executing it."),
        ("\u201cInterpreted\u201d means the raw source is read line by line.",
         "The PVM executes bytecode \u2014 your source is never interpreted directly."),
        (".pyc files make my program run faster.",
         "They speed up startup by skipping compilation. Execution speed is unchanged."),
        ("I can ship a .pyc file like an .exe.",
         "It still needs a matching Python interpreter. Use Docker or a packager instead."),
        ("Compiled languages are always faster.",
         "Usually yes for CPU work \u2014 but native libraries and Python\u2019s new JIT close much of the gap."),
    ]
    W = 1400
    row_h, gap = 86, 14
    H = int(180 + len(pairs) * (row_h + gap) + 70)
    c = C(W, H)
    c.eyebrow(80, 52, "CLEARING IT UP")
    c.text(80, 80, "Five things people get wrong", 32, NAVY, "b")
    c.text(80, 124, "These come up in interviews and code reviews \u2014 worth knowing properly.",
           15, SLATE)

    y = 180
    for myth, fact in pairs:
        c.card(80, y, W - 160, row_h, 14, shadow=False)
        c.rr(80, y, W - 160, row_h, 14, fill=WHITE, outline=LINE, width=1)
        c.rr(80, y, 6, row_h, 3, fill=RED)
        c.circle(122, y + row_h / 2, 15, fill=RED_L)
        c.text(122, y + row_h / 2, "\u2717", 15, RED, "b", "mm")
        c.para(150, y + 26, myth, 14, NAVY, "b", maxw=470, lh=1.4)
        c.line(646, y + 16, 646, y + row_h - 16, LINE, 1.5)
        c.arrow(664, y + row_h / 2, 700, y + row_h / 2, GREEN, 2, 8)
        c.circle(734, y + row_h / 2, 15, fill=GREEN_L)
        c.text(734, y + row_h / 2, "\u2713", 15, GREEN, "b", "mm")
        c.para(762, y + 26, fact, 14, SLATE, "r", maxw=560, lh=1.4)
        y += row_h + gap

    c.rr(80, H - 54, W - 160, 38, 12, fill=BLUE_XL)
    c.text(104, H - 35, "Trainer tip: ask the room to vote on each statement before "
                        "revealing the right-hand side.", 13, NAVY, "r", "lm")
    c.save("fig5_myths.png", OUT)


# --------------------------------------------------------------------------
# figure 6 - where errors appear
# --------------------------------------------------------------------------
def fig_errors():
    W, H = 1400, 644
    c = C(W, H)
    c.eyebrow(80, 52, "ERROR TIMING")
    c.text(80, 80, "Two phases, two kinds of errors", 32, NAVY, "b")
    c.text(80, 124, "Knowing which phase an error belongs to tells you where to look.",
           15, SLATE)

    panels = [
        (80, BLUE, BLUE_XL, PURPLE_L, "Compile phase", "before any of your code runs",
         ["SyntaxError", "IndentationError"],
         "print(\"hello\"",
         "missing closing bracket",
         "The program never starts. Nothing has executed, so nothing needs undoing."),
        (740, PURPLE, PURPLE_L, PURPLE_L, "Runtime", "while bytecode is executing",
         ["NameError", "TypeError", "ZeroDivisionError"],
         "print(total)          # never defined",
         "\u201c5\u201d + 5               # text plus number",
         "Code before the error has already run \u2014 files written, records updated."),
    ]
    for x, acc, tint, tint2, title, sub, chips, ex1, ex2, note in panels:
        c.card(x, 180, 580, 372, 18)
        c.rr(x, 180, 580, 7, 3.5, fill=acc)
        c.rr(x + 26, 208, TWL(title, 13, "b") + 34, 30, 15, fill=tint)
        c.text(x + 26 + (TWL(title, 13, "b") + 34) / 2, 223, title, 13, acc, "b", "mm")
        c.text(x + 26 + TWL(title, 13, "b") + 50, 223, sub, 12.5, MUTED, "r", "lm")
        cx = x + 26
        for chip in chips:
            cx += c.chip(cx, 258, chip, tint, acc, size=13, pad=14, h=34) + 10
        c.text(x + 26, 320, "For example", 12, FAINT, "b", "la")
        c.rr(x + 26, 336, 528, 62, 12, fill="#F8FAFC", outline=LINE, width=1)
        c.text(x + 44, 356, ex1, 13.5, INK, "m", "lm")
        c.text(x + 44, 380, ex2, 13.5, INK, "m", "lm")
        c.para(x + 26, 418, note, 13, MUTED, maxw=520, lh=1.5)
        c.text(x + 26, 500, "\u2717  program stops before it starts" if acc == BLUE
               else "\u2717  program stops halfway",
               13, acc, "b", "la")

    c.rr(80, H - 66, W - 160, 44, 12, fill=PANEL)
    c.text(W / 2, H - 44, "Rule of thumb:  if the error mentions syntax, the file never "
                          "ran. If it mentions a name or a type, it ran and stopped.",
           13, SLATE, "r", "mm")
    c.save("fig6_errors.png", OUT)


# --------------------------------------------------------------------------
# figure 7 - session plan
# --------------------------------------------------------------------------
def fig_session_plan():
    rows = [
        ("Opening & objectives", 3, BLUE),
        ("1. Why translation is needed", 5, BLUE),
        ("2. Compiled vs interpreted", 7, PURPLE),
        ("3. The Python pipeline", 8, PURPLE),
        ("4. Does Python compile?", 6, TEAL),
        ("5. Myths, cleared up", 4, GOLD),
        ("6. Where errors appear", 4, GOLD),
        ("7. Takeaways & knowledge check", 3, GREEN),
    ]
    total = sum(m for _, m, _ in rows)
    W, H = 1340, 700
    c = C(W, H)
    c.eyebrow(90, 52, "TRAINER NOTES")
    c.text(90, 80, "Session plan at a glance", 32, NAVY, "b")
    c.text(90, 124, f"A {total}-minute module. The demo in section 4 is the part "
                    "participants remember \u2014 protect its time.", 14.5, SLATE)

    lx, bx0, bx1 = 90, 470, 1200
    y = 182
    bar_h, gap = 34, 18
    top = max(m for _, m, _ in rows)
    for label, mins, acc in rows:
        c.text(lx, y + bar_h / 2, label, 14.5, NAVY, "r", "lm")
        w = (bx1 - bx0) * mins / top
        c.rr(bx0, y, w, bar_h, 8, fill=acc)
        if w > 90:
            c.text(bx0 + w - 16, y + bar_h / 2, f"{mins} min", 13.5, WHITE, "b", "rm")
        else:
            c.text(bx0 + w + 14, y + bar_h / 2, f"{mins} min", 13.5, acc, "b", "lm")
        y += bar_h + gap

    c.line(bx0, y + 8, bx1, y + 8, LINE, 2)
    c.text(bx1, y + 30, f"Total: {total} minutes", 15.5, NAVY, "b", "ra")
    c.text(bx0, y + 30, "Bars are scaled to the longest section (8 min).",
           12.5, MUTED, "r", "la")

    c.rr(90, H - 84, W - 180, 52, 14, fill=BLUE_XL)
    c.text(W / 2, H - 58, "30-minute version: keep sections 2\u20134 only.      "
                          "60-minute version: add the live dis demo and the __pycache__ "
                          "walkthrough.", 13, NAVY, "r", "mm")
    c.save("fig7_session_plan.png", OUT)


# --------------------------------------------------------------------------
# title card
# --------------------------------------------------------------------------
def title_card():
    W, H = 1400, 700
    c = C(W, H, bg="#FFFFFF")
    for i in range(H):
        t = i / (H - 1)
        col = tuple(int(hex2rgb("#FFFFFF")[k] + (hex2rgb("#E8F1FE")[k] -
                     hex2rgb("#FFFFFF")[k]) * t ** 1.35) for k in range(3))
        c.d.rectangle([0, i * 2, W * 2, (i + 1) * 2], fill=col + (255,))

    c.circle(1290, 60, 250, fill=BLUE_L, alpha=110)
    c.circle(1390, 660, 210, fill=GOLD_L, alpha=110)
    c.circle(1120, 640, 120, fill=BLUE_L, alpha=70)

    # pipeline card
    x, y, w, h = 742, 150, 566, 400
    c.card(x, y, w, h, 20, fill=WHITE, outline="#D8E3F3", shadow=True)
    c.rr(x, y, w, 54, 20, fill="#F7FAFF")
    c.d.rectangle([x * 2, (y + 40) * 2, (x + w) * 2, (y + 54) * 2],
                  fill=hex2rgb("#F7FAFF") + (255,))
    c.line(x, y + 54, x + w, y + 54, LINE, 1.5)
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        c.circle(x + 30 + i * 22, y + 27, 6.5, fill=col)
    c.text(x + 104, y + 27, "how-python-runs", 13, MUTED, "m", "lm")

    steps = [
        ("hello.py", "source code", NAVY, "compile"),
        ("bytecode", "platform-independent", BLUE, "execute"),
        ("Hello, Python!", "output", GREEN, None),
    ]
    sy = y + 82
    for i, (label, sub, acc, arrow_label) in enumerate(steps):
        c.rr(x + 44, sy, w - 88, 66, 14, fill=WHITE, outline="#E2E8F0", width=1)
        c.rr(x + 44, sy, 5, 66, 2.5, fill=acc)
        c.text(x + 70, sy + 26, label, 16.5, NAVY, "mb" if i != 2 else "b", "lm")
        c.text(x + 70, sy + 48, sub, 12, MUTED, "r", "lm")
        sy += 66
        if arrow_label:
            c.arrow(x + w / 2, sy + 6, x + w / 2, sy + 30, acc, 2, 8)
            c.text(x + w / 2 + 16, sy + 18, arrow_label, 11.5, acc, "b", "lm")
            sy += 42

    c.text(96, 274, track("CORPORATE TRAINING  \u00b7  MODULE 02"), 12.5, GOLD, "b")
    c.text(96, 302, "How Python Runs", 50, NAVY, "b")
    c.rr(96, 388, 84, 5, 2.5, fill=GOLD)
    c.text(96, 414, "Interpreted languages  \u00b7  Bytecode  \u00b7  The PVM",
           16.5, SLATE)
    c.text(96, 470, "Python Foundation Series", 14, NAVY, "b")
    c.text(96, 494, "Prepared for new joiners  |  40-minute module  |  2026",
           13, MUTED)

    c.rr(0, H - 8, W, 8, 0, fill=NAVY)
    c.rr(0, H - 8, 300, 8, 0, fill=GOLD)
    path = os.path.join(OUT, "title_card.jpg")
    c.img.convert("RGB").resize((W, H), Image.LANCZOS).save(
        path, "JPEG", quality=90, optimize=True)
    print(f"  title_card.jpg  {W}x{H}  {os.path.getsize(path) / 1024:.0f} KB")


if __name__ == "__main__":
    print("Generating Module 02 visual assets ->", OUT)
    fig_two_paths()
    fig_pipeline()
    fig_code_vs_bytecode()
    fig_comparison()
    fig_myths()
    fig_errors()
    fig_session_plan()
    title_card()
    print("Done.")
