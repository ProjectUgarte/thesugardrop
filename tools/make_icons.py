"""Render the PNG favicons (italic "S" monogram) and the social preview image."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
S = 4  # supersampling
FONT = ("/System/Library/Fonts/Supplemental/Baskerville.ttc", 5)  # SemiBold Italic


def monogram(size):
    W = 64 * S
    im = Image.new("RGB", (W, W), "#FBF6F0")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT[0], 54 * S, index=FONT[1])
    d.text((W / 2, W / 2), "S", font=font, fill="#9C4A5E", anchor="mm")
    return im.resize((size, size), Image.LANCZOS)


monogram(32).save(os.path.join(A, "favicon-32.png"))
monogram(180).save(os.path.join(A, "apple-touch-icon.png"))

src = os.path.join(ROOT, "_archive", "originals", "special-occasion", "024.jpg")
hero = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
ImageOps.fit(hero, (1200, 630), Image.LANCZOS, centering=(0.5, 0.12)).save(os.path.join(A, "og.jpg"), quality=84)
print("icons + og.jpg written")
