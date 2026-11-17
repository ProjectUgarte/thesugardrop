# Go-live plan: thesugardrop.net off Squarespace

**Where things stand (checked 2026-11-17)**
- Domain `thesugardrop.net` is registered through Squarespace (registrar of record: Tucows),
  paid through **2027-05-05**, transfer lock on (normal).
- DNS is hosted by Squarespace. **No email records (MX) exist**, so nothing email-related can break.
- The Squarespace site hasn't been updated since mid-2018 and has no contact method on it.

**Target cost:** GitHub Pages $0 + domain ≈ $12–20/yr + Formspree free ⇒ **≈ $12–20/yr** (vs ~$120–140).

---

## 1. Draft on GitHub Pages (review with Alison)
- Push this repo to GitHub (public — required for free Pages; nothing private is in it).
- Enable Pages from `main` / root. Draft URL: `https://projectugarte.github.io/thesugardrop/`.
- The 404 redirector already handles the `/thesugardrop/` project path.

## 2. Connect the inquiry form (Formspree, free: 50 submissions/month)
- Create the Formspree account **using the email Alison wants inquiries sent to**
  (the free plan only delivers to the account's own email).
- New form → copy the endpoint (`https://formspree.io/f/xxxxxxx`).
- Replace `YOUR_FORM_ID` in `contact.html`'s `<form action=…>`; push; send a test inquiry.
- If the first notification lands in spam, mark it "Not spam" / add `formspree.io` to safe senders.

## 3. Point the domain at GitHub Pages
In Squarespace: **Domains → thesugardrop.net → DNS → DNS Settings**
- Delete the Squarespace Defaults preset (A records `198.185.159.x` / `198.49.23.x`, `www` CNAME
  `ext-sq.squarespace.com`).
- Add custom records:

| Host | Type | Value |
|---|---|---|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |
| `www` | CNAME | `projectugarte.github.io` |

- Then in the repo: add a `CNAME` file containing `thesugardrop.net`, and set it on the Pages site
  (`gh api --method PUT /repos/ProjectUgarte/thesugardrop/pages -f cname=thesugardrop.net`
  — the file alone left `cname:null` on Like Your Car). Once the certificate is issued, turn on
  **Enforce HTTPS** (`-F https_enforced=true`).
- Verify: `dig +short A thesugardrop.net @8.8.8.8` → the four 185.199.x.153 addresses;
  `curl -sI https://thesugardrop.net` → 200.

## 4. Cancel the Squarespace website plan (keep the domain!)
- Squarespace: **Settings → Billing → Subscriptions → Website → Cancel**.
  Cancel only the **website** subscription, not the domain.
- The domain keeps its own renewal at Squarespace (≈ $20/yr for .net).
- Do this *after* step 3 is verified, and save any invoices you want first.

## 5. Optional: transfer the domain to Cloudflare (≈ $11.86/yr at cost)
- At Cloudflare: create an account, add `thesugardrop.net`, and recreate the five records above
  (DNS only / grey cloud for the GitHub Pages records) **before** anything switches.
- At Squarespace: turn off the transfer lock, get the authorization code.
- At Cloudflare: Domain Registration → Transfer, enter the code, pay (adds one year to the expiry).
- Bonus: Cloudflare Email Routing can forward an address like `hello@thesugardrop.net`
  to Alison's existing inbox for free, if she ever wants a business address.
