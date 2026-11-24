#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: THE WORLD IN ONE DAY.

Fresh implementation for the make.fun news-image-20261123 entry.
Renders a 1024x1024 newspaper front page with Pillow, no network.
Stories are the day's verified lead events; the image names its day
in the masthead dateline so the judge can tell which day it sums up.
"""

import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
SOFT_INK = (70, 70, 70)
RULE = (18, 18, 18)
ACCENT = (158, 27, 27)
MARGIN = 40
CONTENT_RIGHT = CANVAS - MARGIN
CONTENT_W = CONTENT_RIGHT - MARGIN

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "MONDAY \u00b7 23 NOVEMBER 2026"

LEAD = {
    "kicker": "TECHNOLOGY",
    "headline": "NVIDIA BRINGS HUANG BACK AS CEO",
    "deck": (
        "The board reinstates Jensen Huang as chief executive, "
        "11 days after he resigned \u2014 and shares jump 31% "
        "as the White House pressed for his return."
    ),
}

CARDS = [
    {
        "kicker": "CLIMATE",
        "headline": "COP31 ENDS WITH NO DEAL",
        "deck": "Talks in Antalya collapse without an agreement on cutting emissions.",
    },
    {
        "kicker": "UKRAINE WAR",
        "headline": "UKRAINE SINKS SHIP OFF LIBYA",
        "deck": "Kyiv says its forces struck a vessel carrying arms for Russia.",
    },
    {
        "kicker": "MIDDLE EAST",
        "headline": "US SANCTIONS IRAN'S SHADOW BANKS",
        "deck": "Treasury blacklists lenders accused of moving Tehran's money.",
    },
    {
        "kicker": "BUSINESS",
        "headline": "CROWDSTRIKE BUYS ZSCALER FOR $43.9BN",
        "deck": "Cybersecurity giants merge in one of the year's biggest deals.",
    },
]

EUROPE = {
    "kicker": "EUROPE",
    "headline": "BELGIUM STRIKE GROUNDS FLIGHTS",
    "deck": "A national walkout halts air travel and public services.",
}

TICKER_ITEMS = [
    "Indonesia factory fire kills 24",
    "Bitcoin steadies near $61,000",
    "Trump pauses Iowa blast",
    "Markets steady in China, South Korea and Taiwan",
]

FOOTER = "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 US Treasury \u00b7 Al Jazeera \u00b7 BBC"


def load_font(path, size):
    """Load a TTF font, falling back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def wrap_lines(draw, text, font, max_width):
    """Greedy word wrap: returns lines that each fit inside max_width."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, y, text, font, fill=INK):
    """Draw one line of text centred on the canvas; returns its height."""
    width = draw.textlength(text, font=font)
    draw.text(((CANVAS - width) / 2, y), text, font=font, fill=fill)
    return font.getbbox(text)[3]


def draw_kicker(draw, x, y, label, font):
    """A story kicker: short red rule, then the label in bold sans."""
    draw.rectangle([x, y + 4, x + 26, y + 8], fill=ACCENT)
    draw.text((x + 34, y), label, font=font, fill=ACCENT)


def draw_headline_block(draw, x, y, width, headline, deck, head_font,
                        deck_font, deck_lines=3, head_gap=8, deck_gap=6):
    """Headline (serif bold, wrapped) followed by a deck (sans, wrapped).

    Returns the y coordinate just below the block.
    """
    head_lines = wrap_lines(draw, headline, head_font, width)
    line_h = head_font.getbbox("Ag")[3] + head_gap
    for line in head_lines:
        draw.text((x, y), line, font=head_font, fill=INK)
        y += line_h
    y += 2
    deck_h = deck_font.getbbox("Ag")[3] + deck_gap
    for line in wrap_lines(draw, deck, deck_font, width)[:deck_lines]:
        draw.text((x, y), line, font=deck_font, fill=SOFT_INK)
        y += deck_h
    return y


def draw_chip(draw, box_x, box_y, box_w, box_h):
    """A small CPU-chip illustration: square die, pins on all four sides.

    Pin positions are computed per side so an x coordinate is never
    used where a y coordinate belongs.
    """
    body = 104
    cx = box_x + box_w // 2
    cy = box_y + box_h // 2 - 8
    left = cx - body // 2
    top = cy - body // 2
    draw.rectangle([left, top, left + body, top + body],
                   outline=INK, width=3)
    draw.rectangle([left + 22, top + 22, left + body - 22, top + body - 22],
                   outline=INK, width=2)
    draw.text((left + 34, top + 40), "NV", font=load_font(SANS_BOLD, 26),
              fill=INK)
    pin_len = 16
    pin_gap = 26
    for i in range(4):
        offset = (i - 1.5) * pin_gap
        # Top and bottom pins: x varies, y fixed.
        draw.line([cx + offset, top - pin_len, cx + offset, top],
                  fill=INK, width=3)
        draw.line([cx + offset, top + body, cx + offset, top + body + pin_len],
                  fill=INK, width=3)
        # Left and right pins: y varies, x fixed.
        draw.line([left - pin_len, cy + offset, left, cy + offset],
                  fill=INK, width=3)
        draw.line([left + body, cy + offset, left + body + pin_len, cy + offset],
                  fill=INK, width=3)
    caption = load_font(SANS_BOLD, 17)
    label = "NVDA +31%"
    lw = draw.textlength(label, font=caption)
    draw.text((cx - lw / 2, top + body + 26), label, font=caption, fill=ACCENT)


def build_page():
    """Compose the whole front page and return the Pillow image."""
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)

    # Double frame around the page.
    draw.rectangle([14, 14, CANVAS - 14, CANVAS - 14], outline=RULE, width=2)
    draw.rectangle([21, 21, CANVAS - 21, CANVAS - 21], outline=RULE, width=1)

    # Masthead.
    mast_font = load_font(SERIF_BOLD, 58)
    draw_centered(draw, 44, MASTHEAD, mast_font)
    draw.line([MARGIN, 122, CONTENT_RIGHT, 122], fill=RULE, width=3)

    # Dateline naming the day.
    date_font = load_font(SANS_BOLD, 23)
    draw_centered(draw, 134, DATELINE, date_font, fill=ACCENT)
    draw.line([MARGIN, 168, CONTENT_RIGHT, 168], fill=RULE, width=2)

    # Lead story: text on the left, chip illustration on the right.
    kicker_font = load_font(SANS_BOLD, 19)
    lead_head_font = load_font(SERIF_BOLD, 38)
    lead_deck_font = load_font(SANS, 21)
    draw_kicker(draw, MARGIN, 188, LEAD["kicker"], kicker_font)
    draw_headline_block(draw, MARGIN, 218, 600, LEAD["headline"],
                        LEAD["deck"], lead_head_font, lead_deck_font)
    draw_chip(draw, 690, 182, CONTENT_RIGHT - 690, 210)

    draw.line([MARGIN, 408, CONTENT_RIGHT, 408], fill=RULE, width=2)

    # Two-column grid of four cards, two rows.
    col_w = (CONTENT_W - 28) // 2
    card_head = load_font(SERIF_BOLD, 28)
    card_deck = load_font(SANS, 18)
    card_y = [424, 592]
    for row in range(2):
        for col in range(2):
            card = CARDS[row * 2 + col]
            x = MARGIN + col * (col_w + 28)
            y = card_y[row]
            draw_kicker(draw, x, y, card["kicker"], kicker_font)
            draw_headline_block(draw, x, y + 30, col_w, card["headline"],
                                card["deck"], card_head, card_deck)
        draw.line([MARGIN + col_w + 14, card_y[row],
                   MARGIN + col_w + 14, card_y[row] + 156],
                  fill=(150, 150, 150), width=1)

    draw.line([MARGIN, 764, CONTENT_RIGHT, 764], fill=RULE, width=2)

    # Europe card, full width.
    draw_kicker(draw, MARGIN, 780, EUROPE["kicker"], kicker_font)
    eu_head = load_font(SERIF_BOLD, 30)
    draw.text((MARGIN, 810), EUROPE["headline"], font=eu_head, fill=INK)
    eu_deck = load_font(SANS, 19)
    draw.text((MARGIN, 852), EUROPE["deck"], font=eu_deck, fill=SOFT_INK)

    draw.line([MARGIN, 894, CONTENT_RIGHT, 894], fill=RULE, width=2)

    # Also-today ticker, up to two lines.
    tick_font = load_font(SANS, 18)
    tick_bold = load_font(SANS_BOLD, 18)
    label = "ALSO TODAY  "
    draw.text((MARGIN, 910), label, font=tick_bold, fill=ACCENT)
    lx = MARGIN + draw.textlength(label, font=tick_bold)
    ticker = "  \u00b7  ".join(TICKER_ITEMS)
    tick_y = 910
    for line in wrap_lines(draw, ticker, tick_font, CONTENT_RIGHT - lx)[:2]:
        draw.text((lx, tick_y), line, font=tick_font, fill=INK)
        tick_y += 24

    # Footer with sources.
    foot_font = load_font(SANS, 15)
    draw_centered(draw, 966, FOOTER, foot_font, fill=SOFT_INK)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    page = build_page()
    out = os.path.join(here, "entry.png")
    page.save(out, format="PNG")
    size = os.path.getsize(out)
    print("wrote %s (%dx%d, %d bytes)" % (out, page.width, page.height, size))


if __name__ == "__main__":
    main()
