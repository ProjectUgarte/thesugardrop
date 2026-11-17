"""Render the PNG favicons (drop mark) and the social preview image."""
import math, os
from PIL import Image, ImageDraw, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
S = 4  # supersampling


def drop(size):
    W = 64 * S
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, W - 1], radius=14 * S, fill="#FBF6F0")
    cx, cy, r, ty = 32, 42.6, 18, 8

    def shape(rr):
        th = math.acos(rr / (cy - ty))
        pts = [(cx * S, ty * S)]
        for k in range(181):
            a = -math.pi / 2 + th + (2 * math.pi - 2 * th) * k / 180
            pts.append(((cx + rr * math.cos(a)) * S, (cy + rr * math.sin(a)) * S))
        return pts

    d.polygon(shape(r + 1.3), fill="#9C4A5E")
    d.polygon(shape(r - 1.3), fill="#F3D3D5")
    d.arc([(cx - 9.5) * S, (cy - 9) * S, (cx + 9.5) * S, (cy + 9.5) * S], 100, 175, fill="white", width=3 * S)
    sx, sy = 49, 13.8
    star = []
    for k in range(8):
        rad = 4.8 if k % 2 == 0 else 1.5
        a = k * math.pi / 4 - math.pi / 2
        star.append(((sx + rad * math.cos(a)) * S, (sy + rad * math.sin(a)) * S))
    d.polygon(star, fill="#B48E57")
    return im.resize((size, size), Image.LANCZOS)


drop(32).save(os.path.join(A, "favicon-32.png"))
drop(180).convert("RGB").save(os.path.join(A, "apple-touch-icon.png"))

src = os.path.join(ROOT, "_archive", "originals", "special-occasion", "024.jpg")
hero = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
ImageOps.fit(hero, (1200, 630), Image.LANCZOS, centering=(0.5, 0.12)).save(os.path.join(A, "og.jpg"), quality=84)
print("icons + og.jpg written")
