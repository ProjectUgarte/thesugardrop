"""Build numbered contact sheets of the archived originals (for curation only)."""
import os, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
SRC = sys.argv[1]; OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
T = 180; COLS = 8
try: font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
except Exception: font = ImageFont.load_default()
for gal in sorted(os.listdir(SRC)):
    d = os.path.join(SRC, gal)
    if not os.path.isdir(d): continue
    files = sorted(os.listdir(d))
    for page in range(0, len(files), 48):
        chunk = files[page:page+48]
        rows = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS*T, rows*T), "white")
        dr = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            with Image.open(os.path.join(d, f)) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                w, h = im.size
                im = ImageOps.fit(im, (T-4, T-4))
            x, y = (i % COLS)*T, (i // COLS)*T
            sheet.paste(im, (x+2, y+2))
            label = f"{os.path.splitext(f)[0]} {max(w,h)}"
            dr.rectangle([x+2, y+2, x+2+dr.textlength(label, font=font)+8, y+26], fill="black")
            dr.text((x+6, y+4), label, fill="white", font=font)
        sheet.save(os.path.join(OUT, f"{gal}-{page//48+1}.jpg"), quality=80)
        print("sheet", gal, page//48+1, len(chunk))
