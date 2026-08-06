---
name: session-recap
description: "Build the two POST-session recap artifacts that follow every live delivery day of a multi-day B2B training program: the day-N-learner-recap (learner-facing HTML page — topics covered, quiz/discussion, cheat sheet, hands-on labs, parked questions, resources) and the day-N-recap-report (stakeholder-facing HTML analytics page — KPIs, tier categorisation, engagement, feedback breakdown, action items). Covers the exact data pointers to ask for upfront, the design system and component library for each, section-by-section structure with last-day branching logic, and the prose style rules both must follow. Companion to [[live-session-deck-skills]] (the deck this recaps) and [[html-deck-skills-acceler-kase-engine]]."
---

# Session Recap Builder — SKILL.md (v1)

Every live delivery day produces two companion artifacts, built right after the session:

| | **Learner recap** (`dayN-learner-recap/`) | **Stakeholder recap report** (`dayN-recap-report/`) |
|---|---|---|
| Audience | The learners who sat through the session | The client sponsor / L&D stakeholder who is paying for the program |
| Job | Teach: re-deliver the content so a learner who zoned out or missed something can catch up | Prove: show who engaged, how, and what to fix next |
| Content | Topics covered, takeaways, cheat sheet, hands-on labs, parked Q&A, resources | Attendance/feedback KPIs, per-learner tier categorisation with evidence, engagement by topic, action items |
| Tone | Warm, second-person, teaching | Neutral, evidence-first, named individuals |
| Not every day needs | A "recap report" — some programs only commission a stakeholder report for select days (check with the client contact) | — |

Both are single-page static HTML, no build step, deployed as siblings under one Vercel project (e.g. `lvt-post-session`), one folder per artifact. A final `post-program-assessment-solution/` sibling (if the program has a graded assessment) closes out the series and is linked from the last day's learner recap.

---

## 0. Ask for these data pointers before you start

Don't guess this content. Ask the user for it, or point at where it lives, before drafting either artifact. Missing any of these is the single biggest cause of a recap that reads generic.

### For the learner recap
- **Program/day identity:** client name, program name, day number of how many, session date, instructor name.
- **Instructor bio + photo** — only needed the FIRST time an instructor appears in the series, or on a handoff day (see §3.1). Don't re-ask for days where the instructor is unchanged.
- **Whether the instructor changed since last time** — if yes, get the outgoing/incoming names and whether it's driven by learner feedback (for the handoff note's framing).
- **The actual session content**, part by part: what topics/parts were covered, the key sub-points under each (usually pulled from the slide deck + instructor's own session notes, not invented). Ask for the slide deck PDF and any session repo link.
- **Whether a scored quiz ran that day** — determines "Quiz Solutions" (scored `.q` format with per-question ✓ answer) vs a single "Check Your Understanding" discussion question (`.pk` format) if no quiz ran.
- **Key takeaways** — usually 6, either already summarized by the instructor or synthesized by you from the parts above.
- **Cheat sheet commands/shortcuts** introduced that day.
- **Hands-on lab guides**: repo links, clone instructions, guide file paths, estimated time per demo.
- **Questions parked or rushed during the live session** — the chat log and/or session transcript. You need the exact question text and who asked it (or "parked, no name") to answer properly rather than inventing a generic FAQ.
- **Session resources**: slide PDF filename, any guide PDFs, repo links.
- **Additional resources**: anything the instructors called out explicitly as worth sharing post-class.
- **Chat log highlights**: links/tools learners or staff dropped in chat worth preserving.
- **Is this the LAST day of the program?** Governs the closing section: mid-program days get "Before Day N+1" (a nudge list + a commit-daily callout); the last day gets "Wrapping Up" (a synthesis of the whole program) plus a "Post Program Assessment" link section if the program has a graded assessment.
- **Diagrams/screenshots** to embed, with filenames — get the actual image assets, don't describe a diagram in prose when an image exists.

### For the stakeholder recap report
- **Enrollment count** and **attendance count for this specific day**.
- **Feedback form responses**: per-respondent ratings across the 5 standard metrics (content relevance, speaker knowledge, teaching skills, interactivity, questions addressed), plus recommend-instructor Y/N. Get the raw export, not a summary — you need per-person numbers to compute per-tier breakdowns correctly.
- **The chat log and/or session transcript** — this is what tier categorisation and engagement counts are built from, not attendance or job title.
- **Learner roster with titles/roles** — needed for the Leaders-vs-ICs cut (which feedback link a respondent received; note that a technical IC who happened to receive the Leaders-form link is still counted as an IC, consistent with prior days in the series).
- **Confirm the tier-assignment rule with the user before applying it**: tiers (Beginner / Intermediate / Advanced) are assigned from what each learner actually *did and asked that specific day*, never from tenure or job title. State this explicitly in the report's section note — it's a recurring point of confusion.
- Everything above needed for the learner recap (topics list) is also needed here, to classify questions by topic.

If any of these are missing, ask before drafting rather than inventing plausible-sounding names, quotes, or numbers — both artifacts are read as factual records of a real session.

---

## 1. Shared foundations

### 1.1 Palette (learner recap)
```
--bg:      #f7f9fc   /* page background */
--ink:     #262533   /* headings, dark surfaces (rhead, foot-bar, callout) */
--accent:  #f86b3c   /* orange — eyebrows, links, accent borders, ticks */
--text2:   #475569   /* body text */
--muted:   #94a3b8   /* labels, captions */
--border:  #dce2ee   /* card borders */
--card-bg: #eef1f7   /* subtle fills (code chips) */
```
Fonts: `DM Serif Display` (headings/h2/pk-q), `DM Sans` (body), `JetBrains Mono` (code). Load via the same Google Fonts `<link>` every recap uses.

### 1.2 Palette (stakeholder report)
```
--bg:      #f4f4f2   /* page background — warmer gray than the learner recap */
--ink:     #1a1a1a   /* body text, dark header */
--accent:  #c2410c   /* darker orange than the learner recap's #f86b3c — deliberate, keeps the two artifacts visually distinct */
--tier-beg: #0f766e  /* Beginner tier — teal */
--tier-int: #7c3aed  /* Intermediate tier — purple */
--tier-adv: #c2410c  /* Advanced tier — orange, same as accent */
--tier-lead: #1e3a8a /* Leaders lens — navy */
--tier-ic:   #0369a1 /* ICs lens — blue */
```
Fonts: `DM Serif Display` + `DM Sans`, no monospace (no code in this artifact). Each tier card carries its color via a CSS custom property (`--tier`) set per wrapping class (`.t-beg`/`.t-int`/`.t-adv`), so donut charts, bars, and borders all inherit it instead of being hand-colored per element.

### 1.3 Both use the same `.rhead` cover pattern
A dark (`#262533`) header bar, not a full-height cover slide: `.lock`/`.cover-lockup` (Acceler + client logo pill), `h1` in DM Serif Display, a `.pill` badge (`Day N of Total · date`), and a `.cover-meta` row of topic tags with orange bullet dots. Copy this bar byte-for-byte between days; only the day number, date, title, and topic tags change.

---

## 2. Learner recap — structure

### 2.1 Section order and IDs
Every `.sec` needs a stable `id` (used by the TOC, the floating nav, and the comments widget's `data-cmt`). Standard order, skip what doesn't apply that day:

1. `#instructor` **Your Instructor** — ONLY on the day an instructor is newly introduced. Bio card (`.meet`): photo, technical specializations list, career highlights, academic/teaching background. If the instructor is changing *starting* this day, also add a `.handoff` note above the TOC ("A Note for Day N" + one-line reason, usually "we heard your feedback") — but never both a handoff note AND a full bio reintroduction for a day where the instructor is unchanged from last time.
2. `#covered` **What We Covered** — the day's parts (`.part` cards, numbered `01`, `02`...), each with a bulleted `<ul>` of sub-points (bold lead-in + explanation per `<li>`). Embed diagrams inline (`.diag` with a maximize-icon lightbox button, see §2.3) where the slide deck has one.
3. `#takeaways` **Key Takeaways** — a 2-column grid (`.tks`) of ~6 cards, each a short header + 1-sentence expansion.
4. `#cheatsheet` **Cheat Sheet** — a 2-column `<table>` of command → what it does.
5. Either `#questions` **Questions We Parked or Rushed** (use `.qa` badge format, §2.4) then `#quiz` **Quiz Solutions** (scored `.q` format, §2.4) if a quiz ran, OR just one `#understanding` **Check Your Understanding** section (`.pk` single discussion question) if it didn't. Order questions-then-quiz if both exist, matching the day's own chronology.
6. `#handson` **Hands-On Labs** — `.pk` cards, one per demo/lab: repo clone command, what it proves, time estimate. Optionally an embedded `.browser` iframe walkthrough if a hosted guide exists.
7. Mid-program only: `#before` **Before Day N+1** — a `.pps` 2-column grid of nudges + a dark `.callout` reinforcing the "commit daily" habit.
   Last day only: `#wrapup` **Wrapping Up** — a synthesis of the whole program (not just the day), same `.pps` + `.callout` shape, plus `#assessment` **Post Program Assessment** linking to the assessment-solution sibling if the program has one.
8. `#resources` **Session Resources** — `.mat`/`.mt` cards linking the slide PDF, session repo, and any guide PDFs.
9. `#additional` **Additional Resources** — anything called out explicitly as worth sharing post-class.
10. Optional: `#stretch` **Optional Stretch Track** — advanced/self-paced assignments, gated behind the guided labs (`.assess` card).
11. `#chat` **From the Chat** — a `<table>` of link → 1-line context, sourced from the actual chat log.

### 2.2 The floating TOC + section nav (add on every recap)
- A `.toc-card` right after `<div class="wrap" id="start">`: chip row (`.toc-chip`) linking every section, numbered to match.
- A `.nav-fab` floating button (bottom-right) + `.nav-panel` slide-up menu + `.nav-back` overlay, same markup and ~30-line vanilla-JS controller on every recap (scroll-position-based active-section highlighting, `y + 130` offset). Copy this JS verbatim; it needs zero changes per day.
- `html{scroll-behavior:smooth}` and `.sec{scroll-margin-top:24px}` so anchor jumps land below the fixed elements.

### 2.3 Diagram/image component
`.diag` card wrapping an `<img>` capped at `max-width:560px` (not full-bleed — a full-width diagram reads oversized in a 1060px-wide column) plus a `.diag-cap` italic caption below. Add a small circular maximize-icon button (`.diag-view`, inline SVG, no text) in a `.diag-head` row above the image; clicking it opens an **in-page lightbox** (dark overlay, image capped at `92vw`/`88vh`, close button + click-outside + Escape to close) — never a plain `<a href="image.png" target="_blank">`, which navigates the browser to a bare image on its own page instead of staying on the recap.

### 2.4 The two Q&A component styles — don't mix them up
- **`.qa`** (badge format): used for "Questions We Parked or Rushed." Two-column grid per card (`.qa-rail` with a numbered circular badge `Q1`, `Q2`… + `.qa-body` with the question in serif and the answer prefixed by a small square "A" lead-in span). Reserve this for real questions attributed to the live session that got a delayed/proper answer.
- **`.q`** (scored quiz format): used only when an actual multiple-choice quiz ran. Each `.q-o` option list has exactly one `li.ok` (correct, green background, trailing `<span class=tick>✓</span>`) and a `.q-w` explanation below the options.
- **`.pk`** (plain card format): used for everything else that's a question-and-answer-shaped block but isn't either of the above — single discussion questions, hands-on lab entries, additional-resource entries. `.pk-q` (serif question) + `.pk-a` (prose answer).

---

## 3. Stakeholder recap report — structure

### 3.1 Section order
1. **KPI cards** (`.kpi-grid`): total enrolled, present today (X/Y, %), feedback submitted (X/Y, %), overall avg rating, recommend-instructor %.
2. **Learner Categorisation** (`.tier-grid`, 3 columns: Beginner / Intermediate / Advanced): each tier card states its count, its rating/response/recommend stats, and a per-learner row (`.tier-row`) with name + a one-line, specific, evidence-based note (what they actually asked or did that day — never a generic "engaged well"). State the tier-assignment rule in a `.section-note` directly above the grid every time (see §0): assigned from that day's actual behavior, not tenure.
3. **The Evidence Behind the Tiers** (`.ev-grid`, 3 columns): 3-4 direct quotes per tier, each attributed by name and source (`Chat` / `Transcript`). Real quotes only — pull from the actual chat export/transcript, never paraphrase into a quote.
4. **[Day], Read by Tier** (`.bytier-row` donut cards + `.split-2` panels): rating-by-tier donuts, a "Questions Asked, by Tier" bar panel, and a "What That Tells Us to Change" panel (`.chg` rows) — concrete, actionable, tied to something specific that happened that day.
5. **Per-Tier Metric Breakdown** (`.metric-grid`): all 5 feedback metrics broken out per tier, with the lowest-scoring cell per tier flagged (`.metric-flag`). Confirm in the section note that every number reconciles to the cohort-wide figures already shown in the KPI cards.
6. **Ratings by Audience — Leaders vs Individual Contributors** (`.aud-grid`): same 5-metric breakdown, cut by which feedback-form link the respondent received instead of by tier. Note any respondent whose form-link and actual role diverge (see §0).
7. **Engagement** (`.split-2`): "Questions by Topic" (stacked bars, legend for question-type breakdown: conceptual/hands-on/platform-product/fragment) and "Who Asked · Top N" (ranked asker list with tier badges).
8. Optional, only if the source deck defines them and the day has content for them: Themes, Quotes, companion Assessment card (`.assess`) — these CSS components exist in the reference build but are not used on every day; include only what that day's data actually supports.

### 3.2 Tier-card evidence rows — the part that takes real editorial judgment
A tier-row note like *"Asked how review agents surface findings"* is far more useful to the client than *"actively engaged."* Write one for every present learner, in every tier, including Beginners (whose notes are often "no questions all day" or a warm sign-off with zero technical engagement — that absence is itself the data point for that tier).

---

## 4. Prose style (both artifacts)

Both recaps are written prose, not quoted transcripts of quiz answers or `<code>` content, so the standing writing rules apply to every paragraph, list item, and quiz-answer explanation you author:

- **No em-dashes.** Use a comma, a colon, parentheses, or split into two sentences, whichever reads best for that specific sentence. Vary the fix; don't mechanically replace every dash with the same punctuation.
- **No 3-item rhetorical cadence** — the "X, Y, and Z" triad used as a stylistic flourish. A genuine enumerated list (five tools, ten checks) is fine; the ban is on manufacturing a rhythmic triad for effect.
- **No "it's not an X, it's a Y."**
- **No "X is not just a Y, it's the whole point."**
- **No antithesis-as-a-crutch** ("not because it's easy, but because it's hard").
- These bans don't apply to direct quotes from the session (chat/transcript excerpts, a named quotable line from the instructor's own deck) or to `<code>` content — only to your own connective prose.

Before shipping either artifact, grep the file for `&mdash;` and confirm zero remain outside `<style>`/`<script>` and outside direct quotes.

---

## 5. Build checklist
- [ ] All data pointers in §0 collected or explicitly confirmed missing/not-applicable with the user.
- [ ] Every `.sec` has a stable `id`; TOC chip count and nav-panel link count both match the actual section count.
- [ ] Diagrams use the capped-width `.diag` + lightbox pattern, not full-bleed `<img>` or a plain new-tab link.
- [ ] Correct Q&A component chosen per §2.4 (don't use `.q` scored format for a day with no real quiz).
- [ ] Last-day branching applied correctly (Wrapping Up + assessment link vs Before Day N+1).
- [ ] Instructor bio/handoff section included only when actually warranted that day (§3.1 / §0), not copied forward out of habit.
- [ ] Stakeholder report's tier assignments are justified by that day's actual chat/transcript evidence, and the tenure-vs-behavior rule is stated in the section note.
- [ ] Zero `&mdash;` outside quotes; no antithesis-crutch constructions in your own prose.
- [ ] Folder deployed as a sibling under the program's existing Vercel-connected repo (e.g. `dayN-learner-recap/`, `dayN-recap-report/`), matching the naming of prior days in the same series exactly (case, hyphenation).
