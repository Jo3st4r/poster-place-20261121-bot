"""Draw the DRIFTWICK travel poster (1024x1024 PNG).

Concept: DRIFTWICK — an island that drifts with the currents, never in the
same harbour twice. One island, 365 harbours, 0 anchors. A golden-hour
vintage travel poster: the place name in huge condensed type across the sky,
one lighthouse on a green drifting island, a sailboat below.

Deterministic: every coordinate is fixed, no randomness, no network.
Run:  python3 tools/render.py [out.png]   (default assets/entry.png)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
HORIZON = 560

SKY_TOP = (255, 246, 220)
SKY_BOTTOM = (255, 217, 160)
SEA_TOP = (18, 131, 127)
SEA_BOTTOM = (7, 86, 94)
SUN = (255, 107, 74)
ISLAND = (30, 91, 63)
ISLAND_LIGHT = (52, 128, 84)
INK = (11, 61, 58)
CREAM = (255, 248, 236)
CORAL = (255, 107, 74)

COND_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def vgrad(top, bottom, height):
    t = np.linspace(0, 1, height, dtype=np.float64)[:, None]
    a = np.array(top, dtype=np.float64)[None, :]
    b = np.array(bottom, dtype=np.float64)[None, :]
    return (a * (1 - t) + b * t).astype(np.uint8)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(BOLD, size)


def draw_poster(out_path):
    sky = np.zeros((H, W, 3), dtype=np.uint8)
    sky[:HORIZON] = vgrad(SKY_TOP, SKY_BOTTOM, HORIZON)[:, None, :]
    sky[HORIZON:] = vgrad(SEA_TOP, SEA_BOTTOM, H - HORIZON)[:, None, :]
    img = Image.fromarray(sky, "RGB").convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # --- sun halo + disc (low sun near the horizon, right of the island) ---
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse([742 - 150, 428 - 150, 742 + 150, 428 + 150],
               fill=(255, 205, 150, 55))
    halo = halo.filter(ImageFilter.GaussianBlur(40))
    ov.alpha_composite(halo)
    d.ellipse([742 - 92, 428 - 92, 742 + 92, 428 + 92], fill=SUN + (255,))

    # --- clouds: flat cream ellipses ---
    for box in [(80, 296, 330, 336), (590, 150, 860, 188),
                (110, 428, 290, 458), (820, 300, 970, 330)]:
        d.ellipse(box, fill=(255, 253, 244, 210))

    # --- birds ---
    for (x, y, s) in [(180, 250, 14), (252, 208, 11), (322, 282, 9),
                      (880, 182, 12)]:
        d.line([(x - s, y), (x, y - s * 0.55), (x + s, y)],
               fill=INK + (220,), width=3)

    # --- horizon line ---
    d.line([(0, HORIZON), (W, HORIZON)], fill=CREAM + (180,), width=3)

    # --- island: one green drifting hill ---
    island = [(140, 648), (200, 548), (290, 494), (375, 468),
              (465, 476), (555, 508), (640, 556), (685, 648)]
    d.polygon(island, fill=ISLAND + (255,))
    d.line(island[:6], fill=ISLAND_LIGHT + (255,), width=5)

    # --- lighthouse: the one landmark, white tower on the crest ---
    d.rectangle([388, 372, 412, 472], fill=CREAM + (255,))
    d.rectangle([388, 420, 412, 428], fill=INK + (255,))
    d.rectangle([392, 354, 408, 372], fill=(40, 40, 40, 255))
    d.ellipse([397, 360, 403, 366], fill=(255, 214, 90, 255))
    d.polygon([(384, 354), (416, 354), (408, 338), (392, 338)],
              fill=CORAL + (255,))

    # --- two small houses on the island ---
    for (hx, hy, s) in [(252, 566, 1.0), (520, 584, 0.8)]:
        w, h = int(36 * s), int(26 * s)
        d.rectangle([hx, hy, hx + w, hy + h], fill=CREAM + (255,))
        d.polygon([(hx - 4, hy), (hx + w + 4, hy),
                   (hx + w // 2, hy - int(18 * s))], fill=CORAL + (255,))

    # --- pines on the slopes ---
    for (px, py, s) in [(330, 520, 1.0), (585, 540, 0.85), (205, 585, 0.7)]:
        w = int(26 * s)
        d.polygon([(px, py - int(34 * s)), (px - w // 2, py),
                   (px + w // 2, py)], fill=(16, 66, 44, 255))
        d.rectangle([px - 2, py, px + 2, py + int(10 * s)],
                    fill=(16, 66, 44, 255))

    # --- sea: wave dashes (fixed jitter so the grid does not read as a grid) ---
    for (y, gap, ln, alpha, shift) in [(660, 90, 46, 110, 0),
                                       (730, 120, 60, 90, 55),
                                       (810, 100, 52, 120, 18),
                                       (890, 130, 64, 90, 70),
                                       (960, 110, 56, 120, 30)]:
        x = 40 + shift
        while x < W - 40:
            d.line([(x, y), (x + ln, y)], fill=(255, 255, 255, alpha),
                   width=4)
            x += gap + ln

    # --- sun reflection: warm dashes on the water below the sun ---
    for (y, ln, alpha) in [(600, 150, 120), (650, 120, 100), (700, 96, 90),
                           (760, 76, 80), (830, 60, 70), (905, 44, 60)]:
        d.line([(742 - ln // 2, y), (742 + ln // 2, y)],
               fill=(255, 190, 130, alpha), width=5)

    # --- sailboat, lower right ---
    d.polygon([(742, 872), (838, 872), (806, 898), (770, 898)],
              fill=(24, 40, 38, 255))
    d.line([(790, 872), (790, 776)], fill=(24, 40, 38, 255), width=4)
    d.polygon([(790, 780), (790, 866), (838, 866)], fill=CREAM + (255,))
    d.polygon([(790, 800), (790, 866), (756, 866)], fill=(255, 220, 170, 255))
    d.rectangle([742, 906, 838, 912], fill=(255, 255, 255, 70))

    # --- the place name, huge condensed type across the sky ---
    name_font = font(COND_BOLD, 150)
    d.text((W // 2, 118), "DRIFTWICK", font=name_font,
           fill=INK + (255,), anchor="mm")

    img.alpha_composite(ov)
    img = img.convert("RGB")

    # --- vintage frame ---
    fd = ImageDraw.Draw(img)
    fd.rectangle([0, 0, W - 1, H - 1], outline=INK, width=12)
    fd.rectangle([26, 26, W - 27, H - 27], outline=CREAM, width=2)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".",
                exist_ok=True)
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/entry.png"
    draw_poster(out)
    print("wrote", out)
