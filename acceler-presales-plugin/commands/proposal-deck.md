---
description: "PRE-SALES pitch deck. Generate a client-facing Acceler proposal / solution deck on the KASE engine — data-driven HTML slides (cover → context → approach → tracks → RFP mapping → delivery → closing), 1280×720, PNG/PPTX-exportable. This is the deck you PITCH with to win the deal. For the live delivery-session deck, use /acceler-presales:session-deck instead."
argument-hint: "<client name + program outline, or 'use last' to build from the latest /acceler-presales:proposal, or 'mirror e& AI Builder' to reuse the 19-slide reference structure>"
---

Generate a client-facing **proposal / solution deck** (the pre-sales pitch) on the Acceler KASE engine for the brief below.

## Input
```
$ARGUMENTS
```

## How to build

1. **Read the engine skill first:** `skills/proposal-deck/SKILL.md` — it has the full KASE mental model, the folder/web-root structure, the `SLIDE_DATA` slide anatomy, the `format()` mini-markdown, the ~80 templates + how to discover their fields, the locked dark-blue palette + type/spacing standard, the build workflow, screenshot QA, and the PNG/PPTX export + Vercel deploy steps.
2. **The engine is bundled** in `skills/proposal-deck/Slide_Library_v2/` (`kase-render.js` + `kase-styles.css`) and brand images in `skills/proposal-deck/Images/`. Copy them into the new deck's web root — do not hand-write slide HTML.
3. **The reference deck** is bundled at `skills/proposal-deck/reference/eand_AI_Builder/` (19 slides + `deck.json`). It is the pattern source — mirror its slide sequence and copy the `SLIDE_DATA` shapes rather than guessing template fields. If the user says "mirror e& AI Builder", reuse its structure 1:1 and only swap the client content.
4. **If a proposal was generated earlier** (`/acceler-presales:proposal`), use its Objective / Curriculum / Day-by-Day / RFP-coverage / Commercials as the source content so the pitch deck and the proposal document stay in sync.

## Slide arc (the e& AI Builder reference — adapt per client)

```
01 cover              →  cover_dark        client name + logo + date
02 divider context    →  section_divider_dark
03 acceler intro      →  acceler_intro     stats · badges · logos
04 approach           →  approach_points   6 points, 3×2
05 two tracks         →  solution_columns
06 divider no-code    →  section_divider_dark
07 no-code overview   →  solution_overview
08 no-code journey    →  champions_timeline
09 no-code pods       →  module_table
10 no-code artifacts  →  tech_modules_grid
11 divider low-code   →  section_divider_dark
12–15 low-code (overview · journey · pods · artifacts)
16 divider delivery   →  section_divider_dark
17 rfp mapping        →  module_table / requirement coverage
18 delivery model     →  two_cards
19 closing            →  closing           theme:dark · contacts
```

Keep the count/order flexible — some clients need fewer tracks or extra RFP slides. The template library is the constraint, not the slide count.

## Design (locked — see SKILL.md §6 for the full standard)

- **Fonts:** DM Serif Display (headlines) + DM Sans (body). Do not change.
- **Palette:** Edelweiss-aligned dark-blue standard; accent coral `#f86b3c`, dark `#262533` (e& client-dialled), indigo `#6167FA`. Sample exact tokens from `kase-styles.css`.
- **Canvas:** 1280×720, served over HTTP from the web root (`python3 -m http.server`) — `file://` breaks the absolute paths + `fetch()`.

## Output

Save the deck web root to:
```
~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/[Client]-proposal-deck/
```
with `deck/Slide_Library_v2/`, `deck/Images/`, and `Decks/<client>_<program>/` (slides + `deck.json`) per SKILL.md §2. List any client-specific images the team needs to drop into `deck/Images/` (client logo, etc.).

## Export (optional)

- **PNG / PPTX:** follow SKILL.md — headless-Brave 2× screenshots per slide → `build_pptx.py` (one full-bleed picture per slide, ordered by `deck.json`). Or hand off to the `/acceler-presales` pptx-deck skill.
- **Deploy:** static — Vercel / S3 / GitHub Pages (serve the web root).

## Quality checklist (apply before saving)

- [ ] Every slide is a `SLIDE_DATA` object naming a real template — no hand-written slide markup
- [ ] `deck.json` lists slides in order; served over HTTP (not `file://`)
- [ ] Cover has client name + client logo (or text fallback) + date
- [ ] Headlines use `[accent]` bracket highlight on the key phrase
- [ ] RFP-mapping / requirement-coverage slide present if the brief is an RFP
- [ ] Closing slide has `theme:"dark"` + contacts
- [ ] Fonts are DM Serif Display + DM Sans; palette sampled from `kase-styles.css`
- [ ] Rendered + eyeballed at 1280×720 (screenshot QA per SKILL.md §8)
