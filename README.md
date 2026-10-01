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
assets/
  01_intro/                     <- figures for module 01
tools/
  make_figures.py               <- regenerates all figures for module 01
  build_html.py                 <- Markdown -> styled, self-contained HTML
```

## Modules published

| # | Module | Document |
|---|--------|----------|
| 01 | Introduction to Python — origins, versions, applications, ecosystem | [notes/01_introduction_to_python.md](notes/01_introduction_to_python.md) |

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
python3 tools/make_figures.py                              # figures for module 01
python3 tools/build_html.py notes/01_introduction_to_python.md
```

## Working notes

- Version facts (3.14.x, support windows, TIOBE position) are correct as of **October 2026**;
  review the version table in module 01 each October when a new minor release ships.
