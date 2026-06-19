# Acceler Proposal Builder — SKILL.md (v2)

**Distilled from the four IK-Acceler reference proposals: Nucleus Software (India · AI Builders · 2-day Live), Booking Holdings (India · GenAI Engineering Accelerator · 4-day Live), Gryphon Investors (US · FDE Programme · 4-day Live), and MCB Mauritius (Self-Paced LMS · 20–30 hrs).**

v2 replaces v1, which was sourced from the wrong corpus (Ooredoo / PowerUp-by-UnO Deloitte work). v2 is grounded in Acceler / Interview Kickstart B2B proposals only — the structural skeleton from v1 is preserved; the format, font, palette, and component patterns are updated to match the IK-Acceler reference samples.

The Mini-UT context layer (decision logic, classification, routing, escalation, pricing scenarios) lives in `Mini-UT Context/context.md` and `Mini-UT Context/utkarsh_context.md`. That layer informs **how** the agent reasons; this SKILL.md informs **what** the agent produces.

---

## 1. Document Architecture

### 1.1 Always Start With a Full-Bleed Navy Cover

Every proposal opens with:

- A full-bleed dark-navy cover page (`#0F1936` background, all text white)
- Eyebrow at top: **"BY UnO UPWARD AND ONWARD"** in **Nunito 9pt**, with single-character flashes in `#3A96D2` inside `UnO` and `AND`
- Partnering line in **Manrope 18pt**: *"Partnering with [Client] on its journey to [strategic intent]"*
- Tagline / mission line in Manrope 18pt (e.g. *"AI enabling orgs for 100X productivity"*)
- Anchor line: **"Proposal For"** + client name + **Month Year**
- Title in **Manrope 19pt bold**: *"Draft Proposal | [Programme Name] For [Client]"*
- Positioning subtitle in Manrope 12pt
- 4-column stats strip table directly under the title (emoji + label + value per cell)

```
[BY UnO UPWARD AND ONWARD]                       ← Nunito 9pt white, accent flashes #3A96D2
Partnering with [Client] on its journey to …
[Tagline]
Proposal For
[Client Name]
[Month Year]
Draft Proposal | [Programme Name] For [Client]    ← Manrope 19pt bold white
[Positioning subtitle]                            ← Manrope 12pt white
[ 🏦 Focus  |  👨‍💻 Audience  |  📅 Duration  |  ⏱️ Hours ]
```

### 1.2 Section Structure (Live / Multi-Day Proposals)

Use **Heading 2** for primary section titles in `#1C4587`. Use day-section headers in 12pt bold `#1A2B4A` or `#0D1F3C` (consistent per proposal). Use Heading 3 in `#000000` for end-of-day outcome boxes.

Standard section order for **live / multi-day proposals**:

1. Objective
2. Curriculum Overview (Who / Delivery / Duration / Tools / Tentative Dates / Prerequisites)
3. Program at a Glance (5-col summary table)
4. Day-by-Day Breakdown (per day: header → Objective+Tools mini-table → Schedule table → 5–10 Part tables → Day Use Cases table → 🎯 End-of-Day takeaway)
5. Program Summary (closing roll-up table)
6. Every [Audience] Walks Away With (2-column Systems Built | Methodology Earned)
7. Commercials (India only — INR table; US/ME proposals carry commercials externally)
8. **Sign-Off Block (§8)**
9. Closing page ("PLUG IN & ACCELERATE")

### 1.3 Section Structure (Self-Paced / LMS Proposals)

Standard section order for **self-paced / LMS proposals**:

1. Objective
2. Curriculum Overview (Format, total hours per track, prerequisites, tools, post-programme support)
3. Program Storyline (one bold-leading paragraph per module)
4. Programme at a Glance (9-col table: Features | Total | Videos | Hands-On | Assignment | Quiz | Reading | Audience)
5. What Participants Walk Away With (Foundation Track / AI Champion Track)
6. Understanding [Client]'s Requirements (Heading 1 `#1C4587`, sub-headings `#2E6DB4`)
7. Curriculum Design & Learning Architecture (Format | Duration | Purpose)
8. Module-by-Module Breakdown (per module: Heading 1 → time/objective/tools → Video Lessons table → Lesson-by-Lesson breakdown with Concepts/Hands-On → Reading Material → Quiz & Assignment → End-of-Module Outcome)
9. Optional Add-On — Industry Expert Masterclass (when applicable)
10. Delivery Methodology & LMS Integration (Content Format · LMS Integration SCORM/xAPI · Localization)
11. Indicative Project Timeline
12. Next Steps (closing with *"We look forward to building [Client]'s AI-ready workforce together."*)
13. **Sign-Off Block (§8)**
14. Content-page footer: `Acceler | Confidential`
15. Closing page ("PLUG IN & ACCELERATE")

---

## 2. Colour Palette

### 2.1 IK-Acceler Brand Palette (Single Source of Truth)

```
NAVY_DEEP    = "0F1936"   // cover & closing page background
NAVY_HEAD    = "1C4587"   // primary section headings (Objective, Program at a Glance, etc.)
NAVY_DAY_A   = "1A2B4A"   // Day-section headers — fintech / engineering proposals
NAVY_DAY_B   = "0D1F3C"   // Day-section headers — strategic / FDE / Booking-style
NAVY_SUB     = "2E6DB4"   // Sub-headings (Heading 2 inside major sections — self-paced)
NAVY_DETAIL  = "1B3A6B"   // Lesson-detail "Concepts:" / "Hands-On:" labels (self-paced)

ACCENT_BLUE  = "3A96D2"   // micro-accent flashes inside cover eyebrow
GOLD         = "C9960C"   // tagline accent (e.g. "AI FORWARD DEPLOYED ENGINEER PROGRAMME")
GREEN_NOTE   = "274E13"   // tools-customisable callout text
RED_NOTE     = "FF0000"   // critical client-decision callout (use sparingly)

TEXT_BODY    = "1A1A2E"   // primary body text
TEXT_MUTED   = "222222"   // secondary body
TEXT_DIM     = "333333"   // tertiary / takeaway bullets
WHITE        = "FFFFFF"   // cover & closing text
GRAY_FOOT    = "999999"   // "Acceler | Confidential" footer
MGRAY        = "CCCCCC"   // table border
GRAY_ZEBRA   = "F5F7FA"   // alternating row shading
```

### 2.2 Day-Header Variant Rules

- Use `NAVY_DAY_A` (`#1A2B4A`) when days are framed as build sprints (Nucleus-style "AI Builder" days, technical fintech proposals).
- Use `NAVY_DAY_B` (`#0D1F3C`) when days are framed by theme or business context (Booking "Production-Grade RAG", Gryphon "The FDE Toolkit").
- Pick one per proposal and use it consistently across every day header. Never mix.

### 2.3 What Changed from v1

The PowerUp / Ooredoo client-specific palettes (Ooredoo red `#E30613`, Gryphon orange `#E05C1A`, Acceler-default blue `#2563EB`, phase colours teal/orange/purple/green) are **retired**. IK-Acceler proposals use a single navy ramp anchored on `#1C4587` for all primary headings, with the two day-header variants above. Accent colours (`GOLD`, `GREEN_NOTE`, `RED_NOTE`) are used sparingly for positioning emphasis only.

---

## 3. Typography

```
FONT_HEADING = "Manrope"   // all headings, body, tables
FONT_COVER   = "Nunito"    // cover + closing eyebrow lines (9pt white)
FONT_MONO    = none         // monospace not used — keep tooling lists in Manrope
```

### 3.1 Type Scale (in pt)

| Element                                       | Size | Weight | Colour              |
|-----------------------------------------------|------|--------|---------------------|
| Cover eyebrow ("BY UnO UPWARD AND ONWARD")    | 9    | Reg    | `#FFFFFF` (Nunito)  |
| Cover partnering line / tagline               | 18   | Reg    | `#FFFFFF`           |
| Cover title ("Draft Proposal \| …")           | 19   | Bold   | `#FFFFFF`           |
| Cover positioning subtitle                    | 12   | Reg    | `#FFFFFF`           |
| Primary section heading (Heading 1/2)         | 17   | Bold   | `#1C4587`           |
| Sub-section heading (self-paced Heading 2)    | 13–14| Bold   | `#2E6DB4`           |
| Day header (live proposals)                   | 12   | Bold   | `#1A2B4A` or `#0D1F3C` |
| Module Heading 3 ("End of Day Outcome", etc.) | 13   | Bold   | `#000000`           |
| Sub-section internal label (Tools, Schedule)  | 13   | Bold   | inherit             |
| Lesson title (self-paced "1.1 — …")           | 12   | Bold   | `#222222`           |
| Lesson "Concepts:" / "Hands-On:" label        | 10   | Bold   | `#1B3A6B`           |
| Body                                          | 11–12| Reg    | `#1A1A2E`           |
| Footer ("Acceler \| Confidential")            | 9    | Reg    | `#999999`           |

---

## 4. Component Library

### 4.1 Borders

```javascript
const bd  = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const bds = { top: bd, bottom: bd, left: bd, right: bd };
const nb  = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const nbs = { top: nb, bottom: nb, left: nb, right: nb };
```

### 4.2 Typography Helpers

```javascript
const sp   = (n=1) => paragraph { spacing: { before: 55*n, after: 55*n }, children: [] };
const pb   = ()    => paragraph { children: [new PageBreak()] };
const div  = (c=NAVY_HEAD) => horizontal-rule paragraph (8pt bottom border in colour c);
const h1   = t  => bold 19pt #1C4587 Manrope (or apply Heading 1 style)
const h2   = (t, c=NAVY_HEAD) => bold 17pt colour c Manrope
const h3   = (t, c="000000")  => bold 13pt colour c Manrope
const body = t  => 11–12pt #1A1A2E Manrope
const bl   = t  => bullet paragraph, 11pt #1A1A2E Manrope
const ftr  = () => "Acceler | Confidential", 9pt #999999 Nunito, right-aligned
```

### 4.3 Table Cell Helpers

```javascript
hc(text, width, bg=NAVY_DEEP)        // header cell — white bold text on navy
dc(text, width, sh, bold, col)       // data cell — optional zebra shading via GRAY_ZEBRA
dvc(text, width, sh)                 // data cell, vertically centred
rc(text, width, bg=NAVY_HEAD)        // accent right-column cell (coloured bg, white bold)
emojiCell(emoji, label, value)       // stats-strip cell — emoji + label + value stacked
```

### 4.4 Stats Strip (Cover Component)

A 1-row × 4-column table directly under the cover title.

```
[ 🏦 [Focus]  |  👨‍💻 [Audience]  |  📅 [Duration]  |  ⏱️ [Hours] ]
```

Rules:
- Equal column widths (default).
- Transparent background on dark cover; if used inside body pages, light gray (`#F5F7FA`).
- Each cell: emoji icon + short bold label + value, stacked.
- Examples from samples:
  - **Nucleus:** `🏦 Fintech Domain Focus | 👨‍💻 Pro Code Engineers Only | 📅 2 Days AI Builder Track | ⏱️ 18 Hrs Hands-On Labs`
  - **Booking:** `🔍 RAG Production-Grade | 🤖 Agents LangGraph · MCP | 🕸️ Multi-Agent Orchestration | ⏱️ 24 Hrs · 4 Days · 6 hrs each`
  - **Gryphon:** `🏢 Portfolio Focus Operational AI | ⚡ FDE Standard 72-hr Deployment | 🔄 APR Built-In GOAT Framework | ⏱️ 24 Hrs · 4 Days · 6 hrs each`

### 4.5 Day Block (Live / Multi-Day Proposals)

Every day follows this exact pattern:

```
[Day N Header — "Day N · X hrs · [Theme]"]                   ← 12pt bold NAVY_DAY_A or NAVY_DAY_B
[ Objective | [single-sentence outcome] ]                    ← 2-row, 2-col table
[ Tools     | [tool · tool · tool] ]

[Day N Schedule — X Hours]                                   ← 12pt bold
[ Section | Source (from N-Day) | Time ]                     ← 3-col schedule table
  - 7–10 rows, each 30–150 min
  - Last row total

[Part 1 — [Title]  ·  X min]                                 ← 2-row narrow table
[Objective: …  Concepts Covered: …  Hands-On: …]               (stacked content in one cell)

[Part 2 — …]
…
[Part k — …]                                                  (5–10 parts per day)

[Day N — [Client] Use Cases Practised]                       ← 12pt bold heading
[ Use Case | What [Audience] Build | Domain | Value ]        ← 4-col, 4–5 rows
  - Each row = one client-grounded build

[ 🎯  End of Day N — What [Audience] Build & Walk Away With ]  ← 1×1 takeaway box
[ Participants leave with: [3–6 concrete artifacts] ]

[ page break ]
```

Key rules:
- **Objective** is a single sentence — no leading "We will…".
- **Concepts covered** are descriptive noun phrases explaining *why* the concept matters.
- **Activities / Hands-On** start with a hands-on verb (Build / Hands-on / Each engineer / Teams / Regroup).
- **Tools** are listed inline joined by `·` (e.g. *"LangChain · LangGraph · Tavily API"*).
- **Outcome** always starts with `🎯` and `✓` cues; phrasing template: *"Participants leave with: [artifact]"*.

### 4.6 Module Block (Self-Paced Proposals)

```
[Heading 1: Module N — [Title]]                              ← bold 17pt #1C4587

[ [Theme]  |  Estimated Time: X Hours ]                      ← single line

[Objective: [single sentence]]                               ← 13pt bold

[Tools Covered]                                              ← 13pt bold
- Tool A
- Tool B

[Video Lessons]                                              ← 13pt bold
[ Lesson Title | Duration | Format ]                         ← lessons summary table
  - N.1, N.2, … N.k    (each 5–10 min)

[Lesson-by-Lesson Breakdown]                                 ← 13pt bold
[N.1  —  [Lesson Title]]                                     ← 12pt bold #222222
Concepts: …                                                  ← 10pt bold #1B3A6B
Hands-On: …                                                  ← 10pt bold #1B3A6B
[N.2  —  …]
…

[Reading Material]                                           ← 13pt bold
- Title — short description (X min)
- …

[Quiz & Assignment]                                          ← 13pt bold
- Quiz NA — …
- Assignment NB — …

[Heading 3: Module N — End of Day Outcome | [Title]]         ← bold 13pt #000000
By the end of Module N, participants will have:
- Outcome 1
- Outcome 2
Recap: …
Reflection: …
Artifact: …
Post-Class Feedback: Instructor ratings & subjective feedback via LMS
```

### 4.7 End-of-Day / End-of-Module Takeaway Box

```
[NAVY header: 🎯  End of Day N — What [Audience] Build & Walk Away With]
[Light body (zebra or pale navy):
   Participants leave with:
   - Artifact 1
   - Artifact 2
   - Artifact 3   (3–6 total)
]
```

Rules:
- Always include the `🎯` emoji.
- Always closes a day or module section before the page break.
- Phrasing: *"Participants leave with:"* (live) or *"By the end of Module N, participants will have:"* (self-paced).

### 4.8 Info Box / Callout

```javascript
infoBox(title, lines, bg=GRAY_ZEBRA, tc=NAVY_HEAD)
```

Background variants observed in the samples:
- `GRAY_ZEBRA` (`#F5F7FA`) — general programme info.
- Light green tint with `#274E13` text — tools-customisable callout (*"All tooling can be customized to align with your team's existing infrastructure"*).
- `#FF0000` text on white — critical client-decision callout (MCB used this once for the optional masterclass note; use sparingly).

### 4.9 Summary Table (Program at a Glance — Live)

5-column structure:

| # | Day Title | Duration | Focus / Key Tools | Key Build / FDE Build / Artifact |
|---|-----------|----------|--------------------|-----------------------------------|
| 1 | …         | X hrs    | …                  | …                                 |
| 2 | …         | X hrs    | …                  | …                                 |
| … | …         | …        | …                  | …                                 |
|   | N Days    | Total hrs| (mixed)            | "Complete [Outcome]"              |

The last row aggregates totals; columns 3–4 carry mixed / summary descriptors.

### 4.10 Programme at a Glance (Self-Paced)

9-column structure (MCB pattern):

| | Features | Total | Videos | Hands-On Activity | Assignment | Quiz | Reading Material | Who is this For? |
|---|---|---|---|---|---|---|---|---|
| Level 1 | … | 15 hrs | 4 hrs | 5 hrs 40 min | 4 hrs | 1 hr 15 min | 2 hrs | For Everyone |
| Level 2 | … | 5 hrs  | 1 hr  | 2 hrs 10 min | 1 hr  | 25 min      | 25 min | For Learners with Paid MS Copilot |

### 4.11 Program Summary (Closing Roll-Up)

Same as 4.9, but column 4 is renamed contextually (e.g. "FY26 Alignment", "FDE Competency Earned"). Always close with:

```
Every [Audience] Walks Away With
[ 🛠️  Systems Built …  |  🏆  Methodology / Projects Earned … ]
```

---

## 5. Content Patterns by Proposal Type

### 5.1 India · Live Multi-Day (Nucleus / Booking style)

```
Cover (navy + stats strip)
div() · sp()
h2("Objective", NAVY_HEAD)
body(...)

h2("Curriculum Overview", NAVY_HEAD)
- Who is this For: [audience]
- Delivery: Live Zoom
- Duration: [N] Full Days ([X] Hours Each)
- Tentative Dates: [if known]
- Tools: [grouped bullet list]
- Prerequisites: [4–6 bullets]

h2("Program at a Glance", NAVY_HEAD)
[5-col summary table]

For each day:
  dayHeader(N, NAVY_DAY_A | NAVY_DAY_B)
  [Objective + Tools mini-table]
  [Schedule table]
  [Part 1 … Part k]
  [Day N — [Client] Use Cases Practised]
  takeawayBox("End of Day N", ...)
  pb()

h2("Program Summary", NAVY_HEAD)
[Closing roll-up table]
[Every [Audience] Walks Away With panel]

[Commercials table — INR]

signOffBlock("India")
closingPage()
```

**Hour bands typically used:**
- 2 days × 9 hrs = 18 hrs (Nucleus pattern)
- 4 days × 6 hrs = 24 hrs (Booking pattern)
- 3 days × 6 hrs = 18 hrs (alternate)

### 5.2 US / Middle East / Other · Live Multi-Day (Gryphon style)

Same as 5.1 with these mandatory additions **before** the Objective:
- `h1("What is a [Role]?", NAVY_HEAD)` — definition box explaining the role/concept
- `h1("Program Overview", NAVY_HEAD)` — narrative paragraph framing the programme
- Optional: "What Changed From the Previous Version" callout (if versioned)
- Tool comparison table (e.g. Claude vs Copilot) when arguing for a specific stack
- Tagline accent in `GOLD` for positioning lines like "AI FORWARD DEPLOYED ENGINEER PROGRAMME"

Day-header colour default: `NAVY_DAY_B` (`#0D1F3C`).

For FDE-style programmes, embed the APR methodology section in Day 3 (second half): GOAT → IKM → PRIME → CAST → AND/ACE.

No commercials table in body — commercial sheet sent separately.

```
signOffBlock("US")  // or "MiddleEast" / "Other" — same logic
```

### 5.3 Self-Paced LMS (MCB style)

```
Cover (navy + Heading 1 title style instead of full stats strip)
h1("Objective", NAVY_HEAD)
h1("Curriculum Overview", NAVY_HEAD)
- Format: Self-paced LMS
- Short video modules (2–10 min)
- Quizzes, reading & hands-on assignments
- Total Hours: ~X hrs (Foundation) | ~Y hrs (Champion)
- Access Note: …
- Prerequisites: None / [list]
- Core Tools: [explicit named tools — usually Microsoft Copilot stack]
- Post-Programme Support: [playbook · cheat sheets · checklists]

h3("Program Storyline", "#000000")
[Module 1 — bold leading sentence + summary paragraph]
[Module 2 — …]
…
[AI Champions Module — Build & Deploy AI Agents]

h3("Tools", "#000000")
[grouped bullet list — Enterprise AI · Automation & Agents · Reference & Enrichment · Data & Reporting]

[Programme at a Glance — 9-col table]

["What Participants Walk Away With" — Foundation Track / AI Champions Track]

h1("Understanding [Client]'s Requirements", NAVY_HEAD)
  h2("1. Workforce Coverage & Personas", NAVY_SUB)
    [Dimension comparison table — Foundation Track | AI Champion Track]
  h2("2. [Client]'s Environment", NAVY_SUB)
  h2("3. Content & Engagement Preferences", NAVY_SUB)
  h2("4. LMS Integration", NAVY_SUB)

h1("Curriculum Design & Learning Architecture", NAVY_HEAD)
[Format | Duration | Purpose table]

For each module:
  h1("Module N — [Title]", NAVY_HEAD)
  [Theme | Estimated Time]
  Objective: …
  Tools Covered: …
  [Video Lessons table — N.1 to N.k]
  [Lesson-by-Lesson Breakdown — Concepts + Hands-On per lesson]
  [Reading Material]
  [Quiz & Assignment]
  h3("Module N — End of Day Outcome | [Title]", "#000000")
  pb()

h1("Optional Add-On — Industry Expert Masterclass", NAVY_HEAD)  // if applicable
h1("Delivery Methodology & LMS Integration", NAVY_HEAD)
  h2("Content Format & Instructional Design", NAVY_SUB)
  h2("LMS Integration", NAVY_SUB)
  h2("Localization & [Client] Customization", NAVY_SUB)

h1("Indicative Project Timeline", NAVY_HEAD)
h1("Next Steps", NAVY_HEAD)
  - Proposal review discussion — 60-minute call
  - Use case deep-dive
  - Tool walkthrough & access sharing
  body(bold12pt, "We look forward to building [Client]'s AI-ready workforce together.")
  ftr()  // "Acceler | Confidential"

signOffBlock(byGeography)
closingPage()
```

### 5.4 Custom / Multi-Persona (Cornerstone style)

- Use §5.1 or §5.2 structure but with persona-specific breakouts inside each day.
- Stats-strip column 2 should make multi-persona nature visible (e.g. *"PM + Design + Content Reps"*).
- A "Cross-Functional Capstone" must appear as the last build of the programme.

---

## 6. Numbering Configuration

```javascript
const NUM = { config: [
  { reference: "bul",  levels: [{ level: 0, format: BULLET, text: "•",  indent: { left: 320, hanging: 220 }}]},
  { reference: "sub",  levels: [{ level: 0, format: BULLET, text: "◦",  indent: { left: 520, hanging: 220 }}]},
  { reference: "arrw", levels: [{ level: 0, format: BULLET, text: "→",  indent: { left: 320, hanging: 220 }}]},
]};
```

- `bul` — primary bullets
- `sub` — sub-bullets
- `arrw` — "Walks Away With" outcome lists (MCB-style closing panel)

---

## 7. Page Layout

```javascript
const PAGE = { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }}};
// (1440 twips = 1.0 inch)
```

- **Page size:** Letter (8.5" × 11")
- **Default margins:** 1.0" all sides
- Tight margins (0.75" / 1080 twips) only when content density requires it on multi-day decks. Default to 1.0".

---

## 8. Sign-Off Block (Mandatory)

Every generated proposal ends with a clean text-based sign-off block on the second-to-last page, immediately before the closing "PLUG IN & ACCELERATE" cover.

### 8.1 Format

```
─────────────────────────────────────────────────────────
Prepared by:    Utkarsh Raj  ·  AI Product Manager, Acceler
Reviewed by:    [Region-specific reviewer per §8.2]
For queries:    [reviewer]@interviewkickstart.com
─────────────────────────────────────────────────────────
                                          Acceler | Confidential
```

- 11pt Manrope, body colour `#1A1A2E`, footer line 9pt `#999999` Nunito.
- Horizontal-rule paragraphs in `#CCCCCC` above and below.

### 8.2 Region → Reviewer Routing

| Client Geography             | Reviewed by (default)        | Override                                |
|------------------------------|------------------------------|-----------------------------------------|
| India                        | **Amit Joseph**              | Always Amit — no override.              |
| US / North America           | **Ryan** (sales-led)         | **Soham** if scope is new / tech-led.   |
| Middle East / GCC / UAE      | **Ryan** (sales-led)         | **Soham** if technical credibility is the gating risk. |
| Europe / UK                  | **Ryan**                     | **Soham** for tech-heavy.               |
| APAC (ex-India)              | **Ryan**                     | **Soham** for tech-heavy.               |
| Africa (e.g. Mauritius)      | **Amit Joseph**              | Amit handles the Indian-Ocean corridor. |
| Global / Multi-Region        | **Anshuman + Soham**         | Two reviewers listed.                   |

**Tech-led vs Sales-led disambiguator (US / ME / Other):**

- **Tech-led → Soham** when: scope is new curriculum, audience is non-tech but content is technical, feasibility is uncertain, technical credibility is the gating risk, or the proposal needs to win on engineering depth.
- **Sales-led → Ryan** when: scope is standard offering, audience-fit is the gating risk, pricing/commercial framing dominates, or the relationship is well-warmed.
- When in doubt, list both: *"Reviewed by: Ryan (commercial) · Soham (technical)"*.

### 8.3 What the Agent Must Do

1. Read the parsed RFP's `geography` field.
2. Apply §8.2 to pick the reviewer.
3. If `complexity ≥ 7` OR `curriculum_status` is *"100% new — full curriculum dev"*, upgrade to dual reviewer for US / ME / Other.
4. Insert the sign-off block in §8.1 format on the second-to-last page (before the closing cover).
5. Never invent an email — pull from the team directory or leave the email line as `[reviewer]@interviewkickstart.com` for human fill-in.

---

## 9. Writing Style Rules

### 9.1 Section Objectives

- One sentence. Active verb at start (Equip / Enable / Build / Develop / Train).
- Avoid *"In this section we will…"*. Go straight to outcome.

### 9.2 Bullets

- **Activities / Hands-On:** start with a hands-on verb (Hands-on, Build, Each engineer, Teams, Regroup).
- **Key concepts:** descriptive noun phrases explaining *why* the concept matters, not just naming it.
- **Outcome bullets:** single italic sentence per artifact; phrasing template *"Participants leave with: [artifact]"*.

### 9.3 Time Labels

- **Live:** *"Day N · [Theme]  (X hrs)"* or *"Day N · Session Title  (X hrs)"*.
- **Self-paced lessons:** *"N.1  —  [Title]  ·  X min"* (always integer min, never sub-minute).
- **Per-module estimate:** *"[Theme]  |  Estimated Time: X Hours"*.

### 9.4 Tool References

- Always name tools explicitly: **ChatGPT · Claude · Gemini · Copilot**. Never *"an AI tool"* or *"an LLM"*.
- For tool-agnostic positioning when the client has a preference: list 2–3 tools joined with `·` and add the inline note *"(tooling customisable to your stack)"*.
- **Microsoft-stack clients** (MCB, internal Copilot deployments): lead with **Microsoft Copilot Chat · Copilot in M365 Apps · Power Automate · AI Builder**. ChatGPT only appears in *"Reference & Enrichment"* context.

### 9.5 Client Voice

- Use the client's name literally and consistently. Never *"the client"*, *"your company"*.
- Reference real client context where confirmed in the RFP (industry, geography, regulator — e.g. Bank of Mauritius for MCB, PCI-DSS for fintech, FY26 priorities for Booking).
- Do **not** reference internal Acceler nicknames or shorthand in client-facing copy.

### 9.6 Avoid

- *"In conclusion"*, *"To summarise"*, *"As mentioned above"* (proposals are read non-linearly).
- Generic outputs: *"improved skills"*, *"better understanding"*, *"enhanced productivity"*. Always specific and measurable.
- Speculative tool claims (*"Copilot will save you 10 hours a week"*). Use observed value statements (*"Reduces SOP review from 2 hrs to 90 seconds — observed in [Client] pilot"*).
- Placeholder text in delivered output (`[CLIENT NAME]`, `TBD`, `xxx`).

---

## 10. Quality Checklist

Before marking a generated proposal review-ready, the agent must self-verify:

- [ ] Cover has: navy bg, "BY UnO UPWARD AND ONWARD" eyebrow, partnering line, tagline, "Proposal For" + client + month-year, big bold title, positioning subtitle, 4-icon stats strip.
- [ ] Primary section headings use `#1C4587`.
- [ ] Day-header colour is consistent throughout (either `#1A2B4A` **or** `#0D1F3C`, not mixed).
- [ ] Program at a Glance table has the mandated columns (5-col live / 9-col self-paced).
- [ ] Every live day has Schedule table + Part tables + Use Cases table + 🎯 End-of-Day box.
- [ ] Every self-paced module has Video Lessons table + Lesson-by-Lesson breakdown + Reading Material + Quiz/Assignment + End-of-Module Outcome.
- [ ] Program Summary closing table + "Every [Audience] Walks Away With" panel present.
- [ ] Tools are explicitly named (not "an AI tool").
- [ ] Client name appears correctly in every section (no placeholder leaks).
- [ ] No section ends abruptly mid-table; every day or module ends with a takeaway and a page break.
- [ ] **Sign-Off Block (§8) present with correct region-specific reviewer.**
- [ ] Footer `Acceler | Confidential` on content pages (self-paced only).
- [ ] Closing page: navy "PLUG IN & ACCELERATE".
- [ ] Validated with `validate.py` before copying to outputs.

---

## 11. File Naming Convention

```
[Client]_[Programme]_[Region]_v[N].docx
```

Examples:
```
Nucleus_AI_Builder_India_v1.docx
Booking_GenAI_Engineering_Accelerator_India_v2.docx
Gryphon_FDE_Programme_US_v3.docx
MCB_AI_Copilot_SelfPaced_Mauritius_v1.docx
Cornerstone_MS_Copilot_MasterClass_US_v1.docx
```

- Use underscores, not spaces.
- Region tag is required (`India`, `US`, `UAE`, `Mauritius`, etc.).
- Version bumps:
  - `v1` → first draft
  - `v2` → after Soham technical review
  - `v3` → after Aashish positioning review
  - `final` → after Amit / Ryan commercial approval

---

## 12. Build Script Pattern

Every proposal is built as a single Node.js script using the `docx` npm package:

```javascript
// 1. Import docx primitives + define COLOUR constants (§2)
// 2. Define BORDERS (bd, bds, nb, nbs)
// 3. Define typography helpers (sp, pb, div, h1, h2, h3, body, bl, ftr)
// 4. Define table helpers (hc, dc, dvc, rc, emojiCell)
// 5. Define NUM (§6) and PAGE (§7) constants
// 6. Build content array:
//    coverPage()
//    → objective()
//    → curriculumOverview()
//    → programAtAGlance()
//    → days.map(renderDay)   OR   modules.map(renderModule)
//    → programSummary()
//    → walkAwayPanel()
//    → commercials()         // India only
//    → signOffBlock(region)  // §8
//    → closingPage()
// 7. Wrap in Document, call Packer.toBuffer, write to /sessions/.../outputs/
// 8. Validate: python3 validate.py <file> 2>&1 | grep -E "Paragraphs|PASSED|FAILED"
// 9. Copy to /Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/
```

### 12.1 Target Paragraph Counts (Sanity Bounds)

| Proposal Type                                    | Target Paragraph Count |
|--------------------------------------------------|------------------------|
| India · 2-day Live (Nucleus-style)               | 180–230                |
| India · 4-day Live (Booking-style)               | 280–360                |
| US/ME · 4-day Live FDE-style (Gryphon)           | 320–400                |
| Self-Paced · 4-module 20 hrs (MCB Foundation)    | 480–620                |
| Self-Paced · 5-module 30 hrs (AI Champion)       | 600–780                |
| Custom multi-persona (Cornerstone-style 3 hr)    | 140–200                |

A draft outside these bands signals either missing sections (low) or over-elaboration (high) — re-validate against §10 before sending for review.

---

## 13. Sources

This SKILL.md is distilled from:

- **Nucleus Software** — `Sample Proposals/Proposal_India_Sample.docx`
  *AI Builder Programme · 2-day Live · India · Fintech · From AI-Assisted Coding to Production-Grade Agentic AI*
- **Booking Holdings** — `Sample Proposals/Sample_Proposal_India.docx`
  *Advanced GenAI Engineering & Productionization Accelerator · 4-day Live · India · Trust & Safety + Fraud Engineering*
- **Gryphon Investors** — `Sample Proposals/Sample_Proposal_US.docx`
  *AI Forward Deployed Engineer Programme · 4-day Live · US · Portfolio-company operational AI + APR methodology*
- **MCB Mauritius** — `Sample Proposals/Sample_Proposal_Self-Paced_Program.docx`
  *AI Learning & Capability Building Programme · Self-Paced LMS · ~20–30 hrs · Microsoft Copilot stack*

The Mini-UT behavioural context (decision logic, classification, routing, escalation, pricing, quality gates) lives in `Mini-UT Context/context.md` and `Mini-UT Context/utkarsh_context.md`.

---

*v2 · May 2026 · Acceler / Interview Kickstart B2B · Pre-Sales Agent — Component 3 (Proposal SKILL.md, geo × delivery matrix)*
