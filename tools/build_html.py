#!/usr/bin/env python3
"""
Render a tutorial draft in Markdown into a self-contained, print-ready HTML
document (images embedded as base64, so the file works anywhere on its own).

Usage:  python3 tools/build_html.py <input.md> [output.html]
"""

import base64
import mimetypes
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
:root{
  --navy:#0B1F3A; --ink:#0F172A; --slate:#475569; --muted:#64748B;
  --line:#E2E8F0; --panel:#F1F5F9; --blue:#2563EB; --blue-xl:#EFF6FF;
  --gold:#D9902A; --gold-xl:#FFFBEB;
}
*{box-sizing:border-box}
body{
  margin:0; background:#F8FAFC; color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:16px; line-height:1.7;
}
.page{max-width:960px; margin:0 auto; background:#fff;
  box-shadow:0 1px 3px rgba(15,23,42,.08),0 12px 40px rgba(15,23,42,.08);}
.hero{width:100%; display:block}
.inner{padding:56px 64px 72px}
h1{font-size:34px; line-height:1.25; color:var(--navy); margin:0 0 6px;
   letter-spacing:-.02em}
h1 + table{margin-top:28px}
h2{font-size:23px; color:var(--navy); margin:52px 0 14px; padding-bottom:10px;
   border-bottom:2px solid var(--line); letter-spacing:-.01em}
h2:first-of-type{margin-top:36px}
h3{font-size:17px; color:var(--navy); margin:30px 0 8px}
p{margin:12px 0}
strong{color:var(--ink)}
a{color:var(--blue); text-decoration:none; border-bottom:1px solid #BFDBFE}
img{max-width:100%; height:auto; border-radius:14px; display:block; margin:26px 0;
    border:1px solid var(--line)}
table{width:100%; border-collapse:collapse; margin:20px 0; font-size:14.5px}
th,td{text-align:left; padding:11px 14px; border-bottom:1px solid var(--line);
      vertical-align:top}
th{background:var(--panel); color:var(--navy); font-weight:700;
   border-bottom:2px solid #CBD5E1; white-space:nowrap}
tbody tr:nth-child(even){background:#FCFDFE}
blockquote{
  margin:22px 0; padding:16px 22px; background:var(--blue-xl);
  border-left:4px solid var(--blue); border-radius:0 12px 12px 0;
}
blockquote p{margin:0}
blockquote p + p{margin-top:10px}
blockquote strong{color:var(--navy)}
blockquote:has(strong:first-child){}
hr{border:none; border-top:1px solid var(--line); margin:44px 0}
ul,ol{padding-left:22px}
li{margin:6px 0}
code{background:#F1F5F9; border:1px solid var(--line); border-radius:6px;
     padding:1.5px 6px; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
     font-size:.88em; color:#0F172A}
details{margin:20px 0; background:var(--gold-xl); border:1px solid #FDE68A;
        border-radius:12px; padding:14px 20px}
summary{cursor:pointer; font-weight:700; color:var(--gold)}
details ol{margin:12px 0 0}
table td:first-child:not(:only-child){}
/* meta table: first two columns as label/value */
.meta th:first-child{white-space:nowrap}
.footer{margin-top:56px; padding-top:20px; border-top:2px solid var(--line);
        color:var(--muted); font-size:13.5px}
@media print{
  body{background:#fff} .page{box-shadow:none; max-width:none}
  .inner{padding:0 8mm} h2{page-break-after:avoid}
  img{page-break-inside:avoid} table{page-break-inside:avoid}
}
@media (max-width:700px){.inner{padding:32px 20px 48px}}
"""


def embed_images(html, base_dir):
    """Replace <img src="..."> with base64 data URIs."""
    def repl(m):
        src = m.group(2)
        if src.startswith(("http://", "https://", "data:")):
            return m.group(0)
        path = os.path.join(base_dir, src)
        if not os.path.exists(path):          # fall back to repo root
            path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            print(f"  ! missing image: {src}")
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as fh:
            data = base64.b64encode(fh.read()).decode("ascii")
        return f'{m.group(1)}src="data:{mime};base64,{data}"'
    return re.sub(r'(<img\b[^>]*?\s)src="([^"]+)"', repl, html)


def build(src_md, out_html=None):
    with open(src_md, encoding="utf-8") as fh:
        text = fh.read()

    title = "Python Tutorial"
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()

    body = markdown.markdown(
        text, extensions=["tables", "attr_list", "md_in_html", "sane_lists"])
    body = embed_images(body, os.path.dirname(os.path.abspath(src_md)))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
<div class="inner">
{body}
<div class="footer">Python Foundation Series &middot; {title} &middot; 2026</div>
</div>
</div>
</body>
</html>
"""
    out_html = out_html or os.path.splitext(src_md)[0] + ".html"
    with open(out_html, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"  {os.path.relpath(out_html, ROOT)}  "
          f"{os.path.getsize(out_html) / 1024:.0f} KB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
