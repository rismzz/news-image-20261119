#!/usr/bin/env python3
"""Render the poster for news-image-20261119.

Draws a 1024x1024 high-contrast infographic poster summing up
Thursday 19 November 2026's world news, using only Pillow and
DejaVu fonts. Every story was cross-checked against multiple
reports of 19 November 2026:

- The first-ever US-China-Russia trilateral: Trump, Xi and Putin
  meet in Shenzhen on the APEC sidelines (Xi met Putin on the
  18th; Trump flew in from Quad talks in Manila and was met by
  Xi at the airport). Agenda: Ukraine, Iran, Taiwan, rare earths
  and AI chips.
- The US-Iran exchange widens: US jets hit an IRGC missile site
  on Qeshm Island; Iran answers with drones on US bases in
  Bahrain and Kuwait.
- Ukraine's strikes collapse a 227-m road arch of the Kerch
  Bridge into the strait; Moscow vows to rebuild while Russia
  hits Kyiv's Dnipro bridges in reply.
- Democrats nominate Hakeem Jeffries for Speaker of the House —
  set to be the first Black Speaker — days after Peltola's Alaska
  win gave Democrats a 56-44 Senate majority.
- Nvidia: founder Jensen Huang resigns; acting chief Colette
  Kress halts H-series chip shipments to mainland China.
- Cyclone Akvan bears down on India's east coast, set to cross
  between Machilipatnam and Puri.
- Also: GTA VI begins its global rollout; Voyager 1 reaches a
  light-day from Earth; Fed minutes point to more rate hikes.

Run:  python3 render_frontpage.py [output-path]
Default output: entry.png next to this script.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (13, 22, 38)          # deep navy
PANEL = (23, 38, 62)       # panel navy
PANEL2 = (19, 32, 54)
PAPER = (246, 241, 231)    # headline off-white
BODY = (203, 211, 224)     # body light grey-blue
RED = (226, 54, 48)
ORANGE = (246, 148, 32)
GOLD = (246, 198, 66)
TEAL = (52, 186, 172)
GREY = (148, 161, 180)
SKY = (44, 74, 116)
SEA = (26, 84, 138)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, text, y, fnt, fill):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text,
              font=fnt, fill=fill)


def chip(draw, x, y, text, fnt, fill_bg, fill_tx):
    w = draw.textlength(text, font=fnt) + 22
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=8, fill=fill_bg)
    draw.text((x + 11, y + 6), text, font=fnt, fill=fill_tx)
    return x + w + 10


def draw_summit_scene(draw, x0, y0, x1, y1):
    """Shenzhen trilateral: night skyline, a round table, three
    leaders (red, gold, teal dots) around it."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # skyline silhouettes
    base = y0 + int((y1 - y0) * 0.52)
    towers = [(x0 + 8, 0.30), (x0 + 52, 0.42), (x0 + 96, 0.24),
              (x0 + 150, 0.38), (x0 + 196, 0.28), (x0 + 244, 0.44),
              (x0 + 288, 0.32)]
    for tx, frac in towers:
        top = y0 + int((y1 - y0) * frac)
        draw.rectangle([tx, top, tx + 34, base], fill=(18, 32, 56))
        for wy in range(top + 12, base - 10, 18):
            draw.rectangle([tx + 6, wy, tx + 12, wy + 8], fill=GOLD)
            draw.rectangle([tx + 22, wy, tx + 28, wy + 8], fill=GOLD)
    # tower spire on the tallest
    draw.line([(x0 + 113, y0 + int((y1 - y0) * 0.24)),
               (x0 + 113, y0 + int((y1 - y0) * 0.16))],
              fill=(18, 32, 56), width=4)
    # floor
    draw.rectangle([x0, base, x1, y1], fill=(30, 52, 84))
    # round table
    cx = (x0 + x1) // 2
    ty = base + 52
    draw.ellipse([cx - 92, ty - 18, cx + 92, ty + 18], fill=PAPER)
    draw.rectangle([cx - 10, ty + 12, cx + 10, y1 - 34], fill=PAPER)
    # three leaders around the table
    for ang, col in ((200, RED), (270, GOLD), (340, TEAL)):
        px = cx + 62 * math.cos(math.radians(ang))
        py = ty - 6 + 26 * math.sin(math.radians(ang))
        draw.ellipse([px - 13, py - 13, px + 13, py + 13], fill=col)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=PAPER)
    # name plates under the table
    f_lab = SANS_B(14)
    labels = "USA · CHINA · RUSSIA"
    draw.text(((x0 + x1 - draw.textlength(labels, font=f_lab)) / 2,
               y1 - 26), labels, font=f_lab, fill=WHITE)


def draw_bridge_icon(draw, cx, cy):
    """Mini Kerch Bridge: deck with a gap, blast, fallen span."""
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(28, 56, 84))
    draw.rectangle([cx - 20, cy - 2, cx - 6, cy + 2], fill=PAPER)
    draw.rectangle([cx + 6, cy - 2, cx + 20, cy + 2], fill=PAPER)
    draw.line([(cx - 14, cy - 2), (cx - 14, cy - 16)], fill=PAPER, width=2)
    draw.line([(cx + 14, cy - 2), (cx + 14, cy - 16)], fill=PAPER, width=2)
    pts = []
    for i in range(8):
        ang = math.pi * i / 4
        r = 9 if i % 2 == 0 else 4
        pts.append((cx + r * math.cos(ang), cy - 8 + r * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)
    draw.ellipse([cx - 3, cy - 11, cx + 3, cy - 5], fill=RED)
    draw.line([(cx - 4, cy + 4), (cx + 8, cy + 14)], fill=(196, 60, 44),
              width=3)
    draw.arc([cx - 18, cy + 12, cx + 18, cy + 22], 0, 180,
             fill=(170, 205, 235), width=2)


def draw_missile(draw, cx, cy):
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(64, 34, 40))
    draw.polygon([(cx - 14, cy + 16), (cx + 4, cy - 20),
                  (cx + 16, cy - 8), (cx - 2, cy + 24)], fill=PAPER)
    draw.polygon([(cx + 4, cy - 20), (cx + 12, cy - 30),
                  (cx + 16, cy - 8)], fill=RED)
    draw.polygon([(cx - 14, cy + 16), (cx - 24, cy + 26),
                  (cx - 8, cy + 26)], fill=ORANGE)
    draw.polygon([(cx - 4, cy + 30), (cx - 14, cy + 40),
                  (cx + 2, cy + 38)], fill=GOLD)


def draw_dome(draw, cx, cy):
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(52, 44, 84))
    draw.arc([cx - 16, cy - 6, cx + 16, cy + 22], 180, 360, fill=PAPER,
             width=3)
    draw.line([(cx - 20, cy + 8), (cx + 20, cy + 8)], fill=PAPER, width=3)
    draw.line([(cx, cy - 14), (cx, cy - 6)], fill=GOLD, width=3)
    for px in (-12, 0, 12):
        draw.line([(cx + px, cy + 8), (cx + px, cy + 16)], fill=PAPER,
                  width=2)
    draw.line([(cx - 20, cy + 17), (cx + 20, cy + 17)], fill=PAPER,
              width=3)


def draw_chip(draw, cx, cy):
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(24, 52, 44))
    for px in (-14, 0, 14):
        draw.line([(cx + px, cy - 26), (cx + px, cy - 16)], fill=GOLD,
                  width=3)
        draw.line([(cx + px, cy + 16), (cx + px, cy + 26)], fill=GOLD,
                  width=3)
        draw.line([(cx - 26, cy + px), (cx - 16, cy + px)], fill=GOLD,
                  width=3)
        draw.line([(cx + 16, cy + px), (cx + 26, cy + px)], fill=GOLD,
                  width=3)
    draw.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=TEAL)
    draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=(13, 22, 38))


def draw_storm(draw, cx, cy):
    draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(28, 56, 84))
    for r, a0 in ((17, 20), (11, 200), (6, 90)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 260,
                 fill=TEAL, width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=PAPER)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # ---- Masthead ----
    y = 16
    centered(d, "THE WORLD IN ONE DAY", y, SERIF_B(47), PAPER)
    y += 58
    d.rectangle([M, y, W - M, y + 34], fill=RED)
    centered(d, "THURSDAY · 19 NOVEMBER 2026", y + 4, SANS_B(25), WHITE)
    y += 48

    # ---- Lead: Shenzhen trilateral ----
    lead_y0 = y
    lead_y1 = y + 340
    d.rectangle([M, lead_y0, W - M, lead_y1], fill=PANEL)
    tx = M + 22
    ty = lead_y0 + 12
    d.text((tx, ty), "SHENZHEN — THE DAY'S BIG STORY", font=SANS_B(19),
           fill=GOLD)
    ty += 30
    f_lead = SERIF_B(46)
    ty = draw_lines(d, ["THREE PRESIDENTS,", "ONE TABLE"],
                    tx, ty, f_lead, PAPER, 54)
    ty += 6
    sub = ("Trump, Xi & Putin meet today — the first US–China–Russia "
           "trilateral, with Ukraine, Iran and Taiwan on the agenda.")
    ty = draw_lines(d, wrap(d, sub, SANS(20), 545), tx, ty, SANS(20),
                    BODY, 27)
    # illustration, right side of the lead panel
    draw_summit_scene(d, 622, lead_y0 + 18, W - M - 18, lead_y0 + 252)
    f_cap = SANS(14)
    d.text((622, lead_y0 + 258),
           "Shenzhen hosts the APEC leaders' summit.",
           font=f_cap, fill=GREY)
    # chips along the bottom of the lead panel
    cy = lead_y1 - 42
    assert ty <= cy - 6, f"lead text overflows into chips: ty={ty} cy={cy}"
    cx = M + 22
    f_chip = SANS_B(16)
    cx = chip(d, cx, cy, "FIRST-EVER TRILATERAL", f_chip, RED, WHITE)
    cx = chip(d, cx, cy, "APEC · SHENZHEN", f_chip, (64, 74, 92), WHITE)
    cx = chip(d, cx, cy, "XI MET PUTIN WEDNESDAY", f_chip,
              (64, 74, 92), WHITE)
    assert cx <= W - M, f"chips overflow panel: cx={cx}"
    y = lead_y1 + 12

    # ---- Middle band: Gulf + Kerch ----
    band_y1 = y + 232
    half = (CW - 16) // 2
    panels = [
        (M, "MIDDLE EAST — ESCALATION", RED,
         "US–Iran fire widens across the Gulf",
         "US jets hit an IRGC missile site on Qeshm Island. Iran "
         "answers with drones on US bases in Bahrain & Kuwait.",
         draw_missile),
        (M + half + 16, "UKRAINE WAR", GOLD,
         "Kerch Bridge arch is down",
         "A 227-m road arch fell into the strait. Moscow vows to "
         "rebuild as Russia hits Kyiv's Dnipro bridges.",
         draw_bridge_icon),
    ]
    for px, kick, accent, head, body, icon in panels:
        d.rectangle([px, y, px + half, band_y1], fill=PANEL)
        icon(d, px + 44, y + 44)
        d.text((px + 82, y + 18), kick, font=SANS_B(16), fill=accent)
        d.text((px + 82, y + 42), "19 NOV 2026", font=SANS(14), fill=GREY)
        hy = y + 76
        hy = draw_lines(d, wrap(d, head, SERIF_B(28), half - 36),
                        px + 18, hy, SERIF_B(28), PAPER, 34)
        end_y = draw_lines(d, wrap(d, body, SANS(18), half - 36),
                           px + 18, hy + 4, SANS(18), BODY, 24)
        assert end_y <= band_y1 - 8, \
            f"middle-band text overflows panel: end_y={end_y}"
    y = band_y1 + 12

    # ---- Third band: Speaker / Nvidia / Cyclone ----
    band2_y1 = y + 186
    col_w = (CW - 32) // 3
    cols = [
        ("UNITED STATES", GOLD, "Jeffries for Speaker",
         "Democrats nominate Hakeem Jeffries — set to be the first "
         "Black Speaker.", draw_dome),
        ("TECH", TEAL, "Nvidia's chief is out",
         "Founder Jensen Huang resigns. Acting chief Kress halts "
         "H-chip shipments to China.", draw_chip),
        ("DISASTER", RED, "Akvan nears India",
         "Akvan bears down on the east coast, set to cross between "
         "Machilipatnam and Puri.", draw_storm),
    ]
    for i, (kick, accent, head, body, icon) in enumerate(cols):
        px = M + i * (col_w + 16)
        d.rectangle([px, y, px + col_w, band2_y1], fill=PANEL2)
        icon(d, px + 40, y + 40)
        d.text((px + 74, y + 20), kick, font=SANS_B(15), fill=accent)
        d.text((px + 74, y + 42), "19 NOV", font=SANS(13), fill=GREY)
        hy = y + 70
        hy = draw_lines(d, wrap(d, head, SERIF_B(24), col_w - 30),
                        px + 15, hy, SERIF_B(24), PAPER, 29)
        end_y = draw_lines(d, wrap(d, body, SANS(16), col_w - 30),
                           px + 15, hy + 3, SANS(16), BODY, 21)
        assert end_y <= band2_y1 - 8, \
            f"third-band text overflows panel: end_y={end_y}"
    y = band2_y1 + 12

    # ---- Ticker ----
    d.rectangle([M, y, W - M, y + 42], fill=(120, 26, 22))
    ticker = ("GTA VI LAUNCHES TODAY · VOYAGER 1 HITS LIGHT-DAY "
              "· FED EYES MORE HIKES")
    assert d.textlength(ticker, font=SANS_B(20)) <= CW - 8, \
        "ticker too wide for the panel"
    centered(d, ticker, y + 9, SANS_B(20), WHITE)
    y += 54
    extra = ("ISRAEL PUSHES INTO CENTRAL GAZA · AUSTRALIA SANCTIONS "
             "SETTLERS · MOLDOVA SUMMONS RUSSIAN ENVOY")
    centered(d, extra, y, SANS_B(15), GREY)
    y += 26
    foot = "Top stories of Thursday, 19 November 2026 — verified against multiple reports of the day"
    centered(d, foot, y, SANS(14), GREY)
    y += 20
    assert y <= H - 6, f"layout overflow: final y={y}"

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
