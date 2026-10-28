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
        shapes.append(f'<g class="bub b{i}"><path d="{_bubble_path(cx, cy, rx, ry, tail, i + 7)}" '
                      f'fill="{fill}" stroke="{INK}" stroke-width="2.2" '
                      'stroke-linejoin="round"/>')
        size = 27 if text == "English" else 21
        direction = ' direction="rtl"' if rtl else ""
        shapes.append(f'<text x="{cx}" y="{cy + size * 0.36:.0f}" text-anchor="middle" '
                      f'font-family="Be Vietnam Pro, sans-serif" font-weight="600" '
                      f'font-size="{size}" fill="{INK}"{direction}>{text}</text></g>')
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


def _sounds():
    body = _shape(_wobbly([(24, 30), (118, 30), (118, 92), (64, 92), (46, 112), (48, 92),
                           (24, 92), (24, 30)], True, 95), "#FFFFFF")
    body += ('<text x="71" y="76" text-anchor="middle" font-family="Be Vietnam Pro, sans-serif" '
             'font-weight="700" font-size="40" fill="#0E4F57">θ</text>')
    for i, (x, h) in enumerate(((138, 18), (152, 34), (166, 52), (180, 30))):
        body += _shape(_wobbly([(x, 70 - h), (x, 70 + h)], False, 96 + i),
                       stroke="#E5B12E" if i % 2 else "#FFFFFF", width=5)
    return _svg_wrap(body, "A speech bubble with a sound symbol and a sound wave")


def _refs():
    body = _shape(_box(56, 20, 150, 124, 120), "#FFFFFF")
    for i, y in enumerate((64, 80, 96, 112)):
        body += _shape(_wobbly([(70, y), (136 - (i % 2) * 18, y)], False, 121 + i),
                       stroke="#8FB4B4", width=3)
    body += ('<text x="103" y="58" text-anchor="middle" font-family="Literata, Georgia, serif" '
             'font-size="58" font-weight="500" fill="#E5B12E">“”</text>')
    body += _shape(_box(30, 34, 52, 114, 130), "#F6D3E0")
    return _svg_wrap(body, "A page of references with quotation marks")


PAGE_ART = {"assess": _assess(), "sounds": _sounds(), "refs": _refs(), "cases": _cases(), "interview": _interview(),
            "insights": _insights(), "library": _library(), "about": _about()}


# ---------------------------------------------------------------- icons
# A small hand-drawn icon set (48 x 48), drawn with the same wobble.
DARK = "#1C2B33"


def _icon(body, label, size=48):
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 48 48" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
            f'{body}</svg>')


def _i(d, fill="none", stroke=DARK, width=2.2):
    return _shape(d, fill, stroke, width)


def _circle_pts(cx, cy, r, n=18):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]


ICONS = {}

ICONS["form"] = _icon(
    _i(_box(11, 8, 37, 41, 101), "#E2EEEE")
    + _i(_wobbly([(16, 17), (19, 20), (23, 14)], False, 102), stroke="#0E4F57", width=2.4)
    + _i(_wobbly([(26, 17), (33, 17)], False, 103))
    + _i(_wobbly([(16, 27), (19, 30), (23, 24)], False, 104), stroke="#0E4F57", width=2.4)
    + _i(_wobbly([(26, 27), (33, 27)], False, 105)) + _i(_wobbly([(16, 35), (31, 35)], False, 106)),
    "A form with checkmarks")

ICONS["bulb"] = _icon(
    _i(_wobbly(_circle_pts(24, 19, 11), True, 110, 0.5), "#FCF3D6")
    + _i(_box(19, 30, 29, 38, 111), "#FFFFFF")
    + _i(_wobbly([(20, 42), (28, 42)], False, 112))
    + _i(_wobbly([(24, 13), (24, 22)], False, 113), stroke="#B98A0E")
    + _i(_wobbly([(6, 12), (10, 14)], False, 114)) + _i(_wobbly([(42, 12), (38, 14)], False, 115)),
    "A lightbulb")

ICONS["book"] = _icon(
    _i(_wobbly([(24, 12), (8, 9), (8, 38), (24, 41), (40, 38), (40, 9), (24, 12)], True, 120),
       "#EEE8F5")
    + _i(_wobbly([(24, 12), (24, 41)], False, 121))
    + _i(_wobbly([(12, 18), (20, 19)], False, 122), stroke="#6B4E9B")
    + _i(_wobbly([(28, 19), (36, 18)], False, 123), stroke="#6B4E9B")
    + _i(_wobbly([(12, 25), (20, 26)], False, 124), stroke="#6B4E9B"),
    "An open book")

ICONS["tag"] = _icon(
    _i(_wobbly([(8, 20), (20, 8), (40, 8), (40, 28), (28, 40), (8, 20)], True, 130), "#F9E3EB")
    + _i(_wobbly(_circle_pts(33, 15, 3, 10), True, 131, 0.3))
    + _i(_wobbly([(17, 21), (25, 29)], False, 132), stroke="#B3205A", width=2.8)
    + _i(_wobbly([(25, 21), (17, 29)], False, 133), stroke="#B3205A", width=2.8),
    "A tag marked wrong")

ICONS["clock"] = _icon(
    _i(_wobbly(_circle_pts(24, 25, 15), True, 140, 0.6), "#E2EEEE")
    + _i(_wobbly([(24, 25), (24, 15)], False, 141), stroke="#0E4F57", width=2.6)
    + _i(_wobbly([(24, 25), (31, 29)], False, 142), stroke="#0E4F57", width=2.6)
    + _i(_wobbly([(18, 6), (30, 6)], False, 143)),
    "A clock")

ICONS["school"] = _icon(
    _i(_wobbly([(6, 20), (24, 8), (42, 20)], False, 150))
    + _i(_box(10, 20, 38, 41, 151), "#E2EEEE")
    + _i(_box(20, 28, 28, 41, 152), "#FFFFFF")
    + _i(_wobbly([(24, 8), (24, 2), (31, 4), (24, 6)], False, 153), stroke="#B3205A"),
    "A school")

ICONS["clinic"] = _icon(
    _i(_box(8, 12, 40, 40, 160), "#F9E3EB")
    + _i(_wobbly([(24, 18), (24, 34)], False, 161), stroke="#B3205A", width=3.2)
    + _i(_wobbly([(16, 26), (32, 26)], False, 162), stroke="#B3205A", width=3.2),
    "A clinic")

ICONS["cap"] = _icon(
    _i(_wobbly([(4, 18), (24, 9), (44, 18), (24, 27), (4, 18)], True, 170), "#EEE8F5")
    + _i(_wobbly([(13, 22), (13, 32), (24, 37), (35, 32), (35, 22)], False, 171))
    + _i(_wobbly([(40, 20), (40, 32)], False, 172), stroke="#6B4E9B"),
    "A graduation cap")

ICONS["calendar"] = _icon(
    _i(_box(8, 11, 40, 40, 180), "#FFFFFF") + _i(_box(8, 11, 40, 18, 181), "#E2EEEE")
    + _i(_wobbly([(16, 7), (16, 14)], False, 182)) + _i(_wobbly([(32, 7), (32, 14)], False, 183))
    + "".join(_i(_wobbly([(x, y), (x + 3, y)], False, 184 + k), stroke="#0E4F57", width=2.6)
              for k, (x, y) in enumerate([(14, 25), (22, 25), (30, 25), (14, 33), (22, 33)])),
    "A calendar")

ICONS["chat"] = _icon(
    _i(_wobbly([(5, 8), (31, 8), (31, 25), (14, 25), (8, 31), (9, 25), (5, 25), (5, 8)],
               True, 190), "#F9E3EB")
    + _i(_wobbly([(19, 21), (43, 21), (43, 37), (39, 37), (40, 43), (33, 37), (19, 37), (19, 21)],
                 True, 191), "#E2EEEE"),
    "Two speech bubbles")

ICONS["globe"] = _icon(
    _i(_wobbly(_circle_pts(24, 24, 17), True, 200, 0.6), "#E2EEEE")
    + _i(_wobbly([(24, 7), (17, 24), (24, 41)], False, 201))
    + _i(_wobbly([(24, 7), (31, 24), (24, 41)], False, 202))
    + _i(_wobbly([(7, 24), (41, 24)], False, 203))
    + _i(_wobbly([(10, 15), (38, 15)], False, 204)) + _i(_wobbly([(10, 33), (38, 33)], False, 205)),
    "A globe")

ICONS["shield"] = _icon(
    _i(_wobbly([(24, 5), (40, 11), (38, 28), (24, 43), (10, 28), (8, 11), (24, 5)], True, 210),
       "#E2EEEE")
    + _i(_wobbly([(17, 24), (22, 29), (31, 18)], False, 211), stroke="#0E4F57", width=2.8),
    "A shield with a checkmark")

ICONS["folders"] = _icon(
    _i(_wobbly([(5, 14), (17, 14), (20, 10), (36, 10), (36, 34), (5, 34), (5, 14)], True, 220),
       "#EBDCD0")
    + _i(_wobbly([(11, 20), (23, 20), (26, 16), (43, 16), (43, 40), (11, 40), (11, 20)], True, 221),
         "#FFFFFF")
    + _i(_wobbly([(17, 28), (36, 28)], False, 222), stroke="#0E4F57")
    + _i(_wobbly([(17, 34), (30, 34)], False, 223), stroke="#E5B12E"),
    "Folders of cases")

ICONS["search"] = _icon(
    _i(_wobbly(_circle_pts(20, 20, 12), True, 230, 0.5), "#FFFFFF")
    + _i(_wobbly([(29, 29), (41, 41)], False, 231), width=4),
    "A magnifying glass")


def icon(name, size=48):
    """An icon from the set, at the requested size."""
    svg = ICONS[name]
    return svg.replace('width="48" height="48"', f'width="{size}" height="{size}"', 1)


def donut(shares, colors, size=220):
    """A hand-drawn donut chart. shares: [(label, percent)]; the rest is 'other'."""
    total = sum(p for _, p in shares)
    parts = shares + [("Other", max(0.0, 100 - total))]
    cols = colors + ["#DCE3E3"]
    cx = cy = 60
    r_out, r_in = 52, 30
    start = -math.pi / 2
    body = ""
    for i, ((label, pct), col) in enumerate(zip(parts, cols)):
        if pct <= 0:
            continue
        sweep = 2 * math.pi * pct / 100
        n = max(3, int(pct / 2))
        outer = [(cx + r_out * math.cos(start + sweep * k / n),
                  cy + r_out * math.sin(start + sweep * k / n)) for k in range(n + 1)]
        inner = [(cx + r_in * math.cos(start + sweep * k / n),
                  cy + r_in * math.sin(start + sweep * k / n)) for k in range(n, -1, -1)]
        d = _wobbly(outer + inner + [outer[0]], True, 300 + i, 0.5)
        body += (f'<path d="{d}" fill="{col}" stroke="#FFFFFF" stroke-width="1.6" '
                 f'stroke-linejoin="round"><title>{label}: {pct:.2f}%</title></path>')
        start += sweep
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 120 120" '
            'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Donut chart of '
            'home languages of California English learners">' + body + "</svg>")


# ---------------------------------------------------------------- About page
def _hello():
    """Two speech bubbles, Vietnamese and English, for the About page."""
    bubbles = [("Xin chào", 92, 62, 80, 42, "#DCEBEB", 120, 1),
               ("Hello", 120, 160, 64, 36, "#FFFFFF", 300, 2)]
    body = ""
    for text, cx, cy, rx, ry, fill, tail, seed in bubbles:
        body += (f'<path d="{_bubble_path(cx, cy, rx, ry, tail, seed + 40)}" fill="{fill}" '
                 f'stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
                 f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" '
                 f'font-family="Be Vietnam Pro, sans-serif" font-weight="600" font-size="23" '
                 f'fill="{INK}">{text}</text>')
    body += ('<g fill="none" stroke-linecap="round" stroke-width="3">'
             '<path d="M 186 40 L 196 26" stroke="#E5B12E"/>'
             '<path d="M 22 168 Q 30 158 38 168 Q 46 178 54 168" stroke="#B3205A"/></g>')
    return ('<svg viewBox="0 0 210 210" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Speech bubbles saying Xin chào and Hello">' + body + "</svg>")


HELLO_SVG = _hello()


# ---------------------------------------------------------------- tone charts
TONE_COLORS = ["#0E4F57", "#B3205A", "#C9951A", "#6B4E9B", "#5E3A26", "#2E6B72"]


def _tone_svg(points, color):
    """One tone's pitch shape on a 1-5 grid. None breaks the line, "stop" ends it
    with a short bar."""
    w, h, pad = 120, 84, 10
    stop = points and points[-1] == "stop"
    pts = [p for p in points if p != "stop"]
    n = len(pts)
    span = 0.62 if stop else 1.0
    xs = [pad + (w - 2 * pad) * span * i / max(1, n - 1) for i in range(n)]

    def y(v):
        return h - pad - (h - 2 * pad) * (v - 1) / 4

    grid = "".join(f'<line x1="{pad}" x2="{w - pad}" y1="{y(v):.1f}" y2="{y(v):.1f}" '
                   f'stroke="#DCE3E3" stroke-width="1"{" stroke-dasharray=\"2 3\"" if v != 3 else ""}/>'
                   for v in range(1, 6))
    segs, cur = [], []
    for x, v in zip(xs, pts):
        if v is None:
            segs.append(cur)
            cur = []
        else:
            cur.append((x, y(v)))
    segs.append(cur)
    lines = ""
    for seg in segs:
        if len(seg) == 1:
            seg = [seg[0], (seg[0][0] + 1, seg[0][1])]
        # Catmull-Rom spline, so the curve passes through every pitch point.
        d = f"M {seg[0][0]:.1f} {seg[0][1]:.1f} "
        if len(seg) == 2:
            d += f"L {seg[1][0]:.1f} {seg[1][1]:.1f}"
        else:
            p = [seg[0]] + seg + [seg[-1]]
            for i in range(1, len(p) - 2):
                (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
                c1 = (x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6)
                c2 = (x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6)
                d += (f"C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} "
                      f"{x2:.1f} {y2:.1f} ")
        lines += (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" '
                  'stroke-linecap="round" stroke-linejoin="round"/>')
    if stop:
        ex, ey = xs[-1], y(pts[-1])
        lines += (f'<line x1="{ex + 7:.1f}" x2="{ex + 7:.1f}" y1="{ey - 9:.1f}" '
                  f'y2="{ey + 9:.1f}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-hidden="true">{grid}{lines}</svg>')


def tone_chart(tones):
    """Small multiples: one pitch drawing per tone, with the word under it."""
    cells = ""
    for i, (label, syl, written, meaning, points, note) in enumerate(tones):
        color = TONE_COLORS[i % len(TONE_COLORS)]
        same = written == syl
        cells += (f'<figure class="tone-cell"><div class="tone-svg">{_tone_svg(points, color)}</div>'
                  f'<figcaption><span class="tone-w" style="color:{color}">{written}</span>'
                  + ("" if same else f'<span class="tone-syl">{syl}</span>')
                  + f'<span class="tone-m">{meaning}</span>'
                  f'<span class="tone-l">{label}</span><span class="tone-n">{note}</span>'
                  '</figcaption></figure>')
    return (f'<div class="tone-chart" style="--n:{len(tones)}" role="img" '
            f'aria-label="Pitch shapes of {len(tones)} tones">{cells}</div>')


# ---------------------------------------------------------------- waffle chart
def waffle(shares, colors, other_color="#DCE3E3"):
    """100 squares, one per percent. shares: [(label, percent)] in order."""
    counts = [round(p) for _, p in shares]
    counts.append(max(0, 100 - sum(counts)))
    fills = []
    for c, col in zip(counts, colors + [other_color]):
        fills += [col] * c
    fills = (fills + [other_color] * 100)[:100]
    size, gap = 20, 4
    rects = ""
    for i, col in enumerate(fills):
        # Fill column by column from the left, so groups read as solid blocks.
        x, y = i // 10, i % 10
        rects += (f'<rect x="{x * (size + gap)}" y="{y * (size + gap)}" width="{size}" '
                  f'height="{size}" rx="4" fill="{col}"/>')
    side = 10 * size + 9 * gap
    return (f'<svg viewBox="0 0 {side} {side}" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="One hundred squares, one for each percent of California English '
            f'learners">{rects}</svg>')


# ---------------------------------------------------------------- greeting strip
GREET = [("Hola", "Spanish", "#F6D3E0", ""), ("Xin chào", "Vietnamese", "#CBE0E1", ""),
         ("你好", "Mandarin", "#F8E5A8", "nǐ hǎo"), ("مرحبا", "Arabic", "#E1D6F0", "marḥaban"),
         ("你好", "Cantonese", "#EBDCD0", "nei5 hou2"), ("Hello", "English", "#FFFFFF", "")]


def greeting_strip():
    """Six hand-drawn speech bubbles saying hello, closing every page."""
    w, h = 1040, 150
    step = w / len(GREET)
    body = ""
    for i, (word, lang, fill, roman) in enumerate(GREET):
        cx = step * i + step / 2
        cy = 62 + (14 if i % 2 else 0)
        rx, ry = 70, 40
        tail = 110 if i % 2 == 0 else 70
        rtl = ' direction="rtl"' if lang == "Arabic" else ""
        body += (f'<g class="gb"><path d="{_bubble_path(cx, cy, rx, ry, tail, 500 + i)}" '
                 f'fill="{fill}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                 f'<text x="{cx:.0f}" y="{cy + (2 if roman else 8):.0f}" text-anchor="middle" '
                 f'font-family="Be Vietnam Pro, sans-serif" font-weight="700" font-size="22" '
                 f'fill="{INK}"{rtl}>{word}</text>'
                 + (f'<text x="{cx:.0f}" y="{cy + 22:.0f}" text-anchor="middle" '
                    'font-family="Literata, Georgia, serif" font-style="italic" '
                    f'font-size="13" fill="#56676D">{roman}</text>' if roman else "")
                 + f'<text x="{cx:.0f}" y="{h - 4}" text-anchor="middle" '
                 'font-family="Be Vietnam Pro, sans-serif" font-size="12" font-weight="600" '
                 f'fill="#56676D">{lang}</text></g>')
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Hello in Spanish, Vietnamese, Mandarin, Arabic, Cantonese, and '
            f'English">{body}</svg>')


GREETING_SVG = greeting_strip()


# ---------------------------------------------------------------- interpreter triangle
def _interp():
    """SLP, interpreter, and family, with conversation lines between them."""
    nodes = [("SLP", 110, 70, "#DCEBEB"), ("Interpreter", 360, 70, "#F8E5A8"),
             ("Family", 610, 70, "#F6D3E0")]
    body = ""
    for (a, ax, ay, _), (b, bx, by, _) in zip(nodes, nodes[1:]):
        mid = (ax + bx) / 2
        for k, sign in enumerate((-1, 1)):
            d = _wobbly([(ax + 62, ay + sign * 14), (mid, ay + sign * 34), (bx - 62, by + sign * 14)],
                        False, 700 + k + int(ax), 1.0)
            body += _shape(d, stroke="#13303A" if k == 0 else "#B3205A", width=2.4)
        body += (f'<path d="M {bx - 66} {by - 20} l 10 6 l -12 4" fill="none" stroke="#13303A" '
                 'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<path d="M {ax + 66} {ay + 20} l -10 -6 l 12 -4" fill="none" stroke="#B3205A" '
                 'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (label, cx, cy, fill) in enumerate(nodes):
        body += (f'<path d="{_bubble_path(cx, cy, 60, 40, 90, 720 + i)}" fill="{fill}" '
                 f'stroke="#13303A" stroke-width="2.2" stroke-linejoin="round"/>'
                 f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-family="Be Vietnam Pro, '
                 f'sans-serif" font-weight="700" font-size="19" fill="#13303A">{label}</text>')
    return ('<svg viewBox="0 0 720 150" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="The SLP, the interpreter, and the family talking back and forth">'
            + body + "</svg>")


INTERP_SVG = _interp()


# ---------------------------------------------------------------- people
# Simple hand-drawn people in the same wobbly ink line as the rest of the site.
SKIN = ["#F2D2B6", "#D9A77E", "#B07A52", "#8A5A3B", "#EBC29C"]
HAIR = ["#2B1D16", "#4A2E1F", "#1C1C1C", "#6B4226", "#2E2A28"]


def _ellipse_pts(cx, cy, rx, ry, n=20):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]


def person(x, y, scale=1.0, skin=0, hair=0, shirt="#0E4F57", style="short", seed=1,
           child=False, extra=""):
    """A standing bust. (x, y) is the top of the head. Returns SVG markup."""
    s = scale
    head_r = (18 if child else 17) * s
    cx, cy = x, y + head_r
    body_w = (21 if child else 27) * s
    body_top = cy + head_r - 1 * s
    body_h = (30 if child else 40) * s
    out = ""
    # hair behind the head for long styles
    if style in ("long", "bun"):
        back = _ellipse_pts(cx, cy + 4 * s, head_r * 1.15, head_r * (1.35 if style == "long" else 1.05))
        out += _shape(_wobbly(back, True, seed + 1, 0.6), HAIR[hair], "#13303A", 2)
    # shirt / body
    body = [(cx - body_w, body_top + body_h), (cx - body_w * 0.98, body_top + 12 * s),
            (cx - body_w * 0.8, body_top + 4 * s), (cx - body_w * 0.35, body_top),
            (cx + body_w * 0.35, body_top), (cx + body_w * 0.8, body_top + 4 * s),
            (cx + body_w * 0.98, body_top + 12 * s), (cx + body_w, body_top + body_h)]
    out += _shape(_wobbly(body, False, seed + 2, 0.6), shirt, "#13303A", 2.2)
    # neck
    out += _shape(_wobbly([(cx - 5 * s, body_top - 4 * s), (cx - 5 * s, body_top + 3 * s),
                           (cx, body_top + 6 * s), (cx + 5 * s, body_top + 3 * s),
                           (cx + 5 * s, body_top - 4 * s)], False, seed + 7, 0.3),
                  SKIN[skin], "#13303A", 1.8)
    # neck + head
    out += _shape(_wobbly(_ellipse_pts(cx, cy, head_r, head_r * 1.05), True, seed + 3, 0.5),
                  SKIN[skin], "#13303A", 2.2)
    # hair on top
    if style == "short":
        top = [(cx - head_r * 1.02, cy), (cx - head_r * 0.9, cy - head_r * 0.75),
               (cx - head_r * 0.2, cy - head_r * 1.12), (cx + head_r * 0.7, cy - head_r * 0.95),
               (cx + head_r * 1.04, cy - head_r * 0.15), (cx + head_r * 0.4, cy - head_r * 0.55),
               (cx - head_r * 0.45, cy - head_r * 0.45), (cx - head_r * 1.02, cy)]
    elif style == "bun":
        out += _shape(_wobbly(_ellipse_pts(cx + head_r * 0.2, cy - head_r * 1.15, head_r * 0.42,
                                           head_r * 0.36), True, seed + 4, 0.4), HAIR[hair],
                      "#13303A", 2)
        top = [(cx - head_r * 1.03, cy + head_r * 0.1), (cx - head_r * 0.85, cy - head_r * 0.8),
               (cx, cy - head_r * 1.08), (cx + head_r * 0.85, cy - head_r * 0.8),
               (cx + head_r * 1.03, cy + head_r * 0.1), (cx + head_r * 0.5, cy - head_r * 0.45),
               (cx - head_r * 0.5, cy - head_r * 0.45), (cx - head_r * 1.03, cy + head_r * 0.1)]
    else:  # long
        top = [(cx - head_r * 1.05, cy + head_r * 0.3), (cx - head_r * 0.9, cy - head_r * 0.8),
               (cx, cy - head_r * 1.1), (cx + head_r * 0.9, cy - head_r * 0.8),
               (cx + head_r * 1.05, cy + head_r * 0.3), (cx + head_r * 0.35, cy - head_r * 0.5),
               (cx - head_r * 0.6, cy - head_r * 0.3), (cx - head_r * 1.05, cy + head_r * 0.3)]
    out += _shape(_wobbly(top, True, seed + 5, 0.5), HAIR[hair], "#13303A", 2)
    # face: two dot eyes and a small smile
    ey = cy + head_r * 0.12
    out += (f'<circle cx="{cx - head_r * 0.36:.1f}" cy="{ey:.1f}" r="{1.9 * s:.1f}" fill="#13303A"/>'
            f'<circle cx="{cx + head_r * 0.36:.1f}" cy="{ey:.1f}" r="{1.9 * s:.1f}" fill="#13303A"/>')
    out += _shape(_wobbly([(cx - head_r * 0.3, cy + head_r * 0.45), (cx, cy + head_r * 0.62),
                           (cx + head_r * 0.3, cy + head_r * 0.45)], False, seed + 6, 0.3),
                  "none", "#13303A", 1.8)
    # rosy cheeks
    out += (f'<circle cx="{cx - head_r * 0.6:.1f}" cy="{cy + head_r * 0.4:.1f}" r="{3 * s:.1f}" '
            f'fill="#E89AAE" opacity="0.55"/><circle cx="{cx + head_r * 0.6:.1f}" '
            f'cy="{cy + head_r * 0.4:.1f}" r="{3 * s:.1f}" fill="#E89AAE" opacity="0.55"/>')
    return out + extra


def _wrap(body, w, h, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{label}">{body}</svg>')


def _glasses(cx, eye_y, r, seed):
    return (_shape(_wobbly(_ellipse_pts(cx - r * 0.36, eye_y, r * 0.24, r * 0.2), True, seed, 0.2),
                   "none", "#13303A", 1.6)
            + _shape(_wobbly(_ellipse_pts(cx + r * 0.36, eye_y, r * 0.24, r * 0.2), True, seed + 1,
                             0.2), "none", "#13303A", 1.6)
            + _shape(_wobbly([(cx - r * 0.12, eye_y), (cx + r * 0.12, eye_y)], False, seed + 2, 0.1),
                     "none", "#13303A", 1.6))


def persona_school():
    """A school SLP with a lanyard badge."""
    p = person(60, 14, 1.15, skin=1, hair=1, shirt="#0E4F57", style="bun", seed=31)
    cx, top = 60, 14 + 17 * 1.15 * 2
    p += _shape(_wobbly([(cx - 8, top + 2), (cx - 2, top + 26), (cx + 8, top + 2)], False, 33, 0.4),
                "none", "#E5B12E", 2.2)
    p += _shape(_box(cx - 9, top + 24, cx + 7, top + 40, 34), "#FFFFFF", "#13303A", 1.8)
    p += _shape(_wobbly([(cx - 5, top + 30), (cx + 3, top + 30)], False, 35, 0.2), "none", "#0E4F57", 1.6)
    return _wrap(p, 120, 110, "A school SLP wearing a badge")


def persona_clinic():
    """A clinic SLP holding a clipboard."""
    p = person(60, 14, 1.15, skin=0, hair=2, shirt="#B3205A", style="short", seed=41)
    cx, top = 60, 14 + 17 * 1.15 * 2
    p += _shape(_box(cx + 2, top + 10, cx + 26, top + 42, 42), "#FCF5DE", "#13303A", 1.8)
    p += _shape(_box(cx + 9, top + 7, cx + 19, top + 13, 43), "#FFFFFF", "#13303A", 1.6)
    for k, yy in enumerate((top + 21, top + 28, top + 35)):
        p += _shape(_wobbly([(cx + 7, yy), (cx + 21, yy)], False, 44 + k, 0.2), "none", "#8FB4B4", 1.6)
    return _wrap(p, 120, 110, "A clinic SLP holding a clipboard")


def persona_student():
    """An SLP graduate student with glasses and a book."""
    p = person(60, 14, 1.15, skin=4, hair=0, shirt="#6B4E9B", style="long", seed=51)
    r = 17 * 1.15
    p += _glasses(60, 14 + r + r * 0.12, r, 52)
    top = 14 + r * 2
    p += _shape(_wobbly([(36, top + 30), (60, top + 24), (84, top + 30), (84, top + 46),
                         (60, top + 40), (36, top + 46), (36, top + 30)], True, 53, 0.5),
                "#FFFFFF", "#13303A", 1.8)
    p += _shape(_wobbly([(60, top + 24), (60, top + 40)], False, 54, 0.2), "none", "#13303A", 1.6)
    return _wrap(p, 120, 110, "An SLP graduate student holding a book")


def child_two_languages():
    """A child with speech bubbles in Vietnamese and English."""
    body = person(110, 70, 1.6, skin=3, hair=2, shirt="#E5B12E", style="short", seed=61, child=True)
    body += (f'<path d="{_bubble_path(48, 46, 40, 26, 40, 62)}" fill="#CBE0E1" stroke="#13303A" '
             'stroke-width="2.2" stroke-linejoin="round"/>'
             '<text x="48" y="54" text-anchor="middle" font-family="Be Vietnam Pro, sans-serif" '
             'font-weight="700" font-size="22" fill="#13303A">mẹ</text>'
             f'<path d="{_bubble_path(176, 40, 42, 26, 140, 63)}" fill="#FFFFFF" stroke="#13303A" '
             'stroke-width="2.2" stroke-linejoin="round"/>'
             '<text x="176" y="48" text-anchor="middle" font-family="Be Vietnam Pro, sans-serif" '
             'font-weight="700" font-size="22" fill="#13303A">mom</text>')
    body += ('<g fill="none" stroke-linecap="round" stroke-width="3">'
             '<path d="M 18 120 Q 26 110 34 120 Q 42 130 50 120" stroke="#B3205A"/>'
             '<path d="M 204 108 L 214 94" stroke="#0E4F57"/></g>')
    return _wrap(body, 230, 210, "A child with speech bubbles saying mẹ in Vietnamese and mom in English")


def session_scene():
    """SLP, interpreter, and a parent with a child, with arrows between them."""
    body = ""
    people = [(110, "SLP", dict(skin=1, hair=1, shirt="#0E4F57", style="bun", seed=71)),
              (360, "Interpreter", dict(skin=2, hair=0, shirt="#E5B12E", style="short", seed=72)),
              (590, None, dict(skin=0, hair=4, shirt="#B3205A", style="long", seed=73))]
    for x, label, kw in people:
        body += person(x, 18, 1.25, **kw)
    body += person(655, 46, 1.0, skin=0, hair=4, shirt="#F6D3E0", style="short", seed=74, child=True)
    for k, (ax, bx) in enumerate(((150, 320), (400, 555))):
        mid = (ax + bx) / 2
        body += _shape(_wobbly([(ax, 52), (mid, 40), (bx, 52)], False, 80 + k, 0.6), "none", "#13303A", 2.4)
        body += _shape(_wobbly([(bx, 72), (mid, 84), (ax, 72)], False, 90 + k, 0.6), "none", "#B3205A", 2.4)
        body += (f'<path d="M {bx - 11} {46} l 11 6 l -11 5" fill="none" stroke="#13303A" '
                 'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<path d="M {ax + 11} {66} l -11 6 l 11 5" fill="none" stroke="#B3205A" '
                 'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, label in ((110, "SLP"), (360, "Interpreter"), (615, "Family")):
        body += (f'<text x="{x}" y="150" text-anchor="middle" font-family="Be Vietnam Pro, sans-serif" '
                 f'font-weight="700" font-size="17" fill="#13303A">{label}</text>')
    return _wrap(body, 720, 158, "An SLP, an interpreter, and a parent with a child, talking back "
                 "and forth")


PERSONA_SVGS = [persona_school(), persona_clinic(), persona_student()]
CHILD_SVG = child_two_languages()
SESSION_SVG = session_scene()
