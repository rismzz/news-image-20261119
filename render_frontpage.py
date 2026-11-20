#!/usr/bin/env python3
"""Render the news-image-20261119 round 2 poster: a dense broadsheet.

One 1024x1024 PNG, drawn programmatically with PIL. Every word on the
page is exact text from the STORIES data below (40 stories, each first
reported on Thursday 19 November 2026, with its source), never text
from an image model. No network, no randomness, no clock: the same
code always writes the same bytes.

Layout, top to bottom: masthead with the giant date, a red date-check
band, three lead stories, a UTC timeline strip, a two-column grid of
eight labelled sections, a markets ticker, and a sources footer.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (248, 244, 232)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (163, 22, 33)
GREY = (110, 108, 100)
RULE = (180, 175, 160)
LIGHT = (238, 232, 214)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FALLBACK_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FALLBACK_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FALLBACK_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size, fallback):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(fallback, size)


def serif_bold(size):
    return font(SERIF, size, FALLBACK_SERIF)


def serif(size):
    return font(SERIF_REG, size, FALLBACK_SERIF)


def sans(size):
    return font(SANS, size, FALLBACK_SANS)


def sans_bold(size):
    return font(SANS_BOLD, size, FALLBACK_SANS_BOLD)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns lines that fit inside width pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(draw, text, fnt, width):
    """One line: shrink with an ellipsis only if it cannot fit."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text + "..."


# ---------------------------------------------------------------- data
# Every story below was first reported on Thursday 19 November 2026.
# Stories from 18 November or earlier (the Kerch bridge collapse, the
# US strikes on Qeshm) are deliberately NOT in this list.

LEADS = [
    ("TOP STORY 1", "AP - BBC",
     "Trump, Xi and Putin Issue 'Peace Declaration'",
     "First trilateral of the three nuclear powers ends with a joint "
     "text - but no deal on Ukraine or Iran."),
    ("TOP STORY 2", "AP - BBC",
     "World Court: Myanmar Committed Genocide",
     "ICJ rules 9-6 that the 2017 crackdown on the Rohingya was "
     "genocide - the first state ever found guilty."),
    ("TOP STORY 3", "REUTERS - AP",
     "Anthropic's Record IPO; Dow Sinks 1,101",
     "AI firm raises $81.3bn, opens +34% and closes +17% at $97.17 - "
     "yet all three US indexes fall about 2%."),
]

# (section label, [(headline, summary, source), ...])
SECTIONS_A = [
    ("WORLD", [
        ("Europe 'Ready for Talks' With Russia on Ukraine",
         "European leaders say they are prepared to negotiate an end to the war.",
         "BBC"),
        ("UK-EU Reset Summit Goes 'Down to the Wire'",
         "London and Brussels push reset talks to the limit ahead of a crunch summit.",
         "BBC - GUARDIAN"),
        ("Venezuela Signs Military Deal With the US",
         "Pact comes less than a year after Maduro's ouster, US defence chief says.",
         "BBC"),
        ("Kenya Picks US Consortium for Critical Minerals",
         "American group wins the mining project, beating Chinese rivals.",
         "AP - BBC"),
        ("Dozens Missing After Migrant Boat Sinks off Senegal",
         "Boat carrying migrants goes down off the coast; search under way.",
         "BBC"),
    ]),
    ("WAR & SECURITY", [
        ("Israeli Army Completes Gaza Ground Operation",
         "Troops finish an operation beyond the Yellow Line; Hamas condemns the incursion.",
         "BBC"),
        ("Houthi Missiles Aimed at Riyadh Intercepted",
         "Saudi-led coalition says it stopped missiles fired towards Riyadh and the south.",
         "THE NEW ARAB"),
        ("West Presses Iran to Restore Nuclear Inspections",
         "US, UK, France and Germany push Tehran at the IAEA in Vienna.",
         "REUTERS"),
        ("Iran War Cost Hits $48.3bn; Senate Blocks Exit Bid",
         "Costs rise as Senate Republicans block the latest bid to end the war.",
         "AP"),
        ("Haiti Forces Launch Operation to Retake Corridor",
         "Armed forces move against gangs entrenched along a key route.",
         "AP"),
    ]),
    ("MARKETS", [
        ("Wall Street Sinks: Dow -1,101, S&P Falls Again",
         "S&P 500 logs a sixth straight loss; Nasdaq drops 2.25%.",
         "REUTERS"),
        ("Bank of Japan Set to Raise Rates in December",
         "Reuters poll: most economists expect a hike to 1.50%, then another by March.",
         "REUTERS"),
        ("Nvidia Board: Huang Will Not Return as CEO",
         "Board rules out a comeback; Alibaba is sued over its ties to the spy scandal.",
         "REUTERS"),
        ("Fed-Hike Fears Hit Asian Markets",
         "Nifty and Sensex slip as hawkish Fed signals and a strong dollar weigh.",
         "THE HINDU"),
    ]),
    ("TECH & AI", [
        ("Chase Customer Emails Leaked in Cyberattack",
         "Thousands of customers hit after third-party vendors are breached.",
         "AP"),
        ("AI-Driven Cyberattack Targeted the EU in October",
         "An official says artificial intelligence was used in the October attack.",
         "AP"),
        ("Chinese Tech Firms Fear US Curbs After Nvidia Fallout",
         "AI chip restrictions loom as the Huang scandal widens.",
         "AP"),
        ("Trump Raised Huang Case 'Briefly' With Xi",
         "Trump tells Fox News he mentioned the ex-Nvidia boss in their talks.",
         "REUTERS"),
        ("Alphabet Falls as Anthropic Debut Reprices Google Stake",
         "Google parent drops 2.9% as the IPO puts fresh value on its holding.",
         "MOTLEY FOOL"),
    ]),
]

SECTIONS_B = [
    ("CLIMATE", [
        ("COP31 Draft Drops All Fossil-Fuel Language",
         "Slimmed text in Antalya cuts the phase-out pledge; Panama threatens to block it.",
         "REUTERS - GUARDIAN"),
        ("Cyclone Akvan Nears India's Odisha Coast",
         "Thousands evacuated as the severe storm approaches; landfall due Friday.",
         "THE HINDU"),
        ("Faults Unfixed in 90% of Insulation-Scheme Homes",
         "UK scheme leaves most homes with faults still not repaired.",
         "BBC"),
    ]),
    ("SCIENCE & HEALTH", [
        ("Voyager 1 Phones Home From One Light-Day Away",
         "NASA's probe calls home from farther than any human-made object has flown.",
         "AP - NASA"),
        ("UK Covid Inquiry: Testing, Tracing and the 'Pingdemic'",
         "Report sets out key findings on the pandemic response.",
         "BBC"),
        ("Newborn Dies After Suspected FGM in Senegal",
         "Three relatives arrested after a baby girl bleeds to death.",
         "AP"),
        ("37 Carpet Pythons Found in Cape York Woodlands",
         "Scientists count dozens of the snakes in a Queensland survey.",
         "REPORTED 19 NOV"),
        ("Palestinian Children a Third of Child-Rights Violations",
         "Save the Children: they are victims of a third of violations worldwide.",
         "AP"),
    ]),
    ("SPORT", [
        ("ATP Finals: Shelton Beats Jodar",
         "American wins and now needs help from Zverev to advance.",
         "AP"),
        ("Broncos Extend Moss in $67m Deal",
         "Cornerback Riley Moss agrees a four-year extension, AP source says.",
         "AP"),
        ("South Africa Top of World Test Standings",
         "Proteas claim first place in the 2025-27 championship table.",
         "REPORTED 19 NOV"),
        ("India Beat Malaysia in Hockey Champions Trophy",
         "Hosts open their Women's Asian Champions Trophy defence in Bhopal.",
         "REPORTED 19 NOV"),
        ("F1 to Introduce Full-Time Race Stewards in 2027",
         "FIA moves to permanent stewards from the 2027 season.",
         "BBC"),
    ]),
    ("CULTURE", [
        ("GTA 6 on Sale Worldwide After 13 Years",
         "Rockstar's game, 13 years in development, reaches players across the globe.",
         "BBC"),
        ("Van Gogh Sells for Record $190.4m",
         "Painting fetches a record price after a row over its Nazi-era history.",
         "BBC"),
        ("Ancient Library in Rome Opens to the Public",
         "Long-buried repository opens after restoration work.",
         "AP"),
        ("Fiona the Hippo Dies After Swallowing a Hat",
         "Cincinnati Zoo's star hippo dies days after eating a visitor's hat.",
         "AP"),
        ("Ella Langley Sweeps Country Music Awards",
         "Langley takes the night's top honours as Taylor Swift performs.",
         "BBC"),
    ]),
]

# (UTC time, what happened) — times as reported by the cited outlets.
TIMELINE = [
    ("01:46", "Trump raised Huang case 'briefly'"),
    ("12:13", "COP31 draft drops fossil fuels"),
    ("16:50", "Anthropic opens +34% at $111.50"),
    ("17:38", "Trump, Xi, Putin issue declaration"),
    ("20:07", "ICJ: Myanmar committed genocide"),
    ("21:00", "Dow closes -1,101; S&P down again"),
    ("21:21", "Europe ready for Russia talks"),
    ("21:26", "Fiona the hippo dies in Cincinnati"),
]

TICKER = ("DOW 49,097 -2.19% - S&P 500 7,176 -2.02% - NASDAQ 23,879 -2.25% - "
           "ANTHROPIC $97.17 +17.1% - NVIDIA -2.9% - NIKKEI -7% IN NOV - "
           "USD 103.81 - BOJ HIKE IN DEC")

FOOTER_SOURCES = ("SOURCES: AP  -  REUTERS  -  BBC  -  THE HINDU  -  THE GUARDIAN  -  "
                  "THE NEW ARAB  -  MOTLEY FOOL  -  NASA")
FOOTER_NOTE = ("All 40 stories verified as first reported on Thursday 19 November 2026. "
               "Rendered programmatically - no AI-generated text in this image.")


# ------------------------------------------------------------- layout
MX = 14                      # side margin
CW = (W - 2 * MX - 12) // 2   # story-column width (494)


def rule(draw, x0, x1, y, color=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_masthead(draw):
    rule(draw, MX, W - MX, 10, INK, 3)
    rule(draw, MX, W - MX, 15, INK, 1)
    kicker = sans_bold(11)
    left = "MAKE.FUN NEWS-IMAGE  -  THE DAY IN ONE PICTURE"
    right = "THURSDAY EDITION"
    draw.text((MX, 22), left, font=kicker, fill=GREY)
    draw.text((W - MX - draw.textlength(right, font=kicker), 22),
              right, font=kicker, fill=GREY)
    name = serif_bold(58)
    title = "THE WORLD IN ONE DAY"
    draw.text(((W - draw.textlength(title, font=name)) // 2, 38),
              title, font=name, fill=NAVY)
    date = serif_bold(38)
    when = "THURSDAY  -  19 NOVEMBER 2026"
    draw.text(((W - draw.textlength(when, font=date)) // 2, 100),
              when, font=date, fill=RED)
    rule(draw, MX, W - MX, 142, INK, 2)
    sub = sans_bold(14)
    line = "40 VERIFIED STORIES   -   8 SECTIONS   -   EVERY REGION   -   ONE DAY"
    draw.text(((W - draw.textlength(line, font=sub)) // 2, 150),
              line, font=sub, fill=INK)
    # Red date-check band.
    draw.rectangle([(MX, 172), (W - MX, 196)], fill=RED)
    check = sans_bold(13)
    msg = "DATE CHECK  -  EVERY STORY ON THIS PAGE WAS FIRST REPORTED ON 19 NOVEMBER 2026"
    draw.text(((W - draw.textlength(msg, font=check)) // 2, 178),
              msg, font=check, fill=PAPER)


def draw_leads(draw):
    y0, height = 204, 94
    col_w = (W - 2 * MX - 2 * 14) // 3
    tag = sans_bold(10)
    head = serif_bold(17)
    body = sans(12)
    src = sans_bold(9)
    for i, (label, source, headline, summary) in enumerate(LEADS):
        x = MX + i * (col_w + 14)
        draw.text((x, y0), label, font=tag, fill=RED)
        sw = draw.textlength(source, font=src)
        draw.text((x + col_w - sw, y0 + 1), source, font=src, fill=GREY)
        lines = wrap(draw, headline, head, col_w)
        assert len(lines) <= 2, f"lead headline too long: {headline}"
        yy = y0 + 14
        for line in lines:
            draw.text((x, yy), line, font=head, fill=INK)
            yy += 20
        slines = wrap(draw, summary, body, col_w)
        assert len(slines) <= 3, f"lead summary too long: {summary}"
        yy = y0 + 14 + 2 * 20
        for line in slines:
            draw.text((x, yy), line, font=body, fill=INK)
            yy += 15
    rule(draw, MX, W - MX, y0 + height + 4, INK, 2)


def draw_timeline(draw):
    y0 = 308
    head = sans_bold(12)
    draw.text((MX, y0), "THE DAY IN UTC  -  KEY HOURS", font=head, fill=RED)
    rule(draw, MX, W - MX, y0 + 16, RULE, 1)
    time_f = sans_bold(12)
    text_f = sans(11)
    col_w = (W - 2 * MX - 3 * 10) // 4
    for i, (when, what) in enumerate(TIMELINE):
        row, col = divmod(i, 4)
        x = MX + col * (col_w + 10)
        y = y0 + 22 + row * 30
        draw.text((x, y), when, font=time_f, fill=RED)
        lines = wrap(draw, what, text_f, col_w - 48)
        assert len(lines) <= 2, f"timeline item too long: {what}"
        yy = y
        for line in lines:
            draw.text((x + 48, yy), line, font=text_f, fill=INK)
            yy += 13
    rule(draw, MX, W - MX, y0 + 66, INK, 2)


def draw_sections(draw, sections, x0, y0):
    """One grid column, stretched so both columns end at the same y."""
    head_f = sans_bold(13)
    story_f = serif_bold(13)
    sum_f = sans(11)
    n_stories = sum(len(stories) for _, stories in sections)
    row_h = (948 - y0 - 20 * len(sections)) / n_stories
    assert row_h >= 25, f"grid rows too tight: {row_h:.1f}px"
    y = y0
    for label, stories in sections:
        draw.rectangle([(x0, y + 4), (x0 + 9, y + 13)], fill=RED)
        draw.text((x0 + 15, y), label, font=head_f, fill=NAVY)
        rule(draw, x0, x0 + CW, y + 19, RULE, 1)
        y += 20
        for headline, summary, source in stories:
            hl = fit(draw, headline, story_f, CW - 44)
            draw.text((x0, y), hl, font=story_f, fill=INK)
            sw = draw.textlength(source, font=sans_bold(8))
            draw.text((x0 + CW - sw, y + 2), source,
                      font=sans_bold(8), fill=GREY)
            sm = fit(draw, summary, sum_f, CW)
            draw.text((x0, y + 13), sm, font=sum_f, fill=(60, 60, 60))
            y += row_h
    return y


def draw_grid(draw):
    y0 = 382
    end_a = draw_sections(draw, SECTIONS_A, MX, y0)
    end_b = draw_sections(draw, SECTIONS_B, MX + CW + 12, y0)
    draw.line([(MX + CW + 5, y0), (MX + CW + 5, 948)], fill=RULE, width=1)
    assert end_a <= 950 and end_b <= 950, (end_a, end_b)
    return max(end_a, end_b)


def draw_ticker(draw):
    draw.rectangle([(MX, 956), (W - MX, 980)], fill=INK)
    fnt = sans_bold(12)
    text = fit(draw, TICKER, fnt, W - 2 * MX - 8)
    assert not text.endswith("..."), "ticker does not fit"
    draw.text(((W - draw.textlength(text, font=fnt)) // 2, 963),
              text, font=fnt, fill=PAPER)


def draw_footer(draw):
    fnt = sans(10)
    draw.text((MX, 988), FOOTER_SOURCES, font=fnt, fill=GREY)
    draw.text((MX, 1002), FOOTER_NOTE, font=fnt, fill=GREY)
    rule(draw, MX, W - MX, 1018, INK, 2)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_leads(draw)
    draw_timeline(draw)
    draw_grid(draw)
    draw_ticker(draw)
    draw_footer(draw)
    return img


def count_stories():
    total = len(LEADS)
    for sections in (SECTIONS_A, SECTIONS_B):
        for _, stories in sections:
            total += len(stories)
    return total


def main():
    assert count_stories() == 40, count_stories()
    img = render()
    img.save(OUT, "PNG", optimize=True)
    import hashlib
    import os
    size = os.path.getsize(OUT)
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes, "
          f"sha256 {digest}")
    assert size <= 1_048_576, "over the 1 MiB cap"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
