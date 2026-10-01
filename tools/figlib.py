#!/usr/bin/env python3
"""
figlib - the shared visual design system for the Python training modules.

Design language: flat corporate, navy + gold + blue, white background,
DejaVu Sans (regular/bold) + DejaVu Sans Mono. Everything is drawn at 2x
and downscaled, so the PNGs stay crisp. Layout is measured before drawing
so nothing overlaps.

Import this from a module's figure script:

    from figlib import *
    c = C(1400, 500)
    c.text(80, 80, "Hello", 34, NAVY, "b")
    c.save("figure.png", OUT)

All coordinates are in design pixels; the 2x supersampling is internal.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# setup
# --------------------------------------------------------------------------
S = 2  # supersample factor
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

NAVY = "#0B1F3A"
INK = "#0F172A"
SLATE = "#475569"
MUTED = "#64748B"
FAINT = "#94A3B8"
LINE = "#E2E8F0"
PANEL = "#F1F5F9"
WHITE = "#FFFFFF"
BLUE = "#2563EB"
BLUE_L = "#DBEAFE"
BLUE_XL = "#EFF6FF"
GOLD = "#D9902A"
GOLD_L = "#FEF3C7"
GOLD_XL = "#FFFBEB"
TEAL = "#0D9488"
TEAL_L = "#CCFBF1"
GREEN = "#16A34A"
GREEN_L = "#DCFCE7"
PURPLE = "#7C3AED"
PURPLE_L = "#EDE9FE"
RED = "#DC2626"
RED_L = "#FEE2E2"
SKY = "#0284C7"
SKY_L = "#E0F2FE"
SLATEG = "#64748B"
SLATEG_L = "#F1F5F9"

_fonts = {}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def F(size, weight="r"):
    key = (round(size, 2), weight)
    if key not in _fonts:
        path = {"r": FR, "b": FB, "m": FM, "mb": FMB}[weight]
        _fonts[key] = ImageFont.truetype(path, max(1, int(round(size * S))))
    return _fonts[key]


def TWL(s, size, weight="r"):
    """Width of a string in design px."""
    return F(size, weight).getlength(s) / S


def wrap(s, size, maxw, weight="r"):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if TWL(t, size, weight) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(s, size, maxw, weight="b", floor=11.0):
    """Shrink font size until the string fits maxw."""
    while size > floor and TWL(s, size, weight) > maxw:
        size -= 0.5
    return size


def track(s, gap=" "):
    return gap.join(list(s))


class C:
    """Canvas: all coordinates/units are design px, scaled by S internally."""

    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * S, h * S), hex2rgb(bg) + (255,))
        self.d = ImageDraw.Draw(self.img, "RGBA")

    # -- primitives --------------------------------------------------------
    def text(self, x, y, s, size=14, color=INK, weight="r", anchor="la",
             alpha=255):
        self.d.text((x * S, y * S), s, font=F(size, weight),
                    fill=hex2rgb(color) + (alpha,), anchor=anchor)

    def para(self, x, y, s, size=13, color=MUTED, weight="r", maxw=240,
             lh=1.5, anchor="la"):
        lines = wrap(s, size, maxw, weight)
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, size, color, weight, anchor)
        return len(lines) * size * lh

    def rr(self, x, y, w, h, r=12, fill=WHITE, outline=None, width=1,
           alpha=255):
        self.d.rounded_rectangle(
            [x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S,
            fill=(hex2rgb(fill) + (alpha,)) if fill else None,
            outline=(hex2rgb(outline) + (alpha,)) if outline else None,
            width=int(width * S))

    def card(self, x, y, w, h, r=16, fill=WHITE, outline=LINE, shadow=True):
        if shadow:
            self.d.rounded_rectangle(
                [x * S, (y + 6) * S, (x + w) * S, (y + h + 6) * S],
                radius=r * S, fill=(15, 23, 42, 16))
        self.rr(x, y, w, h, r, fill, outline, 1)

    def circle(self, cx, cy, r, fill=None, outline=None, width=1, alpha=255):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                       fill=(hex2rgb(fill) + (alpha,)) if fill else None,
                       outline=(hex2rgb(outline) + (alpha,)) if outline else None,
                       width=int(width * S))

    def line(self, x1, y1, x2, y2, color=LINE, width=1, alpha=255):
        self.d.line([x1 * S, y1 * S, x2 * S, y2 * S],
                    fill=hex2rgb(color) + (alpha,), width=int(width * S))

    def hgrad(self, x, y, w, h, c1, c2):
        steps = int(w)
        for i in range(steps):
            t = i / max(1, steps - 1)
            col = tuple(int(hex2rgb(c1)[k] + (hex2rgb(c2)[k] - hex2rgb(c1)[k]) * t)
                        for k in range(3))
            self.d.rectangle([(x + i) * S, y * S, (x + i + 1) * S, (y + h) * S],
                             fill=col + (255,))

    def chip(self, x, y, label, fill=BLUE_XL, fg=NAVY, dot=None, star=False,
             size=14.5, pad=16, h=40):
        extra = 0
        if dot:
            extra += 14
        if star:
            extra += TWL("\u2605 ", size, "b")
        w = pad * 2 + TWL(label, size, "b") + extra
        self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S],
                                 radius=(h / 2) * S, fill=hex2rgb(fill) + (255,))
        cx = x + pad
        if dot:
            self.circle(cx + 4, y + h / 2, 4, fill=dot)
            cx += 14
        if star:
            self.text(cx, y + h / 2, "\u2605", size + 1, GOLD, "b", "lm")
            cx += TWL("\u2605 ", size, "b")
        self.text(cx, y + h / 2, label, size, fg, "b", "lm")
        return w

    def eyebrow(self, x, y, s, color=GOLD):
        self.text(x, y, track(s), 12.5, color, "b")

    def info_icon(self, cx, cy, r=12, color=NAVY):
        self.circle(cx, cy, r, fill=color)
        self.text(cx, cy, "i", r * 1.6, WHITE, "mb", "mm")

    def arrow(self, x1, y1, x2, y2, color=FAINT, width=2, head=9):
        """Straight arrow with a solid head, in design px."""
        import math
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        ex, ey = x2 - ux * head, y2 - uy * head
        self.line(x1, y1, ex, ey, color, width)
        px, py = -uy, ux
        pts = [(x2, y2), (ex + px * head * 0.55, ey + py * head * 0.55),
               (ex - px * head * 0.55, ey - py * head * 0.55)]
        self.d.polygon([(x * S, y * S) for x, y in pts],
                       fill=hex2rgb(color) + (255,))

    def chevron(self, cx, cy, w=9, h=15, color=FAINT, width=2.5):
        """Stroked '>' marker, used between pipeline stages."""
        self.d.line([((cx - w / 2) * S, (cy - h / 2) * S),
                     ((cx + w / 2) * S, cy * S),
                     ((cx - w / 2) * S, (cy + h / 2) * S)],
                    fill=hex2rgb(color) + (255,), width=int(width * S),
                    joint="curve")

    def band(self, x, y, w, h, label, color, fill, size=12.5, pad=14):
        """Rounded label band, used for phase brackets."""
        self.rr(x, y, w, h, h / 2, fill=fill)
        self.text(x + pad, y + h / 2, label, size, color, "b", "lm")

    def save(self, name, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, name)
        img = self.img.convert("RGB").resize((self.w, self.h), Image.LANCZOS)
        img.save(path, "PNG", optimize=True)
        print(f"  {name}  {img.size[0]}x{img.size[1]}  "
              f"{os.path.getsize(path) / 1024:.0f} KB")


