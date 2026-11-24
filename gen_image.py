#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up Monday 23 November 2026.

Local build tool only (needs Pillow, which the sandbox does not have): it draws
the image once, and main.ts ships the finished PNG. Run:
    python3 gen_image.py            # writes entry.png next to this file
All facts were checked against Reuters, AP, AFP, Al Jazeera, BBC and
Investopedia reporting on 23 November 2026; see SOURCES in the README.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (16, 16, 16)
NAVY = (15, 35, 64)
GOLD = (217, 164, 65)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, box, color):
    """Small flat icon drawn with primitives. box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "chip":  # chip
        draw.rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], fill=color)
        draw.rectangle([x0 + 22, y0 + 22, x1 - 22, y1 - 22], fill=PAPER)
        for i in range(3):
            t = x0 + 20 + i * 12
            u = y0 + 20 + i * 12
            draw.line([t, y0 + 4, t, y0 + 12], fill=color, width=3)
            draw.line([t, y1 - 12, t, y1 - 4], fill=color, width=3)
            draw.line([x0 + 4, u, x0 + 12, u], fill=color, width=3)
            draw.line([x1 - 12, u, x1 - 4, u], fill=color, width=3)
    elif kind == "climate":  # sun over waves
        draw.ellipse([cx - 14, y0 + 6, cx + 14, y0 + 34], fill=color)
        for dx, dy in [(0, -6), (22, -2), (-22, -2), (16, 14), (-16, 14)]:
            draw.line([cx + dx, y0 + 2 + dy, cx + dx, y0 + 8 + dy], fill=color, width=3)
        for yy in (y1 - 20, y1 - 10):
            draw.arc([x0 + 4, yy - 8, x1 - 4, yy + 8], 0, 180, fill=color, width=4)
    elif kind == "drone":  # quadcopter drone
        draw.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], fill=color)
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = cx + sx * 20, cy + sy * 16
                draw.line([cx, cy, px, py], fill=color, width=3)
                draw.ellipse([px - 9, py - 4, px + 9, py + 4], outline=color, width=3)
    elif kind == "globe":  # globe
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=color, width=4)
        draw.ellipse([cx - 12, y0 + 4, cx + 12, y1 - 4], outline=color, width=3)
        draw.line([x0 + 4, cy, x1 - 4, cy], fill=color, width=3)
        draw.arc([x0 + 4, y0 + 14, x1 - 4, y1 - 14], 200, 340, fill=color, width=3)
    elif kind == "shield":  # shield with check
        draw.polygon([(x0 + 8, y0 + 6), (x1 - 8, y0 + 6), (x1 - 8, y0 + 28),
                      (cx, y1 - 6), (x0 + 8, y0 + 28)], fill=color)
        draw.line([cx - 12, cy + 2, cx - 3, cy + 11, cx + 13, cy - 9], fill=WHITE, width=5)
    elif kind == "plane":  # top-view aeroplane
        draw.rounded_rectangle([cx - 7, y0 + 6, cx + 7, y1 - 6], 7, fill=color)
        draw.polygon([(cx - 3, y0 + 2), (cx + 3, y0 + 2), (cx, y0 + 10)], fill=color)
        draw.rectangle([x0 + 2, cy - 12, x1 - 2, cy - 2], fill=color)
        draw.rectangle([x0 + 12, y1 - 16, x1 - 12, y1 - 8], fill=color)


CARDS = [
    ("TECH", (15, 35, 64), "chip",
     "HUANG IS BACK AT NVIDIA",
     "Reinstated as CEO 11 days after quitting in scandal; shares jump 31% "
     "and lift the Nasdaq 6.5% and the S&P 500 4.7%."),
    ("CLIMATE", (14, 122, 110), "climate",
     "COP31 ENDS WITH NO DEAL",
     "In Antalya, the EU rejects a final text silent on fossil fuels; the "
     "longest climate summit on record collapses."),
    ("WAR", (166, 58, 46), "drone",
     "UKRAINE SINKS SHIP OFF LIBYA",
     "Zelenskyy says seven sea drones sank the corvette Merkury and hit the "
     "cargo ship Angara; NATO meets over Poland."),
    ("MIDDLE EAST", (36, 86, 166), "globe",
     "US SANCTIONS IRAN'S SHADOW BANKS",
     "Treasury hits 2 dozen-plus exchange houses and front firms; Iran vows "
     "to counter a US Hormuz blockade."),
    ("BUSINESS", (178, 91, 9), "shield",
     "CROWDSTRIKE BUYS ZSCALER, $43.9BN",
     "All-stock cybersecurity mega-deal announced on Monday as cyber "
     "threats mount."),
    ("EUROPE", (108, 63, 181), "plane",
     "BELGIUM GROUNDED BY STRIKE",
     "A national anti-austerity strike shuts air traffic control; 404 "
     "flights axed at Brussels, 50,000+ passengers hit."),
]

TICKER = ("ALSO TODAY:  Indonesia fire kills 24  \u00b7  Bitcoin steadies near $61,000  "
          "\u00b7  Trump pauses Iowa blast  \u00b7  Asia steps in to steady markets")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=3)
    # masthead
    d.rectangle([24, 24, W - 24, 168], fill=NAVY)
    f_title = font(SERIF, 62)
    f_date = font(SANS_B, 34)
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=f_title, fill=WHITE, anchor="ma")
    d.text((W // 2, 128), "MONDAY  \u00b7  23 NOVEMBER 2026", font=f_date, fill=GOLD, anchor="ma")
    # sub-deck
    f_sub = font(SERIF_IT, 23)
    d.text((W // 2, 182), "Six stories that defined the day", font=f_sub, fill=GREY, anchor="ma")
    d.line([W // 2 - 120, 214, W // 2 + 120, 214], fill=GOLD, width=3)

    # grid of cards: 2 cols x 3 rows
    gx, gy, gw, gh, gap = 24, 226, 476, 222, 12
    f_kick = font(SANS_B, 17)
    f_head = font(SANS_B, 28)
    f_deck = font(SANS, 19)
    for i, (kicker, color, icon, head, deck) in enumerate(CARDS):
        cx = gx + (i % 2) * (gw + gap)
        cy = gy + (i // 2) * (gh + gap)
        d.rectangle([cx, cy, cx + gw, cy + gh], fill=WHITE, outline=(200, 192, 172), width=2)
        d.rectangle([cx, cy, cx + gw, cy + 6], fill=color)
        # kicker tag
        kw = d.textlength(kicker, font=f_kick) + 20
        d.rectangle([cx + 14, cy + 18, cx + 14 + kw, cy + 44], fill=color)
        d.text((cx + 24, cy + 31), kicker, font=f_kick, fill=WHITE, anchor="lm")
        # icon top-right
        draw_icon(d, icon, (cx + gw - 78, cy + 16, cx + gw - 14, cy + 80), color)
        # headline (max 2 lines; keep clear of the icon zone at top-right)
        lines = wrap(d, head, f_head, gw - 32 - 88)
        y = cy + 56
        for ln in lines[:2]:
            d.text((cx + 16, y), ln, font=f_head, fill=INK)
            y += 35
        # deck (max 3 lines)
        dlines = wrap(d, deck, f_deck, gw - 32)
        y = cy + 56 + 35 * min(len(lines), 2) + 6
        for ln in dlines[:3]:
            d.text((cx + 16, y), ln, font=f_deck, fill=(60, 60, 60))
            y += 25

    # ticker strip (shrink the font until the line fits the strip)
    ty = gy + 3 * gh + 2 * gap + 12  # 928
    d.rectangle([24, ty, W - 24, ty + 44], fill=NAVY)
    tick_size = 18
    while tick_size > 12:
        f_tick = font(SANS_B, tick_size)
        if d.textlength(TICKER, font=f_tick) <= 940:
            break
        tick_size -= 1
    d.text((W // 2, ty + 22), TICKER, font=f_tick, fill=WHITE, anchor="mm")
    # footer
    f_foot = font(SANS, 14)
    d.text((W // 2, H - 38), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 Investopedia \u00b7 23 Nov 2026",
           font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
