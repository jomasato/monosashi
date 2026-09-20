"""Draw the home-screen icons.

The icon is the instrument itself: a graduated track with the needle parked
off-centre. Nothing else on the screen is that coral, so the icon and the game
read as the same object.

    python tools/make_icons.py
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUND = (12, 16, 20)
TRACK = (33, 42, 51)
TICK = (105, 119, 133)
NEEDLE = (255, 107, 74)
TRUTH = (78, 201, 168)


def dial(size, rounded, inset=0.16):
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.215), fill=GROUND)
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=GROUND)

    pad = s * inset
    top, bot = s * 0.30, s * 0.70
    d.rounded_rectangle([pad, top, s - pad, bot], radius=int((bot - top) * 0.22), fill=TRACK)

    # the target band, off to the right
    bw = (s - pad * 2)
    tx = pad + bw * 0.66
    band = bw * 0.17
    d.rectangle([tx - band / 2, top, tx + band / 2, bot], fill=TRUTH + (70,))

    # graduations
    for i in range(1, 10):
        x = pad + bw * i / 10.0
        h = (bot - top) * (0.42 if i % 5 else 0.62)
        d.line([(x, top), (x, top + h)], fill=TICK, width=max(1, int(s * 0.006)))

    # the needle, deliberately not on the band
    nx = pad + bw * 0.38
    d.line([(nx, top - s * 0.04), (nx, bot + s * 0.04)], fill=NEEDLE, width=max(2, int(s * 0.016)))
    r = s * 0.085
    d.ellipse([nx - r, (top + bot) / 2 - r, nx + r, (top + bot) / 2 + r], fill=NEEDLE)

    return img.resize((size, size), Image.LANCZOS)


def out(img, name):
    img.save(os.path.join(HERE, name))
    print("wrote", name)


if __name__ == "__main__":
    # iOS masks apple-touch-icon itself, so hand it a full square
    out(dial(180, rounded=False), "icon-180.png")
    out(dial(192, rounded=True), "icon-192.png")
    out(dial(512, rounded=True), "icon-512.png")
    # maskable: keep everything inside the middle 80%
    out(dial(512, rounded=False, inset=0.26), "icon-maskable-512.png")
    out(dial(32, rounded=True, inset=0.12), "favicon-32.png")
