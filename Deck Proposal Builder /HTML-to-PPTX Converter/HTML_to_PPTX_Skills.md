---
name: html-to-pptx-converter-acceler-kase-deck
description: "How to convert a rendered Acceler KASE HTML slide deck into a pixel-faithful 16:9 PowerPoint — one full-bleed 2× PNG per slide, ordered by deck.json, assembled with python-pptx (build_pptx.py). Covers when to use this image-fidelity path vs a native PPTX rebuild, the headless-Brave 2× render step, the build script, verification, and gotchas. Companion to [[html-deck-skills-acceler-kase-engine]] (builds the HTML deck this converts) and [[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]] (the native, text-editable PPTX-by-copy alternative)."
metadata:
  node_type: memory
  type: reference
---

# Acceler HTML → PPTX Converter — SKILL.md

**Goal:** turn a finished, on-brand **KASE HTML deck** (1280×720 slides, see [[html-deck-skills-acceler-kase-engine]]) into a **PowerPoint that opens anywhere and looks identical to the live HTML** — zero design drift.

**How:** each slide is rendered to **one full-bleed 2× PNG** and dropped into a blank 16:9 PPTX slide via `python-pptx`. The deck's design is JS-rendered (DM Serif/DM Sans, CSS grids, SVG), so a screenshot-per-slide is the faithful conversion. Slide order follows `deck.json`.

**Files in this folder**
- `build_pptx.py` — the assembler (PNGs → 16:9 PPTX).
- `AI_Builder_Program_for_eand_NonExec.pptx` — **sample output**, regenerated from the latest e& AI Builder deck (Edelweiss-aligned dark-blue palette + Jun-2026 type/spacing standard).

---

## 1. When to use this (vs a native rebuild)

| | **This skill — image per slide** | **Native PPTX rebuild** ([[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]]) |
|---|---|---|
| Output | Each slide is a flat 2× image | Real shapes / text boxes |
| Fidelity | **Pixel-identical to the HTML** | Re-creates the design in PPTX tokens |
| Editable in PPT | ❌ images only | ✅ text/shapes editable |
| Use when | "Don't change the design — just give me a .pptx" / send-to-client / print | Client needs to edit text, or you're matching an existing native reference |

**Rule of thumb:** if the source of truth is the HTML deck and nobody needs to edit it in PowerPoint, use this. It's fast and never drifts.

---

## 2. Prerequisites

- A working KASE HTML deck served over HTTP (see [[html-deck-skills-acceler-kase-engine]] §2/§7). **Must be HTTP**, not `file://` (absolute `/deck/…` paths + `fetch(deck.json)`).
- A headless renderer. **Use `chrome-headless-shell` first — NOT Brave** (see ⚠️ below). Renderer priority:
  1. **`chrome-headless-shell`** (Playwright's bundled Chromium) — preferred, most reliable here:
     ```bash
     CH=$(find ~/Library/Caches/ms-playwright -name chrome-headless-shell -type f | head -1)
     # e.g. ~/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell
     ```
  2. **Google Chrome** (if installed) — same Chromium flags as the §3 loop, just swap the binary:
     ```bash
     CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
     # add --headless=new  (Chrome needs the flag; chrome-headless-shell does not)
     ```
     If Chrome isn't installed it's a quick `brew install --cask google-chrome` (or download).
  3. **Safari / WebKit** (no install — native to macOS) — drive `WKWebView` via a tiny Swift tool compiled with `swiftc` (`shoot.swift`, see LVT deck). Renders single slides correctly; flaked on a full 16-slide batch loop here, so use one slide per process invocation if you go this route. (`safaridriver` WebDriver also exists but needs `safaridriver --enable` + "Allow Remote Automation" and opens real windows — clumsier.)
  4. **Brave** — ❌ broken here, see ⚠️.
- `python3 -m pip install python-pptx` (once).

### ⚠️ Renderer gotcha — don't waste time on Brave (learned LVT deck, Jun 2026)

**Headless Brave hangs in this environment** and never writes a PNG — even on a trivial no-network `data:text/html` page, with `--headless=new` *and* legacy `--headless`, with `--disable-background-networking`, with the sandbox disabled. It just stalls on startup. Symptom: the loop runs, `build_pptx.py` reports `missing: [all slides]`, 0 PNGs. **Do not burn cycles re-flagging Brave.**

**What works, instantly and cleanly: Playwright's bundled `chrome-headless-shell`** (real Chromium, purpose-built for headless; exits per-invocation so a sequential loop is reliable). It's already on disk at `~/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell` (find it: `find ~/Library/Caches/ms-playwright -name chrome-headless-shell`). No `--headless` flag needed (it is headless). `--force-device-scale-factor=2` + `--window-size=1280,720` → exact 2560×1440 2× PNGs.

**Any real Chromium works** — so **Google Chrome** (`--headless=new --screenshot=…`, same flags as §3) or **Safari/WebKit** (`swiftc shoot.swift`, one slide per process) are both fine fallbacks if `chrome-headless-shell` isn't present. The only renderer that failed here was Brave. See the renderer priority list in §2.

---

## 3. The two steps

### Step 1 — render every slide to a 2× PNG
Serve the deck root, then loop `deck.json` slides through headless Brave at `--force-device-scale-factor=2` → **2560×1440** PNGs into `/tmp/eshots/hr/`.

```bash
cd <deck_root>
python3 -m http.server 8123 &                 # serve the web root (HTTP, not file://)

CH=$(find ~/Library/Caches/ms-playwright -name chrome-headless-shell -type f | head -1)
rm -rf /tmp/eshots && mkdir -p /tmp/eshots/hr
for s in $(python3 -c "import json;[print(x) for x in json.load(open('Decks/<name>/deck.json'))['slides']]"); do
  name="${s%.html}"
  "$CH" --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --user-data-dir="/tmp/cr-$name" \
    --window-size=1280,720 --virtual-time-budget=6500 \
    --screenshot="/tmp/eshots/hr/$name.png" \
    "http://127.0.0.1:8123/Decks/<name>/$s" >/dev/null 2>&1
done
ls -1 /tmp/eshots/hr | grep -c png        # expect == number of slides
```
- Per-slide `--user-data-dir` avoids profile-lock contention across the loop.
- ~~Brave~~ → use `chrome-headless-shell` (see §2 ⚠️). `chrome-headless-shell` is *already* headless — no `--headless` flag.
- `--virtual-time-budget=4500` gives Google Fonts + the render JS time to settle before the shot (skip it and headlines fall back to a system serif).
- `--window-size=1280,720` + scale-factor 2 = exact 16:9 at 2×. Each `.slide` is exactly 1280×720, so the shot is full-bleed with no letterboxing.
- The named-PNG (`07-nocode-overview.png`) matters — `build_pptx.py` maps PNG ↔ slide by `deck.json` name.

### Step 2 — assemble the PPTX
`build_pptx.py` (in this folder) creates a 13.333×7.5 in (16:9) deck and adds one full-width/height picture per `deck.json` slide.

```bash
cd <deck_root>            # run from the deck root: it reads Decks/<name>/deck.json
python3 build_pptx.py     # → AI_Builder_Program_for_eand_NonExec.pptx
```

Key bits of the script (edit these per deck):
```python
DECK_DIR = "Decks/eand_AI_Builder"     # where deck.json lives
SHOTS    = "/tmp/eshots/hr"            # the 2× PNGs from Step 1
OUT      = "AI_Builder_Program_for_eand_NonExec.pptx"
SW, SH   = 12192000, 6858000          # 16:9 in EMU (13.333in × 7.5in) — don't change
# blank = prs.slide_layouts[6]; add_picture(img, 0,0, width=SW, height=SH) per slide
```
It prints `slides written:` and any `missing:` (a slide in deck.json with no PNG → render it and re-run).

---

## 4. Verify

- **Count:** `slides written` == number of entries in `deck.json` (and `missing: none`).
- **Open it:** PowerPoint / Keynote / Google Slides — it should look identical to the live deck.
- **Spot-check the palette** (latest standard, see [[html-deck-skills-acceler-kase-engine]] §5): dark `#262533`, coral `#f86b3c`, indigo `#6167fa`, cool light `#f7f9fc`. If a slide looks stale, its PNG is old — re-render Step 1 (don't trust a cached `/tmp/eshots`).
- File size is a few MB (19 × 2× PNGs ≈ 5 MB) — expected.

---

## 5. Gotchas

- **Re-render after ANY deck change** — colour, copy, layout. The PPTX is only as fresh as the PNGs. Always `rm -rf /tmp/eshots` first so you never ship a mix of old/new shots.
- **Colour-profile caveat:** macOS screenshots are colour-managed (Display P3). The *embedded* PNG looks correct in PowerPoint, but if you eyedrop a saturated coral `#f86b3c` off the raw pixels it reads ~`#e7744a` (≈10–15 pts off). Judge colour from the live HTML / source hex, not from sampling the PNG.
- **Fonts:** the render must reach Google Fonts (online). Offline → DM Serif/DM Sans fall back and headlines look wrong. Keep `--virtual-time-budget` so fonts load before the shot.
- **HTTP only:** `file://` breaks `fetch(deck.json)` and the absolute `/deck/…` paths → blank/half slides.
- **Images, not text:** output slides are flat images — not editable in PowerPoint. If the client must edit text, use the native rebuild skill instead.
- **`curl localhost` may be sandbox-blocked** even when the server is up — render with Brave to confirm, not curl.

---

## 6. Checklist
- [ ] Deck served over HTTP from the web root (not `file://`)
- [ ] `rm -rf /tmp/eshots` then render **every** slide at 2× (PNG count == slide count)
- [ ] `build_pptx.py` `DECK_DIR` / `OUT` set for this deck; run from the deck root
- [ ] `slides written` == deck.json count, `missing: none`
- [ ] Opened the PPTX and eyeballed — palette + layout match the live HTML
- [ ] Sample/output PPTX saved alongside `build_pptx.py`

---

*Built from the e& AI Builder (No-Code + Low-Code) Non-Executive deck, Jun 2026. The sample `AI_Builder_Program_for_eand_NonExec.pptx` here is regenerated from the latest HTML deck (`…/Downloads/1. PowerUp/e&/eand_deck_build/`) after the Edelweiss-aligned dark-blue recolour + type/spacing standardisation. Pairs with [[html-deck-skills-acceler-kase-engine]] (builds the deck) and [[pptx-deck-skills-acceler-match-a-reference-solution-deck-builder]] (native, editable PPTX-by-copy).*
