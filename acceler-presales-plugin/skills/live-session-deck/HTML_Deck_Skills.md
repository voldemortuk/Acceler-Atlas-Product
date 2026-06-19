---
name: html-deck-skills-acceler-kase-engine
description: "How to build a client-ready, pixel-consistent HTML slide deck on the Acceler KASE engine — a data-driven slide system where each slide is a tiny SLIDE_DATA object rendered by a shared kase-render.js + kase-styles.css. Covers folder structure, the ~80 templates and how to discover their fields, the format() mini-markdown, the Edelweiss-aligned dark-blue colour palette + type/spacing standard (locked Jun 2026), the build workflow, headless-Brave screenshot QA, PNG/PPTX export, Vercel deploy, and the fixes/gotchas found building the e& AI Builder deck. Companion to [[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]], [[deck-skills]], [[doc-proposal-skills]], [[pricing-skills]]."
metadata:
  node_type: memory
  type: reference
---

# Acceler HTML Deck Builder — the KASE engine — SKILL.md

**Goal:** ship a polished, on-brand HTML slide deck (1280×720, navigable, presenter-ready) where every slide is a *small data object*, not hand-written HTML — so the whole deck stays visually consistent and is trivial to edit, re-theme, screenshot, and export to PPTX.

**Engine:** lives in `engine/Slide_Library_v2/` next to this file — `kase-render.js` (the renderer + ~80 templates) and `kase-styles.css` (all the styling). **Reusable as-is — copy it into any new deck.** Worked example: the **e& AI Builder** deck (`…/Downloads/1. PowerUp/e&/eand_deck_build/`).

---

## 1. Mental model

A deck is three things:
1. **A viewer** (`index.html`) — a 1280×720 iframe shell with arrow-key / dot / label nav that auto-scales to the window. It reads a manifest and loads slides into the iframe.
2. **A shared engine** — `kase-render.js` + `kase-styles.css`. You almost never edit these (except deliberate fixes, see §9).
3. **Slides** — one tiny HTML file each. The *only* author-edited part is a `SLIDE_DATA = {…}` object naming a **template** + its fields. `kase-render.js` turns that into the rendered slide.

> One template → many slides. Change the data, not the markup. That is the whole point.

---

## 2. Folder structure (this is a *web root* — paths are absolute)

```
<deck_root>/                         ← serve THIS folder over http
  index.html                         ← the viewer (DECK = '/Decks/<name>/')
  deck/
    Slide_Library_v2/
      kase-render.js                 ← engine (copy from engine/ here)
      kase-styles.css                ← engine
    Images/                          ← ALL images resolve to /deck/Images/<file>
      acceler-logo-dark.svg, acceler-logo-white.svg, Cover_image.png,
      All_FAANG_logos.png, TIME_logo.png, GSV_2025.png, <client-logo>.png …
  Decks/
    <deck_name>/
      deck.json                      ← { "name", "created", "slides": [ "01-x.html", … ] }
      01-cover.html  02-…  …         ← the slide files
```

**Critical:** slides reference `/deck/Slide_Library_v2/…` and `/deck/Images/…` as **absolute** paths, and the viewer fetches `/Decks/<name>/deck.json`. So it **must be served over HTTP from the web root** (`python3 -m http.server`). `file://` breaks `fetch()` and the absolute paths.

---

## 3. Anatomy of a slide file

```html
<!DOCTYPE html><html lang="en"><head>
  <meta charset="UTF-8"><title>…</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="/deck/Slide_Library_v2/kase-styles.css" rel="stylesheet">
</head><body>
<script>
const SLIDE_DATA = {
  template: "solution_overview",     // ← picks the layout
  eyebrow:  "NO-CODE AI BUILDER",
  headline: "[No-Code AI Builder]: Overview",
  rows: [ … ],
  _sizes: {}                          // optional per-field font overrides
};
</script>
<div id="kase-mount"></div>
<script src="/deck/Slide_Library_v2/kase-render.js"></script>
</body></html>
```

The boilerplate is identical on every slide; only `SLIDE_DATA` changes. Fonts are **DM Serif Display** (headlines) + **DM Sans** (body) — don't change.

---

## 4. The `format()` mini-markdown (works in almost every text field)

| Syntax | Renders as |
|---|---|
| `[text]` | accent colour (coral `#f86b3c`) — use for the highlighted phrase in a headline |
| `[white:text]`, `[navy:text]`, `[teal:text]` … | named colour class `kc-<name>` |
| `[#073763:text]` | inline hex colour |
| `**bold**` / `*italic*` | bold / italic |
| `\n` | line break / new paragraph |
| line starting `--` | bullet point (• ) — used inside multi-line fields |
| pills fields: split on `·` | each `·`-separated token becomes a pill |

So a headline like `"[4 Days · 12 Pods]: From prompting to agents"` puts the bracketed part in the accent colour.

---

## 5. Discover any template's fields (the method — don't guess)

The renderer dispatches on `KASE_TEMPLATES[SLIDE_DATA.template]`. To find what a template accepts:

```bash
# list every template name
grep -nE "^  [a-z0-9_]+: function" engine/Slide_Library_v2/kase-render.js
# read the field-doc comment block + render body for one template
grep -n "^  champions_timeline" engine/Slide_Library_v2/kase-render.js   # → line N
# then read ~16 lines above N (the // Fields: … comment) and ~40 below (the body)
```
Every template has a `// Fields: …` comment above it. The **safest source of truth is a real working slide** that already uses it — copy its `SLIDE_DATA` shape.

### Templates used in the e& deck (field cheat-sheet)
- **cover_dark** — `headline`(\n ok) · `tagline_prefix` · `tagline_highlight` · `date` · `client_name` · `client_logo`(file in /deck/Images, else text fallback) · `client_logo_height` · optional `client_logo_2`/`_2_height`/`client_name_2`. Acceler logo is baked into the left.
- **section_divider_dark** — `section_label` · `headline`(\n) · `subtext`. (Dark RHS climber image baked in.)
- **acceler_intro** — `eyebrow` · `headline` · `subheading` · `stats:[{content:"100,000+\n--label"}]` (6) · `badge_1_src`/`badge_1` · `badge_2_src`/`badge_2` · `logos_src` (all images in /deck/Images).
- **approach_points** — `eyebrow` · `headline` · `points:[{num,title,desc}]` (6 → 3×2 grid after the §9 fix).
- **solution_columns** — `eyebrow` · `headline` · `card_title` · `card_subtitle` · `left_label` · `left_tagline` · `left_items:[{content}]` · `right_label` · `right_tagline`* · `right_items:[{content}]` · `banner`. *(right_tagline added in §9.)*
- **solution_overview** — `eyebrow` · `headline` · `card_title` · `card_color` · `label_color` · `strip_bg` · `strip_border` · `rows:[{label, type?, content}]` where `type` ∈ `pills`(split `·`) | `bullets`(`--` lines) | default(title\n desc) · `logos_note` · `logos_src`.
- **champions_timeline** — `eyebrow` · `headline` · `pre_label`/`pre_title`/`pre_desc` · `mod_1..8_week`/`_title`/`_desc`/`_pill` · `compact` · `banner`. Pills (drive colour): `Foundation, Enable, Build, Apply, Deploy, Aware, Communicate, Discover, Lead, Advanced, Diagnose, Architect`. Up to 8 modules.
- **module_table** — `eyebrow` · `headline` · `col_module`/`col_outcome`/`col_tags`/`col_duration` · `rows:[{module(\n), badge, outcome(\n), tags(\n-separated → pills), duration, color}]`. Row `color` ∈ `navy, teal, amber, accent, dark`.
- **tech_modules_grid** — `eyebrow` · `headline` · `note` · `col_1..4_label` · `c1..8_tag`/`_title`/`_desc` (cards 1-2→col1, 3-4→col2 …) · `banner`. (8 cards / 4 cols.)
- **two_cards** — `eyebrow` · `headline` · `card_1_title`/`card_1_sub`/`card_1_content`(`--` bullets, `—` marker) · `card_2_*` · `takeaway`.
- **use_case** — `layout:"1col"` · `eyebrow` · `headline` · `section_label` · `cases:[{content:"Title | subtitle\nbody"}]`.
- **closing** — `theme:"dark"` · `tagline` · `contacts:[{name,title,email}]`.

There are ~80 templates total (cover, dividers, pricing_grid, aiq_spider, testimonials_grid, frontier_case, pipeline_comparison, blueprint, ik_* variants, …). List them all with the grep above.

### Colour palette — the standard (Edelweiss-aligned dark-blue, locked on the e& deck Jun 2026)
The deck spine is **cool**: dark indigo-grey + coral accent + indigo secondary + cool off-whites/slate greys. Tokens are literal hex in **BOTH** `kase-styles.css` **and** `kase-render.js` (~230 inline hex there), so re-theming means swapping **both** files — **case-insensitively** (some hex are upper-case, e.g. `#262533`/`#F86B3C`).

| Role | Hex |
|---|---|
| **Dark** — all surfaces (cards, headers, full-bleed cover/divider/stat) | `#262533` |
| **Primary accent** — eyebrow, section-labels, divider lines, buttons, headline `[…]` highlight | `#f86b3c` · light `#ff7752` |
| **Secondary accent** — pills / labels | `#6167fa` (indigo) |
| **Main light bg** | `#f7f9fc` · panels `#eef1f7` / `#e6eaf2` |
| **Borders / dividers** | `#dce2ee` / `#cbd1e2` |
| **Body text** (slate) | `#475569` · muted `#64748b` · faint `#94a3b8` |
| **Headline / text on dark** | near-white `#f4f6fb` |
| Acceler **logo** marks (logo only — NOT the deck spine) | navy `#1B2A6B` · cyan `#27B4E6` |

> **Reference source of truth:** the dark-blue palette is sampled from the **Edelweiss proposal PPTX** (`…/Downloads/1. PowerUp/Edelweiss/Acceler_AI_Builders_Accelerator-Proposal-Edelweiss-…pptx`) — its most-used accent is `#F86B3C`, dark `#1A1A2E`, indigo `#6167FA`. The e& deck dark was then dialled to `#262533` per client preference.

**Curriculum / section semantic colours are intentionally NOT part of the spine** — the blueprint day/track categories (blue `#1e3a8a`, teal `#0f766e`, green `#16a34a`, amber `#b45309`, red `#dc2626`) stay as-is; they encode meaning, so **don't recolour them when re-theming**.
- **module_table row colors:** `navy · teal · amber · accent · dark`.
- **solution_overview card_color** accepts hex or `kc-` names: `navy · teal · brown · dark · muted · white`.

### Typography & spacing standard (locked on the e& deck, Jun 2026)
The system had drifted to **28 font-sizes / 15 line-heights / 3 different slide-top paddings**. The standard:
- **Slide-top padding:** every content slide = `44px 60px 0` so the eyebrow + headline start at the **same Y on every slide**. (Only the dense `cc-slide` keeps `24px`.) Don't override padding-top per-template.
- **Eyebrow:** one style — `13px / 600 / letter-spacing 0.12em / uppercase / #f86b3c`. The divider `section-label` uses the **same** (was 11px/0.14em).
- **Hero headline** (cover · dividers · closing): `52px` DM Serif Display (was a mix of 50/54/56).
- **Content headline** `32px` · **body** `15px` · **small** `13px` · **micro** (pills/labels) `11px` · dense data grids `12px`.
- Fonts unchanged: **DM Serif Display** (headlines) + **DM Sans** (body).

### Per-field overrides
- `_sizes: { "headline": 30, "rows[3].content": 13 }` → injects `font-size` for that `data-ks` path. Use to fix overflow without touching CSS.
- `_align: { "headline": "center" }` → text-align override.

---

## 6. Build workflow (start to finish)

1. **Scaffold** the web root (§2). Copy `engine/Slide_Library_v2/*` → `deck/Slide_Library_v2/`. Copy brand images → `deck/Images/` (incl. the client logo).
2. **Viewer** `index.html` — copy from the e& deck; set `const DECK = '/Decks/<your_name>/';`.
3. **Plan the narrative** (e.g. cover → divider → creds → approach → overview per track → journey → module table → use-cases → mapping → delivery → closing).
4. **Author each slide** — pick a template, fill `SLIDE_DATA`. Mirror a known-good slide's field shape.
5. **`deck.json`** — list slide filenames in order.
6. **Validate** before opening a browser (catches bad JSON / unknown templates / fields a template `.map`s that you didn't supply):

```bash
# parse + template-exists check, then a headless render smoke-test
node -e 'const fs=require("fs");/* eval each SLIDE_DATA, check template in KASE_TEMPLATES, run it against a DOM shim */'
```
(See the e& deck history for the exact validator; it renders each template against a stub `document` and asserts >200 chars out.)

7. **Preview + QA by screenshot** (§7) — you can't trust it until you see it.

---

## 7. Local preview + screenshot QA (the part that makes it pro)

```bash
cd <deck_root>
python3 -m http.server 8755 &            # serve the web root
open http://localhost:8755               # human preview
```

**Headless screenshots (Brave is Chromium — works without installing anything):**
```bash
BRAVE="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
"$BRAVE" --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1280,720 \
  --screenshot="/tmp/shot.png" \
  "http://localhost:8755/Decks/<name>/07-overview.html"
# 2x crisp (for PPTX/export): add  --force-device-scale-factor=2  → 2560x1440
```
Loop over every slide in `deck.json`, screenshot each, then **actually look at them** and fix alignment/overflow. This is how you catch the things validation can't (empty columns, misaligned bullets, wrapped pills). Sandbox note: `curl localhost` may be blocked even when the server is up — use Brave to render, not curl.

---

## 8. Export to PPTX (pixel-faithful, no design drift)

These are JS-rendered slides, so the faithful conversion is **one full-bleed 2× PNG per 16:9 slide** (not a native rebuild — that's the *other* skill, [[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]], for matching a native PPTX reference).

1. Render all slides at 2× (§7) → `/tmp/eshots/hr/*.png` (2560×1440).
2. Run `build_pptx.py` (next to this file): creates a 13.333×7.5 in deck, one `add_picture(img, 0,0, full width/height)` per slide, ordered by `deck.json`.
```bash
python3 -m pip install python-pptx          # once
cd <deck_root> && python3 build_pptx.py     # → AI_Builder…_NonExec.pptx
```
Result: opens anywhere, looks identical to the HTML. Trade-off: slides are images (not text-editable). That's the right call when the instruction is "don't change the design."

---

## 9. Fixes & gotchas (learned building the e& deck)

- **Serve over HTTP, not file://** — absolute `/deck/…` paths + `fetch(deck.json)` need a server.
- **Client logo** in `cover_dark`: if `client_logo` file is absent it falls back to `client_name` **text** — fine for drafts; drop `<client>.png` into `/deck/Images/` and set `client_logo` to light it up. (e& logo arrived without an extension → `file` showed PNG → renamed `eand-logo.png`.)
- **`approach_points` left a huge empty right half** — the stock `.ap-grid` is a single column. Fix (local CSS): `display:grid; grid-template-columns:1fr 1fr; column-gap:54px; row-gap:22px; align-content:center;` → 6 points become a balanced 3×2.
- **`solution_columns` columns didn't line up** — only `left_tagline` rendered, so left items started lower than right. Fix: add a `right_tagline` branch in the render (mirror the left one) + supply `right_tagline`.
- **Bullet dot floated high** (`solution_overview` Learning Objectives) — `.so-bullet::before` used `top:4px` on an 8px glyph. Fix: `top:0; line-height:21px;` (= text font-size×line-height) so the marker centres on the first line.
- **Bullets block centred, not left** (`solution_overview` bullets row) — `.so-content` is `align-items:center`, so a bullets block gets centred (big left gap) even though the text is `text-align:left`. Fix: `.so-content:has(.so-bullets){ align-items:stretch; text-align:left; }` (leaves pills/normal rows centred).
- **two-tracks L/R rows didn't line up** (`solution_columns`) — `.sc-items` used `justify-content:space-evenly`, so uneven wrap heights drifted the columns out of sync + left loose gaps. Fix: `.sc-items{ display:grid; grid-auto-rows:1fr; }` + `.sc-item{ justify-content:center; }` → equal-height bands that align across both columns.
- **Re-theming colour:** hex live in **both** `kase-styles.css` and `kase-render.js` — swap both, case-insensitively. **Leave the curriculum/section semantic colours** (blue/teal/green/amber/red) untouched. **macOS screenshots are colour-managed (Display P3)** — sampling a screenshot reads a saturated coral `#f86b3c` back as ~`#e7744a` (≈10–15 pts off). **Trust the source hex, not the screenshot pixels.**
- **Type/spacing drift** — before standardising, the deck had 28 font-sizes + 3 slide-top paddings. Keep to the §5 type & spacing standard (slide-top `44px 60px 0`; eyebrow 13px; hero headline 52px). Watch dense grid slides (`sb`/`ref`/`ns`, `overflow:hidden`) when bumping top padding — tighten internal gaps rather than the top pad if they clip.
- **champions_timeline** handles up to **8** modules; pills must be one of the known set (§5) or they fall back to grey.
- **Editing the engine is safe per-deck** — each deck has its *own copy* of `kase-render.js`/`kase-styles.css` under `deck/Slide_Library_v2/`, so a fix here never touches other decks.
- Long pill labels wrap to 2 lines (fine); very long table outcomes may need a `_sizes` nudge.

---

## 10. Deploy to Vercel (static site)

The **deck root is already a complete static site** — no build step.
1. Push the **`<deck_root>/`** folder (the one containing `index.html`, `deck/`, `Decks/`) to a GitHub repo, with `index.html` **at the repo root**.
2. In Vercel: **New Project → import the repo →** Framework Preset **"Other"**, Build Command **empty**, Output Directory **`./`** (root). Deploy.
3. Live at `https://<project>.vercel.app/` (the viewer). Direct slide: `…/Decks/<name>/01-cover.html`.
   - If `index.html` sits in a subfolder, set Vercel **Root Directory** to that subfolder instead.
   - Absolute `/deck/…` and `/Decks/…` paths resolve correctly because the repo root is the web root — same as local.

---

## 11. Checklist
- [ ] Web root scaffolded; engine + `/deck/Images/` (incl. client logo) in place
- [ ] `index.html` viewer `DECK` path set
- [ ] Each slide = template + `SLIDE_DATA`, shape mirrored from a known-good slide
- [ ] `deck.json` lists slides in order
- [ ] Validator: every SLIDE_DATA parses + template exists + render smoke-test >200 chars
- [ ] Screenshot **every** slide (Brave headless) and eyeball — fix alignment/overflow
- [ ] (export) 2× PNGs → `build_pptx.py` → 16:9 PPTX verified (count/size)
- [ ] (deploy) repo root = web root; Vercel preset "Other", output `./`

---

*Built from the e& AI Builder (No-Code + Low-Code) Non-Executive deck, Jun 2026 (`…/Downloads/1. PowerUp/e&/eand_deck_build/`). Engine reverse-engineered from the Acceler×ANSR OSB v3 KASE deck. Pairs with [[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]] (native PPTX-by-copy), [[deck-skills]], [[doc-proposal-skills]], [[pricing-skills]], [[session-mapping-skills]].*
