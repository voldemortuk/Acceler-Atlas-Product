---
name: live-session-deck-skills-acceler-html-live-session-deck-builder
description: "How to build a client-facing live session HTML deck — full-screen slides with keyboard navigation, speaker notes, progress bar, touch swipe, and print fallback. Covers the design tokens (cream bg · navy + cyan · Acceler logo), the slide-type library (cover · instructor intro · phase divider · pipeline · checklist · screenshot · ecosystem · chapter rail · pick cards · statement · handoff), the JS controller (40 lines), accessibility, and the worked example (e& PPF Hungary · CETIN × Yettel · Build your AI team). This is the SOURCE that PPTX_Deck_Skills.md converts from — keep the HTML and PPTX in sync via shared data. Companion to [[pptx-deck-skills]], [[doc-proposal-skills]], [[pricing-skills]], [[session-mapping-skills]]."
metadata:
  node_type: memory
  type: reference
  originSessionId: 6d83a6a7-37dc-44fa-b73c-61e1418d2a82
---

# Acceler Live Session Deck Builder — SKILL.md (v1)

**The HTML deck is the source of truth.** The PPTX is downstream — `PPTX_Deck_Skills.md` copies a reference deck and rebuilds only the content slides whose data changed. Keep this HTML deck's content data in a single block at the top so the PPTX twin can re-use it without drift.

**Default reference:** `acceler-nucleus-session-deck/` (Nucleus AI Builders, Apr 2026). **Reusable for:** any live session — e& PPF Hungary (CETIN × Yettel), Cornerstone MasterClass, Bosch Masterclass, Edelweiss days, ANSR demo, etc. The engine is reference-agnostic — point it at any reference deck and re-extract its tokens.

---

## 1. The deck shape (4 movements)

Every live session deck follows the same 4-movement arc:

1. **Open** — cover · instructor intro · how the session runs · "pop into the chat" warm-up · "optimise your experience" house rules (3 cards)
2. **Set up** — phase divider · setup overview (split layout: 2 cards + URL card + checklist) · 5 numbered VM/tool steps (each = browser screenshot + 1-line banner) · ecosystem overview (5-card grid)
3. **Build** — phase divider · pattern stages (Basic → Intermediate → Advanced) · pick-your-use-case (2 cards) · handoff to lab
4. **Close / handoff** — dark statement slide with kicker + big line + CTA

Total slides typically **15–25** per session. Cover, instructor, phase dividers, and statement slides are framing — never rebuild them. Only content slides change per client.

---

## 2. Design tokens (lock these)

### 2.1 Palette

```
--bg:            #FAF7F1   /* cream/beige page background */
--bg2:           #EEF0FB   /* secondary surface (chat warm-up) */
--card:          #FFFFFF   /* card surfaces */
--navy:          #2C3F8E   /* primary navy (banners, accents) */
--navy-deep:     #0F1632   /* dark slides + body fallback */
--cyan:          #5BC4D2   /* progress · accents · CTAs */
--cyan-dk:       #2C3F8E   /* cyan dark (headings) — alias of navy */
--cyan-soft:     #E8F7FA   /* cyan tint (callouts, urlcard) */
--ink:           #1A2240   /* body text */
--text2:         #4B5563   /* secondary text */
--muted:         #6B7280   /* tertiary / labels */
--border:        #E5E7EB   /* hairlines */
--green:         #10B981   /* success */
--green-l:       #ECFDF5   /* success tint (allgreen check) */
--amber:         #B45309   /* warn (locked steps) */
--amber-l:       #FFF8ED   /* warn tint */
--red:           #DC2626   /* error */
--red-l:         #FEF2F2   /* error tint */
```

Dark slides use a navy gradient: `linear-gradient(135deg,#0F1632 0%,#2D3666 100%)`. Cover uses radial: `radial-gradient(ellipse at 30% 25%,#2D3666 0%,#0A0A1A 100%)`.

### 2.2 Typography

```
--font: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
--mono: "SF Mono", Monaco, "Cascadia Code", monospace;
```

Type scale (use `clamp()` for responsiveness):

| Element                    | Size                          | Weight | Notes                            |
|----------------------------|-------------------------------|--------|----------------------------------|
| Cover h1                   | `clamp(40px,5vw,68px)`        | 800    | letter-spacing -0.025em          |
| Section h2                 | `clamp(34px,4.4vw,56px)`      | 800    | letter-spacing -0.02em           |
| Statement big              | `clamp(34px,4.6vw,60px)`      | 800    | letter-spacing -0.025em          |
| Slide h (.h)               | `clamp(24px,2.9vw,35px)`      | 800    | letter-spacing -0.015em          |
| Lead body (.lead)          | 18px                          | 400    | line-height 1.6                  |
| Eyebrow                    | 13.5px                        | 700    | letter-spacing 0.16em · UPPERCASE|
| Card title (.card .t)      | 20px                          | 800    | letter-spacing -0.01em           |
| Card desc (.card .d)       | 15px                          | 400    | line-height 1.55                 |
| Banner                     | 15px                          | 400    | line-height 1.5                  |
| Mono (URL block)           | 13px                          | 400    | --mono family                    |

### 2.3 Page size & layout

- **Slide canvas:** absolute-positioned full-viewport (`position:absolute; inset:0`), padding `44px 64px`.
- **Inner max-width:** `1180px`, centered (`.inner`).
- **Print:** `@page { size: 1280px 720px; margin: 0; }`, each `.slide` becomes `page-break-after:always` and forced `opacity:1`. Hides progress, brand, fs, counter, zone, notes, nav.

---

## 3. Slide-type library (every shape you need)

### 3.1 Cover (slide 0)

```html
<div class="slide cover active" data-notes="…">
  <div class="inner">
    <div class="cover__logos">
      <div class="logoplate"><img src="acceler_logo.png" alt="Acceler"></div>
      <!-- optional partner logos: div.logodiv between plates -->
    </div>
    <div class="badge">Copilot Leadership Lab · [Client] · [Account]</div>
    <h1>Build your<br><span class="accent">AI team.</span></h1>
    <p>Walk in a leader. Walk out a builder — with a <b>real agent that works your week.</b></p>
    <div class="chips">
      <span class="chip">🛠️ <b>Copilot Studio</b> · Virtual Labs</span>
      <span class="chip">🤖 <b>1 agent</b> · built end-to-end</span>
      <span class="chip">⏱️ <b>2.5 hours</b></span>
    </div>
    <div class="foot">← → navigate · F fullscreen · "." speaker notes</div>
  </div>
</div>
```

Rules:
- One H1 only, with a `<span class="accent">` for the cyan-highlighted phrase.
- Logos sit on white `logoplate` rounded cards with `box-shadow 0 12px 34px rgba(0,0,0,.28)`.
- 3 chips max — keep them factual (tools · output · duration).
- Always include the navigation hint at the foot (`← → · F · "."`).

### 3.2 Instructor intro (slide 1)

Two-column grid `270px 1fr`. Left column = circular photo (196px), specializations list, experience tiles. Right column = "Your host today" eyebrow + name + role + 3–4 `bsec` blocks (Career Highlights · Telco/Domain · Recent Work · Now). The featured-experience tile gets `.extile--feat` with cyan glow.

```html
<div class="intro">
  <div class="intro__l">
    <img class="intro__photo" src="…" alt="…">
    <div class="intro__lab">Technical Specializations</div>
    <ul class="speclist"><li>…</li></ul>
    <div class="explab">Experience</div>
    <div class="extiles">
      <span class="extile extile--feat" style="color:#E40000;">Airtel<span class="tcap">Telecom</span></span>
      <span class="extile" style="color:#0B2A6B;">Paytm</span>
    </div>
  </div>
  <div class="intro__r">
    <div class="intro__eyebrow">Your host today</div>
    <div class="intro__name">[Name]</div>
    <div class="intro__role">[Tagline · ex-X · current Y]</div>
    <div class="bsec"><h4>Career Highlights</h4><ul>…</ul></div>
    <div class="bsec"><h4>📡 [Domain] — [Industry]</h4><ul>…</ul></div>
    <div class="bsec"><h4>Recent Work</h4><ul>…</ul></div>
    <div class="bsec"><h4>Now — Building with AI</h4><ul>…</ul></div>
  </div>
</div>
```

Rules:
- Speaker notes: ~60 seconds. Establish credibility, then move.
- 4 `bsec` blocks max. Bold the bank-shot stats (`<b>+70%</b>`, `<b>4.85/5</b>`).
- Anchor the most relevant experience as `--feat` — if it's a telco audience, feature the telco brand.

### 3.3 Pipeline (3 steps)

`pipe` = flex row of 3 `pstep` cards separated by `parrow` arrows. Each step = icon + title + 1-line description.

```html
<div class="pipe">
  <div class="pstep"><div class="pi">🧰</div><div class="pt">Set up</div><div class="pd">Get everyone into the virtual lab and working.</div></div>
  <div class="parrow">→</div>
  <div class="pstep"><div class="pi">🤖</div><div class="pt">Build your agent</div><div class="pd">One agent, end-to-end, live on your own account.</div></div>
  <div class="parrow">→</div>
  <div class="pstep"><div class="pi">🌙</div><div class="pt">See one run</div><div class="pd">An agent that works while you sleep.</div></div>
</div>
```

Followed by a `banner` with a conversation-mode reminder (`💬 This works best as a conversation. Ask any time…`).

### 3.4 Chat warm-up (engagement)

Background: `linear-gradient(135deg,#F4F6FC 0%,#D8DCEF 100%)`. Centered. Big "Pop into the chat:" line followed by 3 white pills (Name · Role · Location). Used right before the first phase to break the ice.

### 3.5 House rules (3 cards)

Background: same light gradient. 3 numbered cards with coloured corner dots (amber, cyan, navy). Rules: **Be Vocal** · **Be Confident** · **Be Active**. Each card has a `01/02/03` numerator (small, muted).

### 3.6 Phase divider

```html
<div class="slide section">
  <div class="inner">
    <div class="num">Phase N · [Phase Name]</div>
    <h2>First, let's<br>get you set up.</h2>
    <div class="sub">Nobody moves on until everybody is in. Five minutes, well spent.</div>
  </div>
</div>
```

Dark navy gradient. Always uses `.num` eyebrow + h2 (two-line break) + `.sub` line. Use once per major arc transition.

### 3.7 Setup split (cards + URL/checklist)

Two-column grid `1fr 1fr`. Left = 2 numbered cards (`.card.top`). Right = `urlcard` (cyan-soft pill with URL + button) + readiness checklist (`✓` items). Concludes with the green "All green? Let's move forward. ✅" pill.

### 3.8 Screenshot step (VM walkthrough)

`shotwrap` = column of: framed browser mockup (`shot__bar` with 3 colored dots + `<img>`) + banner with the 1-line instruction. Used in numbered series ("Sign in · 1 of 5", "Open lab · 2 of 5", etc.). Eyebrow indicates progress.

### 3.9 Ecosystem (5-card grid)

5-column grid of `ecard` cards. Each = icon + name + 1-line description. Cyan top border (`border-top:4px solid var(--cyan)`). Used to introduce a stack ("The building blocks you'll use today").

### 3.10 Chapter rail (3-stage)

3 `chnode` cards separated by `charrow` arrows. Each node = numbered tag + icon + name + description. Use for "Basic → Intermediate → Advanced" or any 3-stage progression. The narrative banner below ties it together.

### 3.11 Pick cards (2-option chooser)

`pick` = 2-column grid of `pcard` cards. Each = function eyebrow (e.g. "Staying current") + agent name (e.g. "Yettel Market Pulse") + description + 3 cyan-soft `ptag` chips. Use for "pick your use case" decision moments.

### 3.12 Locked / pre-build steps

`lstep` rows with numbered tag + title + tagline + blurred mono code block (`filter:blur(4.5px)`). The pseudo-element absolute-positions a `LOCKED` pill in the corner. Use sparingly — a teaser of what's about to come.

### 3.13 Outbox (live result)

Green-tinted outcome row showing what arrives after the agent runs. Small uppercase "EMAIL" label + the actual subject/body excerpt.

### 3.14 Statement / handoff

```html
<div class="slide dark stmt">
  <div class="inner">
    <div class="kick">Your build guide</div>
    <div class="big">The next hour is <span class="accent">yours.</span></div>
    <div class="sub">Each of you builds your own agent.</div>
    <div style="margin-top:32px;"><a class="cta" href="…">Open the build lab →</a></div>
  </div>
</div>
```

Dark navy gradient. Centered. Kicker + big line + sub + CTA. Use as a phase handoff or session close. Always 1 CTA max.

### 3.15 Speaker notes

Every slide MUST have a `data-notes="…"` attribute. Notes are toggled by `.` key. Format: 1–3 sentences, written as direct address to the instructor (not the audience). Include cues like "Don't dwell — name them, then move." or "Keep this to ~60 seconds."

---

## 4. The JS controller (40 lines, copy verbatim)

```javascript
const slides=[...document.querySelectorAll('.slide')], total=slides.length;
let cur=0; const $=id=>document.getElementById(id);
const speaker=slides.map(s=>s.dataset.notes||''); let notesOn=false, ctO;
function updNotes(){ $('notesC').textContent=speaker[cur]||''; }
function progress(){
  $('progress').style.width=((cur+1)/total*100)+'%';
  const c=$('counter'); c.textContent=(cur+1)+' / '+total;
  c.classList.add('on'); clearTimeout(ctO); ctO=setTimeout(()=>c.classList.remove('on'),2000);
  updNotes(); syncNav();
}
function goTo(n){ if(n<0||n>=total) return; slides[cur].classList.remove('active'); cur=n; slides[cur].classList.add('active'); progress(); }
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '){e.preventDefault();goTo(cur+1);}
  else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();goTo(cur-1);}
  else if(e.key==='Home')goTo(0); else if(e.key==='End')goTo(total-1);
  else if(e.key==='.'){ notesOn=!notesOn; $('notes').classList.toggle('on',notesOn); }
  else if(e.key==='f'||e.key==='F'){ /* fullscreen toggle */ }
});
// click zones + bottom nav + touch swipe + ?s= deep link
```

Features (all free with the same script):
- **Keyboard:** `←/→/Space` navigate · `Home/End` jump · `.` toggle notes · `F` fullscreen.
- **Touch:** swipe left/right (50px threshold).
- **Click zones:** left 11% / right 11% of the viewport.
- **Bottom nav:** dot indicator + prev/next + count, auto-scrolls active dot into view.
- **Progress bar:** cyan, top-of-screen, animates on slide change.
- **Counter:** appears in top-right for 2s after each change, then fades.
- **Deep link:** `?s=N` opens to slide N on page load.
- **Speaker notes:** absolute-positioned tray that slides up from bottom; toggled with `.`.

---

## 5. Per-client retargeting (the generalisation)

To produce a deck for a new client:

1. **Copy** the working reference HTML (e.g. `acceler-nucleus-session-deck/index.html`) to a new folder named `acceler-[client]-session-deck/`.
2. **Swap framing tokens** in slide 0 (cover): client name in badge, partner logo if applicable, big-line phrasing, chips (tools · output · duration).
3. **Swap instructor** in slide 1: photo path, name, role line, specializations, experience tiles (feature the most relevant brand for the audience — telco uses Airtel, banking uses HDFC, etc.), `bsec` content.
4. **Swap content** in build slides (use cases, screenshots, ecosystem). Keep slide IDs (data-step ordering) stable so the PPTX twin can re-use the same data block.
5. **Update CTAs** to point at the next-deck folder (`pick-your-use-case/index.html`).
6. **Update speaker notes** to client context.
7. **Validate**: open in browser, walk every slide via keyboard, check screenshots load, check notes appear, check print preview.

The 4 movements stay the same. Tokens, screenshots, copy change.

---

## 6. Content data block (sync with PPTX twin)

To keep the HTML and the PPTX in sync, the content data lives in a single top-of-file object that both decks consume:

```javascript
const DECK = {
  client: "e& PPF Hungary",
  partner: "CETIN × Yettel",
  programme: "Build your AI team",
  duration: "2.5 hours",
  output: "1 agent · built end-to-end",
  instructor: {
    name: "Madan Rawtani",
    role: "AI + Growth + Engineering · ex-Bharti Airtel · Growth @ Acceler",
    photo: "assets/slide02_2.png",
    specializations: ["AI-Powered Growth Systems", "Multi-Agent Systems & Agentic Workflows", "…"],
    featuredExperience: { brand: "Airtel", color: "#E40000", caption: "Telecom" },
    experience: [
      { brand: "Paytm",         color: "#0B2A6B" },
      { brand: "OYO",           color: "#EE2E24" },
      { brand: "PhysicsWallah", color: "#6C4FB6" },
      { brand: "Housing.com",   color: "#EF1C74" }
    ],
    blocks: [
      { heading: "Career Highlights", items: ["…"] },
      { heading: "📡 Airtel — Telecom", items: ["…"] },
      …
    ]
  },
  useCases: [
    { fn: "Staying current", agent: "Yettel Market Pulse", desc: "…", tags: ["🌐 Live web","📧 Work IQ","🕘 9 AM daily"] },
    { fn: "Walking in cold", agent: "Yettel Meeting Prep", desc: "…", tags: ["🗓️ Calendar","📧 Email + Teams","🕘 9 AM daily"] }
  ],
  ecosystem: [
    { i: "🛠️", n: "Copilot Studio", d: "Where you build, test & publish your agent." },
    …
  ]
};
```

The PPTX builder (`PPTX_Deck_Skills.md`) consumes the same `DECK` object, so when you update the HTML, the PPTX rebuild gets the same data automatically.

---

## 7. Accessibility & polish

- **Contrast:** all text passes WCAG AA on cream bg. Dark slides use white at `≥0.7` opacity for non-headings.
- **Touch targets:** click zones are 11% of viewport on each side. Bottom nav buttons are 30×30px (above the 24px AA minimum).
- **Keyboard-only:** every interaction has a key binding. No mouse-only paths.
- **Screen readers:** `<img alt>` on every screenshot. Logos have `alt` set. `aria-label` on prev/next buttons.
- **Reduced motion:** the `.slide.active` opacity transition is `.4s ease` — gentle enough for vestibular sensitivity. Skip the SVG animations (`.anim-svg`) on `prefers-reduced-motion`.

---

## 8. Worked example — e& PPF Hungary

**File:** `e&-pp-hungary-session-deck/index.html`  
**Format:** 17 slides, 2.5 hours.  
**Arc:** Cover · Madan intro · How 2.5 hrs run · Pop into chat · Optimise · **Phase 1 Set up** · VM access split · 5 VM steps · Browser tabs · Find Copilot Studio · Copilot ecosystem · Basic→Intermediate→Advanced · **Phase 2 Build** · Pick use case · Handoff to lab.  
**Output:** Each participant builds their own Copilot agent (Yettel Market Pulse OR Yettel Meeting Prep) end-to-end on their VM.  
**PPTX twin:** Built by copying the 46-slide reference deck and rebuilding only Days 2–4 content per `PPTX_Deck_Skills.md` §5 (reorder via `sldIdLst` element refs). Output: `Acceler_Solution_Deck-e&-PP-Hungary.pptx`.

---

## 9. Build script pattern

Recommended file layout:

```
[client]-session-deck/
├── index.html              ← the deck (this skill)
├── pick-your-use-case/
│   └── index.html          ← per-use-case lab (linked from handoff CTA)
├── assets/
│   ├── slide02_2.png       ← instructor photo
│   ├── slide07_1.png       ← VM login screenshot
│   ├── slide08_1.png       ← My Labs screenshot
│   └── …
└── acceler_logo.png        ← brand mark (or inline SVG)
```

Open `index.html` in any modern browser. No build step. No npm. No bundle. Hosts on any static server (S3, GitHub Pages, Vercel static, Cloudfront).

---

## 10. Quality checklist

- [ ] Cover has client + partner branding · badge · 1 h1 with cyan-accent phrase · 3 chips · keyboard hint footer
- [ ] Instructor intro: photo · 4–5 specializations · featured experience tile (`--feat`) · 3–4 `bsec` blocks · name + role + eyebrow
- [ ] Every slide has `data-notes` (1–3 sentences, instructor-facing)
- [ ] Phase divider before each major arc transition (Set up → Build → Close)
- [ ] All 3 pipeline arrows are `→` (`parrow` class)
- [ ] Setup screenshots all use `shot` frame with browser-bar dots
- [ ] Ecosystem grid is exactly 5 cards (rebuild as `c3` if 3 or `c4` if 4)
- [ ] Chapter rail has 3 nodes with numbered tags
- [ ] Pick cards have 3 `ptag` chips each (max)
- [ ] Statement / handoff slides use `.dark.stmt` class with kicker + big + sub + 1 CTA
- [ ] Print stylesheet hides progress, brand, fs, counter, zone, notes, nav
- [ ] Deep link `?s=N` opens correct slide
- [ ] Keyboard nav works: arrows · space · home/end · `.` notes · `F` fullscreen
- [ ] Touch swipe works (50px threshold)
- [ ] Deck plays through end-to-end without errors in console
- [ ] PPTX twin (`PPTX_Deck_Skills.md`) consumes the same `DECK` data object

---

## 11. File naming convention

```
[Client]-session-deck/index.html
acceler-nucleus-session-deck/index.html         ← Apr 2026, reference
e&-pp-hungary-session-deck/index.html           ← Jun 2026
bosch-india-masterclass-deck/index.html
csod-copilot-agent-masterclass-deck/index.html
edelweiss-day-1-deck/index.html
```

Per-day decks for multi-day programs go in subfolders: `edelweiss-day-1-deck/index.html`, `edelweiss-day-2-deck/index.html`, etc.

---

*Built from: e& PPF Hungary live session deck (`Build your AI team`, Jun 2026); acceler-nucleus-session-deck reference (Apr 2026). Pairs with [[pptx-deck-skills]] (the PPTX twin), [[doc-proposal-skills]] (the proposal that anchors the deck), [[pricing-skills]] (the commercials behind the deck), [[session-mapping-skills]] (the requirement coverage that justifies the deck).*
