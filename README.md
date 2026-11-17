# The Sugar Drop — thesugardrop.net

Static site for Alison's custom-confections business, rebuilt off Squarespace.
Plain HTML/CSS/JS — no build step to publish; GitHub Pages serves the repo as-is.

## Pages
| File | What it is |
|---|---|
| `index.html` | Home: hero, gallery categories, promises, flavor teaser, Meet Alison, inquiry CTA |
| `gallery.html` | Filterable gallery of all 373 photos with a lightbox (data in `assets/gallery-data.js`) |
| `flavors.html` | Cake/cupcake flavors, buttercreams, fillings, and the cookie menu (`#cookies`) |
| `about.html` | Alison's bio |
| `contact.html` | Order inquiry form (Formspree) |
| `404.html` | Friendly not-found page that also redirects old Squarespace URLs (`/work`, `/cookies-1`, `/wedding-cakes`, …) |

Shared styles: `assets/site.css` (colors/fonts are CSS variables at the top). Shared behavior: `assets/site.js`.
The header and footer are repeated in each page — edit all five pages when changing the nav.

## Preview locally
```bash
python3 -m http.server 8100
```
Then open http://localhost:8100.

## Photos
- The full-resolution originals downloaded from Squarespace live in `_archive/originals/<gallery>/NNN.jpg`
  (not committed — 246 MB; keep a backup copy in iCloud/Google Drive).
- `python3 tools/build_images.py` makes the web versions in `assets/img/` (1600px lightbox images,
  4:5 thumbnails cropped around Squarespace's saved focal points, category covers, hero) and rewrites
  `assets/gallery-data.js`. It only processes new or changed files.
- **To add new work:** save the photo as the next number in the right folder
  (e.g. `_archive/originals/wedding-cakes/041.jpg`), run the script, commit, push. Category order,
  names, and cover photos are set in the `GALLERIES` list at the top of the script.
- `python3 tools/make_icons.py` renders the favicon PNGs and the social preview image (`assets/og.jpg`).

## Inquiry form
`contact.html` posts to Formspree. Until the real endpoint replaces `YOUR_FORM_ID` in the form's
`action`, submitting shows a "not connected yet" message instead of sending. Setup steps are in
`docs/go-live.md`.

## Going live
See `docs/go-live.md` (draft on GitHub Pages → form → point the domain → cancel the Squarespace plan
→ optional domain transfer).
