#!/usr/bin/env python3
"""Draw the 19 November 2026 news poster (news-image-20261119).

A 1024x1024 infographic, "THE WORLD IN ONE DAY", built with
Pillow and the DejaVu faces only. The stories are the day's
verified headlines, each confirmed in more than one report
dated 19 November 2026:

- Shenzhen: Trump, Xi and Putin sit down together, the first
  US-China-Russia trilateral, on the APEC sidelines. Xi met
  Putin the day before; Trump flew in from Quad talks in
  Manila. Ukraine, Iran, Taiwan, rare earths and AI chips are
  on the table.
- Gulf: American jets hit an IRGC missile site on Qeshm
  Island; Iran fires drones at US bases in Bahrain and Kuwait.
- Kerch Strait: a 227-metre road arch of the Kerch Bridge is
  down in the water; Moscow promises a rebuild while Russian
  missiles hit Kyiv's bridges over the Dnipro.
- Washington: the Democrats nominate Hakeem Jeffries for
  Speaker of the House; he would be the first Black Speaker.
- Tech: Nvidia founder Jensen Huang resigns; acting chief
  Colette Kress stops H-series chip shipments to China.
- Weather: Cyclone Akvan closes on India's east coast and is
  expected to cross between Machilipatnam and Puri.
- Also in the ticker: GTA VI launches worldwide, Voyager 1
  reaches a light-day from Earth, and the Fed's minutes point
  to further rate hikes.

Usage: python3 render_frontpage.py [output.png]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = (1024, 1024)
MARGIN = 34
CW = SIZE[0] - 2 * MARGIN

PALETTE = {
    "night": (12, 20, 36),
    "card": (24, 40, 66),
    "card2": (20, 34, 58),
    "paper": (247, 242, 232),
    "ink": (205, 213, 226),
    "dim": (150, 163, 182),
    "alarm": (228, 56, 50),
    "amber": (247, 150, 34),
    "gold": (247, 199, 68),
    "mint": (54, 188, 174),
    "sky": (46, 76, 118),
    "sea": (28, 86, 140),
    "white": (255, 255, 255),
    "slate": (66, 76, 94),
}

FACES = "/usr/share/fonts/truetype/dejavu"
_cache = {}


def face(kind, size):
    """A cached DejaVu face: kind is serif_b, sans_b or sans."""
    key = (kind, size)
    if key not in _cache:
        names = {
            "serif_b": "DejaVuSerif-Bold.ttf",
            "sans_b": "DejaVuSans-Bold.ttf",
            "sans": "DejaVuSans.ttf",
        }
        _cache[key] = ImageFont.truetype(
            os.path.join(FACES, names[kind]), size)
    return _cache[key]


def split_lines(draw, text, fnt, width):
    """Greedy word wrap, returning a list of lines."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


class Poster:
    """A 1024x1024 canvas with a y-cursor and small helpers."""

    def __init__(self):
        self.img = Image.new("RGB", SIZE, PALETTE["night"])
        self.d = ImageDraw.Draw(self.img)
        self.y = 0

    def text(self, pos, s, fnt, colour):
        self.d.text(pos, s, font=fnt, fill=colour)

    def centre(self, y, s, fnt, colour):
        w = self.d.textlength(s, font=fnt)
        self.text(((SIZE[0] - w) / 2, y), s, fnt, colour)

    def para(self, x, y, lines, fnt, colour, gap):
        """Draw lines top to bottom, returning the y below them."""
        for line in lines:
            self.text((x, y), line, fnt, colour)
            y += gap
        return y

    def panel(self, x, y, w, h, colour):
        self.d.rectangle([x, y, x + w, y + h], fill=colour)

    def pill(self, x, y, s, fnt, bg, fg):
        w = self.d.textlength(s, font=fnt) + 22
        self.d.rounded_rectangle([x, y, x + w, y + 30], radius=8, fill=bg)
        self.text((x + 11, y + 6), s, fnt, fg)
        return x + w + 10

    def save(self, path):
        self.img.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({os.path.getsize(path)} bytes)")


def skyline_scene(p, x0, y0, x1, y1):
    """Night skyline above the summit table: towers, lit windows,
    three leaders as coloured dots around a white table."""
    p.panel(x0, y0, x1 - x0, y1 - y0, PALETTE["sky"])
    floor = y0 + (y1 - y0) * 13 // 25
    spans = [(6, 62, 30), (52, 84, 42), (100, 118, 24), (148, 108, 38),
             (198, 96, 28), (240, 118, 44), (290, 104, 32)]
    for off, tall, wide in spans:
        top = floor - tall
        p.d.rectangle([x0 + off, top, x0 + off + wide, floor],
                      fill=(17, 30, 54))
        for wy in range(top + 10, floor - 8, 17):
            for wx in (off + 6, off + wide - 12):
                p.d.rectangle([x0 + wx, wy, x0 + wx + 6, wy + 7],
                              fill=PALETTE["gold"])
    p.d.line([(x0 + 159, y0 + 8), (x0 + 159, y0 + 26)],
             fill=(17, 30, 54), width=4)
    p.panel(x0, floor, x1 - x0, y1 - floor, (31, 54, 86))
    cx = (x0 + x1) // 2
    ty = floor + 48
    p.d.ellipse([cx - 88, ty - 16, cx + 88, ty + 16],
                fill=PALETTE["paper"])
    p.d.rectangle([cx - 9, ty + 11, cx + 9, y1 - 32], fill=PALETTE["paper"])
    for ang, colour in ((205, PALETTE["alarm"]), (270, PALETTE["gold"]),
                        (335, PALETTE["mint"])):
        px = cx + 60 * math.cos(math.radians(ang))
        py = ty - 4 + 24 * math.sin(math.radians(ang))
        p.d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=colour)
        p.d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=PALETTE["paper"])
    tag = "USA · CHINA · RUSSIA"
    f = face("sans_b", 14)
    p.text((((x0 + x1) - p.d.textlength(tag, font=f)) / 2, y1 - 25),
           tag, f, PALETTE["white"])


def rocket_icon(p, cx, cy):
    """A small rocket climbing out of its blast circle."""
    p.d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(66, 36, 42))
    p.d.polygon([(cx - 16, cy + 18), (cx + 2, cy - 22),
                 (cx + 16, cy - 10), (cx - 2, cy + 24)],
                fill=PALETTE["paper"])
    p.d.polygon([(cx + 2, cy - 22), (cx + 10, cy - 30),
                 (cx + 16, cy - 10)], fill=PALETTE["alarm"])
    p.d.polygon([(cx - 16, cy + 18), (cx - 26, cy + 26),
                 (cx - 8, cy + 26)], fill=PALETTE["amber"])
    p.d.polygon([(cx - 4, cy + 24), (cx - 12, cy + 30),
                 (cx + 2, cy + 29)], fill=PALETTE["gold"])


def bridge_icon(p, cx, cy):
    """A deck with its middle span gone, blast above, sea below."""
    p.d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(30, 58, 86))
    p.d.rectangle([cx - 21, cy - 3, cx - 7, cy + 1], fill=PALETTE["paper"])
    p.d.rectangle([cx + 7, cy - 3, cx + 21, cy + 1], fill=PALETTE["paper"])
    p.d.line([(cx - 15, cy - 3), (cx - 15, cy - 17)], fill=PALETTE["paper"],
             width=2)
    p.d.line([(cx + 15, cy - 3), (cx + 15, cy - 17)], fill=PALETTE["paper"],
             width=2)
    star = []
    for i in range(8):
        ang = math.pi * i / 4
        r = 10 if i % 2 == 0 else 5
        star.append((cx + r * math.cos(ang),
                     cy - 9 + r * math.sin(ang)))
    p.d.polygon(star, fill=PALETTE["amber"])
    p.d.ellipse([cx - 3, cy - 12, cx + 3, cy - 6], fill=PALETTE["alarm"])
    p.d.line([(cx - 5, cy + 3), (cx + 9, cy + 15)], fill=(198, 62, 46),
             width=3)
    p.d.arc([cx - 19, cy + 13, cx + 19, cy + 23], 0, 180,
            fill=(172, 207, 237), width=2)


def dome_icon(p, cx, cy):
    """A capitol dome: arch, columns, base."""
    p.d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(54, 46, 86))
    p.d.arc([cx - 17, cy - 7, cx + 17, cy + 21], 180, 360,
            fill=PALETTE["paper"], width=3)
    p.d.line([(cx - 21, cy + 7), (cx + 21, cy + 7)], fill=PALETTE["paper"],
             width=3)
    p.d.line([(cx, cy - 15), (cx, cy - 7)], fill=PALETTE["gold"], width=3)
    for px in (-13, 0, 13):
        p.d.line([(cx + px, cy + 7), (cx + px, cy + 15)],
                 fill=PALETTE["paper"], width=2)
    p.d.line([(cx - 21, cy + 16), (cx + 21, cy + 16)],
             fill=PALETTE["paper"], width=3)


def chip_icon(p, cx, cy):
    """A processor: square die, gold pins on four sides."""
    p.d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(26, 54, 46))
    for px in (-15, 0, 15):
        p.d.line([(cx + px, cy - 27), (cx + px, cy - 17)],
                 fill=PALETTE["gold"], width=3)
        p.d.line([(cx + px, cy + 17), (cx + px, cy + 27)],
                 fill=PALETTE["gold"], width=3)
        p.d.line([(cx - 27, cy + px), (cx - 17, cy + px)],
                 fill=PALETTE["gold"], width=3)
        p.d.line([(cx + 17, cy + px), (cx + 27, cy + px)],
                 fill=PALETTE["gold"], width=3)
    p.d.rectangle([cx - 17, cy - 17, cx + 17, cy + 17], fill=PALETTE["mint"])
    p.d.rectangle([cx - 9, cy - 9, cx + 9, cy + 9], fill=PALETTE["night"])


def storm_icon(p, cx, cy):
    """A cyclone: three spiral arcs around a calm eye."""
    p.d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(30, 58, 86))
    for r, start in ((18, 15), (12, 195), (7, 85)):
        p.d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 255,
                fill=PALETTE["mint"], width=3)
    p.d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=PALETTE["paper"])


def story_card(p, x, y, w, h, kicker, colour, headline, body, icon,
               date="19 NOV 2026"):
    """One news panel: icon + kicker + headline + body text."""
    p.panel(x, y, w, h, PALETTE["card"])
    icon(p, x + 44, y + 44)
    p.text((x + 82, y + 18), kicker, face("sans_b", 16), colour)
    p.text((x + 82, y + 42), date, face("sans", 14), PALETTE["dim"])
    hy = y + 76
    hy = p.para(x + 18, hy,
                split_lines(p.d, headline, face("serif_b", 28), w - 36),
                face("serif_b", 28), PALETTE["paper"], 34)
    end = p.para(x + 18, hy + 4,
                 split_lines(p.d, body, face("sans", 18), w - 36),
                 face("sans", 18), PALETTE["ink"], 24)
    assert end <= y + h - 8, f"card text overflows: {kicker} end={end}"
    return end


def mini_card(p, x, y, w, h, kicker, colour, headline, body, icon):
    """A narrower third-band panel (icon row, then headline/body)."""
    p.panel(x, y, w, h, PALETTE["card2"])
    icon(p, x + 40, y + 40)
    p.text((x + 74, y + 20), kicker, face("sans_b", 15), colour)
    p.text((x + 74, y + 42), "19 NOV", face("sans", 13), PALETTE["dim"])
    hy = y + 70
    hy = p.para(x + 15, hy,
                split_lines(p.d, headline, face("serif_b", 24), w - 30),
                face("serif_b", 24), PALETTE["paper"], 29)
    end = p.para(x + 15, hy + 3,
                 split_lines(p.d, body, face("sans", 16), w - 30),
                 face("sans", 16), PALETTE["ink"], 21)
    assert end <= y + h - 8, f"mini card overflows: {kicker} end={end}"
    return end


def build():
    p = Poster()
    d = p.d

    # ---- masthead ----
    p.y = 18
    p.centre(p.y, "THE WORLD IN ONE DAY", face("serif_b", 44),
             PALETTE["paper"])
    p.y += 56
    p.panel(MARGIN, p.y, CW, 32, PALETTE["alarm"])
    p.centre(p.y + 4, "THURSDAY · 19 NOVEMBER 2026",
             face("sans_b", 24), PALETTE["white"])
    p.y += 46

    # ---- lead story: Shenzhen ----
    lead_top, lead_h = p.y, 330
    p.panel(MARGIN, lead_top, CW, lead_h, PALETTE["card"])
    lx, ly = MARGIN + 22, lead_top + 12
    p.text((lx, ly), "SHENZHEN — THE DAY'S BIG STORY",
           face("sans_b", 19), PALETTE["gold"])
    ly += 30
    ly = p.para(lx, ly, ["THREE PRESIDENTS,", "ONE TABLE"],
                face("serif_b", 46), PALETTE["paper"], 54)
    ly += 6
    ly = p.para(lx, ly,
                split_lines(d, "Trump, Xi & Putin meet today — the "
                            "first US–China–Russia trilateral, with "
                            "Ukraine, Iran and Taiwan on the agenda.",
                            face("sans", 20), 545),
                face("sans", 20), PALETTE["ink"], 27)
    skyline_scene(p, 622, lead_top + 18, SIZE[0] - MARGIN - 18,
                  lead_top + 252)
    p.text((622, lead_top + 258), "Shenzhen hosts the APEC leaders' "
           "summit.", face("sans", 14), PALETTE["dim"])
    chip_y = lead_top + lead_h - 42
    assert ly <= chip_y - 6, f"lead text runs into chips: ly={ly}"
    cx = MARGIN + 22
    f_chip = face("sans_b", 16)
    cx = p.pill(cx, chip_y, "FIRST-EVER TRILATERAL", f_chip,
                PALETTE["alarm"], PALETTE["white"])
    cx = p.pill(cx, chip_y, "APEC · SHENZHEN", f_chip,
                PALETTE["slate"], PALETTE["white"])
    cx = p.pill(cx, chip_y, "XI MET PUTIN WEDNESDAY", f_chip,
                PALETTE["slate"], PALETTE["white"])
    assert cx <= SIZE[0] - MARGIN, f"chips overflow: cx={cx}"
    p.y = lead_top + lead_h + 12

    # ---- middle band: Gulf + Kerch ----
    band_h = 228
    half = (CW - 16) // 2
    story_card(p, MARGIN, p.y, half, band_h,
               "MIDDLE EAST — ESCALATION", PALETTE["alarm"],
               "US–Iran fire widens across the Gulf",
               "US jets hit an IRGC missile site on Qeshm Island. "
               "Iran answers with drones on US bases in Bahrain & "
               "Kuwait.", rocket_icon)
    story_card(p, MARGIN + half + 16, p.y, half, band_h,
               "UKRAINE WAR", PALETTE["gold"],
               "Kerch Bridge arch is down",
               "A 227-m road arch fell into the strait. Moscow vows "
               "to rebuild as Russia hits Kyiv's Dnipro bridges.",
               bridge_icon)
    p.y += band_h + 12

    # ---- third band: Speaker / Nvidia / Cyclone ----
    band2_h = 184
    col_w = (CW - 32) // 3
    mini_card(p, MARGIN, p.y, col_w, band2_h,
              "UNITED STATES", PALETTE["gold"],
              "Jeffries for Speaker",
              "Democrats nominate Hakeem Jeffries — set to be the "
              "first Black Speaker.", dome_icon)
    mini_card(p, MARGIN + col_w + 16, p.y, col_w, band2_h,
              "TECH", PALETTE["mint"],
              "Nvidia's chief is out",
              "Founder Jensen Huang resigns. Acting chief Kress "
              "halts H-chip shipments to China.", chip_icon)
    mini_card(p, MARGIN + 2 * (col_w + 16), p.y, col_w, band2_h,
              "DISASTER", PALETTE["alarm"],
              "Akvan nears India",
              "Akvan bears down on the east coast, set to cross "
              "between Machilipatnam and Puri.", storm_icon)
    p.y += band2_h + 12

    # ---- ticker + footer ----
    p.panel(MARGIN, p.y, CW, 40, (122, 28, 24))
    ticker = ("GTA VI LAUNCHES TODAY · VOYAGER 1 HITS LIGHT-DAY "
              "· FED EYES MORE HIKES")
    assert d.textlength(ticker, font=face("sans_b", 20)) <= CW - 8, \
        "ticker too wide"
    p.centre(p.y + 9, ticker, face("sans_b", 20), PALETTE["white"])
    p.y += 52
    extra = ("ISRAEL PUSHES INTO CENTRAL GAZA · AUSTRALIA SANCTIONS "
             "SETTLERS · MOLDOVA SUMMONS RUSSIAN ENVOY")
    p.centre(p.y, extra, face("sans_b", 15), PALETTE["dim"])
    p.y += 26
    p.centre(p.y, "Top stories of Thursday, 19 November 2026 — "
             "verified against multiple reports of the day",
             face("sans", 14), PALETTE["dim"])
    p.y += 20
    assert p.y <= SIZE[1] - 6, f"layout overflow: y={p.y}"
    return p


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out)


if __name__ == "__main__":
    main()
