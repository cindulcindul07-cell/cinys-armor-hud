"""Generates Ciny's Armor HUD badges (12x12 pixel art, original artwork) and a
preview mock-up with stand-in armor sprites. Run: python3 make_badges.py  (needs Pillow)"""
import math, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "badges")
os.makedirs(OUT, exist_ok=True)

N = 8  # badge size in pixels: same size and octagon shape as uku's 8x8 warn icon

COLORS = {
    "brilliant":  (0x1B, 0xAC, 0xA6),
    "best_move":  (0x96, 0xBC, 0x4B),
    "inaccuracy": (0xF7, 0xC6, 0x31),
    "blunder":    (0xCA, 0x34, 0x31),
}

QMARK = ["##.", "..#", ".#.", "...", ".#."]   # 3x5 mini question mark
STAR = ["..#..", ".###.", "#####", ".###.", ".#.#."]  # 5x5

MASK = ["..XXXX..",
        ".XXXXXX.",
        "XXXXXXXX",
        "XXXXXXXX",
        "XXXXXXXX",
        "XXXXXXXX",
        ".XXXXXX.",
        "..XXXX.."]  # same octagon as uku's warn.png


def bang(x0, y0):  # 1px wide, 5 tall: bar(3) gap dot
    return [(x0, y0), (x0, y0 + 1), (x0, y0 + 2), (x0, y0 + 4)]


def glyph(rows, x0, y0):
    return [(x0 + c, y0 + r) for r, line in enumerate(rows)
            for c, ch in enumerate(line) if ch == "#"]


def symbol(name):
    if name == "brilliant":      # !!
        return bang(2, 1) + bang(5, 1)
    if name == "best_move":      # star
        return glyph(STAR, 2, 1)
    if name == "inaccuracy":     # ?!
        return glyph(QMARK, 1, 1) + bang(5, 1)
    if name == "blunder":        # ??
        return glyph(QMARK, 1, 1) + glyph(QMARK, 4, 1)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def make(name):
    base = COLORS[name]
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    px = img.load()
    inside = lambda x, y: 0 <= x < N and 0 <= y < N and MASK[y][x] == "X"
    for y in range(N):
        for x in range(N):
            if not inside(x, y):
                continue
            rim = not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if rim:  # light rim top-left, dark rim bottom-right (same shading idea as uku's icon)
                k = x + y
                f = 0.85 if k <= 6 else 0.75 if k == 7 else 0.63
                px[x, y] = shade(base, f) + (255,)
            else:
                f = 1.13 if x + y <= 4 else 1.0
                px[x, y] = shade(base, f) + (255,)
    tint = tuple(int(v + (255 - v) * 0.82) for v in base)  # soft white with a hint of the badge colour
    for (x, y) in symbol(name):
        if 0 <= x < N and 0 <= y < N:
            px[x, y] = tint + (255,)
    img.save(os.path.join(OUT, name + ".png"))
    return img


badges = {n: make(n) for n in COLORS}

# ---------- stand-in armor sprites (16x16, original pixel art, preview only) ----------
HELMET = [
    "................", "................",
    "....########....", "...#HHHHHHHH#...", "..#HBBBBBBBBS#..",
    "..#HBBBBBBBBS#..", "..#HBBBBBBBBS#..", "..#HBBBBBBBBS#..",
    "..#HB#DDDD#BS#..", "..#HB#DDDD#BS#..", "..#HB#....#BS#..",
    "..#BB#....#BS#..", "..####....####..", "................",
    "................", "................"]
CHEST = [
    "................", ".###........###.", "#HBB#......#BBS#",
    "#HBBB######BBBS#", "#HBBBBBBBBBBBBS#", "#HBBBBBBBBBBBBS#",
    ".#BBBBBBBBBBBS#.", "..#HBBBBBBBBS#..", "..#HBBBBBBBBS#..",
    "..#HBBBBBBBBS#..", "..#HBBBBBBBBS#..", "..#BBBBBBBBBS#..",
    "..############..", "................", "................", "................"]
LEGS = [
    "................", "..############..", "..#HBBBBBBBBS#..",
    "..#HBBBBBBBBS#..", "..#HBBBBBBBBS#..", "..#HBB####BBS#..",
    "..#HBB#..#BBS#..", "..#HBB#..#BBS#..", "..#HBB#..#BBS#..",
    "..#HBB#..#BBS#..", "..#HBB#..#BBS#..", "..#BBB#..#BBS#..",
    "..####....####..", "................", "................", "................"]
BOOTS = [
    "................", "................", "................", "................",
    "................", "..####....####..", "..#HBS#..#HBS#..",
    "..#HBS#..#HBS#..", "..#HBS#..#HBS#..", ".#HBBBS#.#HBBBS#",
    "#HBBBBS##HBBBBS#", "################", "................", "................",
    "................", "................"]
for m in (HELMET, CHEST, LEGS, BOOTS):
    assert all(len(r) == 16 for r in m) and len(m) == 16

MATERIALS = {
    "diamond": ((0x9A, 0xF5, 0xEA), (0x33, 0xBA, 0xA8), (0x1E, 0x7F, 0x80)),
    "iron":    ((0xF2, 0xF2, 0xF2), (0xC8, 0xC8, 0xC8), (0x8A, 0x8A, 0x8A)),
    "gold":    ((0xFF, 0xF1, 0x8A), (0xF5, 0xC8, 0x2E), (0xB9, 0x82, 0x14)),
    "leather": ((0xC3, 0x9B, 0xF0), (0x8F, 0x5F, 0xD0), (0x5B, 0x37, 0x95)),
}


def sprite(mask, material):
    hi, base, sh = MATERIALS[material]
    cols = {"H": hi, "B": base, "S": sh, "#": (0x1B, 0x1B, 0x22), "D": (0x12, 0x12, 0x16)}
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(mask):
        for x, ch in enumerate(row):
            if ch in cols:
                img.putpixel((x, y), cols[ch] + (255,))
    return img


# ---------- preview ----------
S = 5
STEP, SIZE, BADGE_GAP = 20, 22, 2
WIDTH = 4 * STEP + 2                  # 82, like the vanilla hotbar start
HOTBAR_LEFT = WIDTH + 7 + 29 + 0      # widget + gap (98-91) + offhand slot space
W = HOTBAR_LEFT + 182 + 8
H = N + BADGE_GAP + SIZE + 2
prev = Image.new("RGBA", (W, H), (38, 50, 36, 255))
pp = prev.load()


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            pp[xx, yy] = c


def rating_for(p):
    return "brilliant" if p > 75 else "best_move" if p > 50 else "inaccuracy" if p > 25 else "blunder"


def bar_color(p):
    t = p / 100.0
    return (int(255 * min(1, 2 * (1 - t))), int(255 * min(1, 2 * t)), 0, 255)


def strip(x, y, slots):  # hotbar-look strip (stand-in for the vanilla sprite)
    w = slots * STEP + 2
    rect(x, y, w, SIZE, (0x8B, 0x8B, 0x8B, 255))
    rect(x + 1, y + 1, w - 2, SIZE - 2, (0x2A, 0x2A, 0x2A, 255))
    for i in range(1, slots):
        rect(x + i * STEP, y + 1, 2, SIZE - 2, (0x8B, 0x8B, 0x8B, 255))
    for i in range(slots):
        rect(x + i * STEP + 2, y + 2, 18, SIZE - 4, (0x1A, 0x1F, 0x18, 255))


slot_y = N + BADGE_GAP
strip(HOTBAR_LEFT, slot_y, 9)
strip(0, slot_y, 4)
pieces = [(HELMET, "diamond", 12), (CHEST, "iron", 100), (LEGS, "leather", 62), (BOOTS, "gold", 40)]
for i, (mask, mat, pct) in enumerate(pieces):
    x = i * STEP
    prev.alpha_composite(sprite(mask, mat), (x + 3, slot_y + 3))
    if pct < 100:  # vanilla item bar: 13x2 black, 12x1 colour, at item x+2, y+13
        rect(x + 5, slot_y + 16, 13, 2, (0, 0, 0, 255))
        rect(x + 5, slot_y + 16, max(1, round(13 * pct / 100)), 1, bar_color(pct))
    prev.alpha_composite(badges[rating_for(pct)], (x + 6, slot_y - N - BADGE_GAP))

prev = prev.resize((W * S, H * S), Image.NEAREST)
prev.save(os.path.join(OUT, "preview.png"))
print("done")
