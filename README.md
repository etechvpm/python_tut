# python_tut

A Python tutorial built **one topic at a time**, in a corporate-training format.

## How this works

1. You ask about a Python topic (any topic, any order).
2. I explain it in chat, then prepare the module as a **draft** for review.
3. Only after you approve does it get published into `notes/`.
4. Repeat — nothing enters the notes without your approval.

## Layout

```
notes/
  INDEX.md                      <- table of contents: every published topic
  01_introduction_to_python.md  <- source of truth (Markdown)
  01_introduction_to_python.html<- print-ready reading copy (self-contained)
  02_how_python_runs.md/.html   <- module 02, same pattern
assets/
  01_intro/                     <- figures for module 01
  02_how_python_runs/           <- figures for module 02
tools/
  figlib.py                     <- shared design system for all figures
  make_figures.py               <- regenerates figures for module 01
  make_figures_02.py            <- regenerates figures for module 02
  build_html.py                 <- Markdown -> styled, self-contained HTML
```

## Modules published

| # | Module | Document |
|---|--------|----------|
| 01 | Introduction to Python — origins, versions, applications, ecosystem | [notes/01_introduction_to_python.md](notes/01_introduction_to_python.md) |
| 02 | How Python Runs — interpreted languages, bytecode, the PVM | [notes/02_how_python_runs.md](notes/02_how_python_runs.md) |

Full list with status: [`notes/INDEX.md`](notes/INDEX.md).

## Module format

Each published module contains:

- a metadata header (audience, duration, prerequisites, version basis)
- learning objectives
- illustrated sections with comparison tables and callouts
- key takeaways and a knowledge check (answers collapsed)
- glossary and references
- **Appendix A — trainer notes**: 45-minute session plan, per-section talking
  points, facilitation tips, and expected questions with ready answers

## Rebuilding the visuals

```bash
cd tools && python3 make_figures.py && python3 make_figures_02.py && cd ..
python3 tools/build_html.py notes/01_introduction_to_python.md
python3 tools/build_html.py notes/02_how_python_runs.md
```

## Working notes

- Version facts (3.14.x, support windows, TIOBE position, JIT status) are correct as of
  **October 2026**; refresh them each October when a new minor release ships.
- Module 02's `dis` sample output is verbatim CPython 3.11 and is labelled as such,
  because opcode names and offsets differ between versions.
