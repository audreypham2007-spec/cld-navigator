# art.py - the hand-drawn illustration on the Home page.
# English sits in the middle. Around it, speech bubbles in the five home
# languages in the Knowledge Library, each in that language's own script.
# The wobble in each outline is deliberate, so it reads as drawn by hand.

import math
import random

INK = "#1C2B33"

# (text, center x, center y, width radius, height radius, fill, tail angle, rtl)
BUBBLES = [
    ("Español",    112,  78, 78, 40, "#F6D3E0", 45, False),
    ("Tiếng Việt", 290,  70, 82, 40, "#CBE0E1", 130, False),
    ("English",    205, 172, 92, 50, "#FFFFFF", 150, False),
    ("普通话",      84, 262, 66, 38, "#F8E5A8", -36, False),
    ("العربية",    326, 250, 70, 38, "#E1D6F0", 213, True),
    ("廣東話",      206, 318, 60, 32, "#EBDCD0", 270, False),
]


def _bubble_path(cx, cy, rx, ry, tail_deg, seed):
    """A closed, slightly wobbly ellipse with a small speech tail."""
    rnd = random.Random(seed)
    points = []
    steps = 28
    tail = math.radians(tail_deg)
    for i in range(steps):
        a = 2 * math.pi * i / steps
        wobble = 1 + rnd.uniform(-0.025, 0.025)
        x = cx + rx * wobble * math.cos(a)
        y = cy + ry * wobble * math.sin(a)
        # Push one point outward to form the tail.
        diff = abs((a - tail + math.pi) % (2 * math.pi) - math.pi)
        if diff < 0.12:
            x = cx + rx * 1.32 * math.cos(a)
            y = cy + ry * 1.45 * math.sin(a)
        points.append((x, y))
    d = f"M {points[0][0]:.1f} {points[0][1]:.1f} "
    for i in range(1, steps + 1):
        x0, y0 = points[i - 1]
        x1, y1 = points[i % steps]
        d += f"Q {x0:.1f} {y0:.1f} {(x0 + x1) / 2:.1f} {(y0 + y1) / 2:.1f} "
    return d + "Z"


def _svg():
    shapes, labels = [], []
    for i, (text, cx, cy, rx, ry, fill, tail, rtl) in enumerate(BUBBLES):
        shapes.append(f'<path d="{_bubble_path(cx, cy, rx, ry, tail, i + 7)}" '
                      f'fill="{fill}" stroke="{INK}" stroke-width="2.2" '
                      'stroke-linejoin="round"/>')
        size = 27 if text == "English" else 21
        direction = ' direction="rtl"' if rtl else ""
        labels.append(f'<text x="{cx}" y="{cy + size * 0.36:.0f}" text-anchor="middle" '
                      f'font-family="Lexend, sans-serif" font-weight="500" '
                      f'font-size="{size}" fill="{INK}"{direction}>{text}</text>')
    marks = """
  <g fill="none" stroke-linecap="round" stroke-width="3">
    <path d="M 386 150 L 398 132" stroke="#E5B12E"/>
    <path d="M 404 160 Q 412 150 420 158 T 434 154" stroke="#E5B12E"/>
    <path d="M 14 160 Q 24 148 34 160 Q 44 172 54 160" stroke="#B3205A"/>
    <circle cx="30" cy="190" r="3" fill="#5E3A26" stroke="none"/>
    <circle cx="420" cy="196" r="3" fill="#6B4E9B" stroke="none"/>
  </g>"""
    return ('<svg viewBox="0 0 440 372" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Speech bubbles in Spanish, Vietnamese, Mandarin, Arabic, and '
            'Cantonese around a bubble in English">'
            + "".join(shapes) + "".join(labels) + marks + "</svg>")


BUBBLES_SVG = _svg()


# ---------------------------------------------------------------- page art
# Small hand-drawn illustrations for each tab's header. Same wobble as above.
LINE = "#FFFFFF"


def _wobbly(points, closed=True, seed=1, jitter=1.4):
    """Smooth path through points, nudged slightly so it looks hand-drawn."""
    rnd = random.Random(seed)
    pts = [(x + rnd.uniform(-jitter, jitter), y + rnd.uniform(-jitter, jitter))
           for x, y in points]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        mx, my = (x0 + x1) / 2 + rnd.uniform(-1, 1), (y0 + y1) / 2 + rnd.uniform(-1, 1)
        d += f"Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f} "
    return d + ("Z" if closed else "")


def _box(x0, y0, x1, y1, seed):
    return _wobbly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], True, seed)


def _shape(d, fill="none", stroke=LINE, width=2.4):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def _svg_wrap(body, label):
    return (f'<svg viewBox="0 0 200 140" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{label}">{body}</svg>')


def _assess():
    body = _shape(_box(52, 22, 142, 128, 3), "#E2EEEE")
    body += _shape(_box(78, 14, 116, 30, 4), "#FFFFFF")
    for i, y in enumerate((52, 78, 104)):
        body += _shape(_wobbly([(66, y), (72, y + 6), (82, y - 6)], False, 10 + i),
                       stroke="#0E4F57", width=3)
        body += _shape(_wobbly([(92, y), (128, y)], False, 20 + i), stroke="#8FB4B4", width=3)
    body += _shape(_wobbly([(150, 40), (176, 14), (184, 22), (158, 48), (148, 50), (150, 40)],
                           True, 7), "#F6D3E0")
    return _svg_wrap(body, "A clipboard with a checklist and a pencil")


def _cases():
    body = _shape(_wobbly([(30, 44), (70, 44), (80, 34), (150, 34), (150, 112), (30, 112),
                           (30, 44)], True, 5), "#EBDCD0")
    body += _shape(_wobbly([(46, 58), (86, 58), (96, 48), (170, 48), (170, 126), (46, 126),
                            (46, 58)], True, 6), "#FFFFFF")
    for i, (w, c) in enumerate(((64, "#0E4F57"), (40, "#E5B12E"), (52, "#0E4F57"))):
        body += _shape(_wobbly([(64, 78 + i * 14), (64 + w, 78 + i * 14)], False, 30 + i),
                       stroke=c, width=5)
    return _svg_wrap(body, "Two folders with case notes")


def _interview():
    body = _shape(_wobbly([(18, 70), (60, 34), (102, 70)], False, 8))
    body += _shape(_box(28, 70, 92, 124, 9), "#F6D3E0")
    body += _shape(_box(52, 94, 68, 124, 11), "#FFFFFF")
    body += _shape(_wobbly([(112, 26), (186, 26), (186, 68), (140, 68), (126, 82), (128, 68),
                            (112, 68), (112, 26)], True, 12), "#FFFFFF")
    body += _shape(_wobbly([(124, 40), (174, 40)], False, 13), stroke="#B3205A", width=3)
    body += _shape(_wobbly([(124, 54), (160, 54)], False, 14), stroke="#B3205A", width=3)
    body += _shape(_wobbly([(122, 90), (182, 90), (182, 122), (170, 122), (176, 134),
                            (156, 122), (122, 122), (122, 90)], True, 15), "#E2EEEE")
    return _svg_wrap(body, "A house and two speech bubbles")


def _insights():
    body = _shape(_wobbly([(28, 20), (28, 122), (180, 122)], False, 16))
    bars = [(44, 60, "#CBE0E1"), (62, 84, "#E5B12E"), (92, 40, "#CBE0E1"),
            (110, 70, "#E5B12E"), (140, 76, "#CBE0E1"), (158, 96, "#E5B12E")]
    for i, (x, top, c) in enumerate(bars):
        body += _shape(_box(x, top, x + 14, 120, 40 + i), c)
    body += _shape(_wobbly([(176, 18), (176, 32)], False, 50))
    body += _shape(_wobbly([(169, 25), (183, 25)], False, 51))
    return _svg_wrap(body, "A bar chart comparing two languages")


def _library():
    books = [(40, 34, 30, "#F6D3E0"), (72, 22, 26, "#FFFFFF"), (100, 40, 28, "#E1D6F0")]
    body = ""
    for i, (x, top, w, c) in enumerate(books):
        body += _shape(_box(x, top, x + w, 124, 60 + i), c)
        body += _shape(_wobbly([(x + 6, top + 16), (x + w - 6, top + 16)], False, 70 + i),
                       stroke="#1C2B33", width=2)
    body += _shape(_wobbly([(132, 124), (150, 46), (176, 52), (158, 128), (132, 124)],
                           True, 66), "#EBDCD0")
    body += _shape(_wobbly([(20, 126), (186, 126)], False, 67))
    return _svg_wrap(body, "A shelf of books")


def _about():
    body = _shape(_box(40, 18, 120, 126, 80), "#FFFFFF")
    for i, y in enumerate((40, 56, 72, 88)):
        body += _shape(_wobbly([(54, y), (106 - (i % 2) * 14, y)], False, 81 + i),
                       stroke="#8FB4B4", width=3)
    ring = [(132 + 26 * math.cos(a / 10 * math.pi), 78 + 26 * math.sin(a / 10 * math.pi))
            for a in range(0, 21)]
    body += _shape(_wobbly(ring, True, 90, 0.8), "rgba(226,238,238,0.55)")
    body += _shape(_wobbly([(150, 98), (178, 126)], False, 91), width=6)
    return _svg_wrap(body, "A page under a magnifying glass")


PAGE_ART = {"assess": _assess(), "cases": _cases(), "interview": _interview(),
            "insights": _insights(), "library": _library(), "about": _about()}
