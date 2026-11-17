"""Build web images + assets/gallery-data.js from the archived originals.

Usage:  python3 tools/build_images.py [ORIGINALS_DIR]
        (default ORIGINALS_DIR = _archive/originals)

Originals are laid out as <gallery-slug>/<NNN>.jpg (any image format works).
To add new work: drop photos into the right gallery folder with the next number
(e.g. wedding-cakes/041.jpg) and re-run. Output is only rewritten for new/changed files.
"""
import json, os, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_archive", "originals")
OUT = os.path.join(ROOT, "assets", "img")
MANIFEST = os.path.join(ROOT, "_archive", "manifest.json")

FULL_MAX = 1600            # long edge of lightbox images
THUMB = (600, 750)         # 4:5 grid thumbnails
COVER = (720, 900)         # 4:5 category cards
HERO_W = (1400, 900)       # hero widths (srcset)

# Display order, names, short filter label and the photo used for each category card.
GALLERIES = [
    ("special-occasion",   "Special Occasion Cakes",        "Special Occasion",     "022"),
    ("wedding-cakes",      "Wedding Cakes",                 "Wedding",              "025"),
    ("character-cakes",    "Character Cakes",               "Character",            "003"),
    ("cupcakes",           "Designer Cupcakes",             "Cupcakes",             "001"),
    ("cookies",            "Designer Cookies",              "Cookies",              "001"),
    ("cake-pops",          "Cake Pops",                     "Cake Pops",            "011"),
    ("dessert-tables",     "Dessert Tables & Sets",         "Dessert Tables",       "013"),
    ("sugar-drops-treats", "Sugar Drops, Oreos & Treats",   "Sugar Drops & Treats", "009"),
]
HERO = ("special-occasion", "024")
ABOUT = ("about", "alison")

focal = {}
if os.path.exists(MANIFEST):
    for m in json.load(open(MANIFEST)):
        if "focal" in m:
            focal[m["file"].rsplit(".", 1)[0]] = m["focal"]


def load(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    return im.convert("RGB")


def fresh(src, dst):
    return os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)


def save(im, dst, q):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "WEBP", quality=q, method=6)


def fit_max(im, edge):
    if max(im.size) <= edge:
        return im
    r = edge / max(im.size)
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)


def crop(im, size, key):
    return ImageOps.fit(im, size, Image.LANCZOS, centering=tuple(focal.get(key, (0.5, 0.5))))


def find(gallery, stem):
    d = os.path.join(SRC, gallery)
    for f in os.listdir(d):
        if os.path.splitext(f)[0] == stem:
            return os.path.join(d, f)
    raise FileNotFoundError(f"{gallery}/{stem}")


data = {"galleries": []}
for slug, title, short, cover in GALLERIES:
    d = os.path.join(SRC, slug)
    items = []
    for f in sorted(os.listdir(d)):
        stem, _ = os.path.splitext(f)
        if not stem.isdigit():
            continue
        src = os.path.join(d, f)
        full = os.path.join(OUT, slug, f"{stem}.webp")
        thumb = os.path.join(OUT, slug, "t", f"{stem}.webp")
        if not (fresh(src, full) and fresh(src, thumb)):
            im = load(src)
            save(fit_max(im, FULL_MAX), full, 80)
            save(crop(im, THUMB, f"{slug}/{stem}"), thumb, 76)
        with Image.open(full) as fi:
            items.append({"n": stem, "w": fi.width, "h": fi.height})
    src = find(slug, cover)
    cdst = os.path.join(OUT, "covers", f"{slug}.webp")
    if not fresh(src, cdst):
        save(crop(load(src), COVER, f"{slug}/{cover}"), cdst, 80)
    data["galleries"].append({"slug": slug, "title": title, "short": short, "count": len(items), "items": items})
    print(f"{title:32} {len(items):3} photos")

src = find(*HERO)
for w in HERO_W:
    dst = os.path.join(OUT, f"hero-{w}.webp")
    if not fresh(src, dst):
        im = load(src)
        save(im.resize((w, round(im.height * w / im.width)), Image.LANCZOS), dst, 82)

src = find(*ABOUT)
dst = os.path.join(OUT, "alison.webp")
if not fresh(src, dst):
    save(load(src), dst, 88)

with open(os.path.join(ROOT, "assets", "gallery-data.js"), "w") as fh:
    fh.write("window.GALLERY_DATA=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("total:", sum(g["count"] for g in data["galleries"]), "photos -> assets/gallery-data.js")
