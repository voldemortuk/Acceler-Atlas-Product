---
description: "Draft an IK-Acceler proposal document from a brief. Follows Doc_Proposal_Skills.md v2 (Nucleus / Booking / Gryphon / MCB house style)."
argument-hint: "<brief notes, or 'use last' to continue from /acceler:similar output>"
---

Draft a first-level proposal in IK-Acceler house style for the brief below.

## Input
```
$ARGUMENTS
```

## How to draft

1. Read the proposal skill: `skills/doc-proposal/SKILL.md` (it has the full house style: cover format, palette, fonts, section order, sign-off routing).
2. If `/acceler:similar` was run earlier in this session, use the recommended precedent as the structural anchor — lift section rhythm and day breakdown.
3. If `/acceler:discovery` was run, honour the strength score: flag the unanswered must-asks under "Open Questions for the Client" at the end. Never invent client-specific facts.

## Output format (markdown — start with the [COVER] frontmatter)

```
[COVER]
client: [Client Name]
programme: [Programme Name]
title: Draft Proposal | [Programme Name] For [Client]
subtitle: [Positioning subtitle — one line]
partnering: Partnering with [Client] on its journey to [strategic intent]
tagline: AI enabling orgs for 100X productivity
date: [Month Year]
geography: [region]
delivery: [delivery format]
day_header: 1A2B4A
stat_1: 🏦 | Focus | [value]
stat_2: 👨‍💻 | Audience | [value]
stat_3: 📅 | Duration | [value]
stat_4: ⏱️ | Hours | [value]
[/COVER]

## 1. Objective
[Single-sentence with active verb]

## 2. Curriculum Overview
**Who is this For:** …
**Delivery:** …
**Duration:** …
**Tools:** Tool · Tool · Tool
**Prerequisites:**
- …

## 3. Program at a Glance
[5-col: # | Day Title | Duration | Focus | Key Build]

## 4. Day-by-Day Breakdown
### Day 1 · [Theme] (X hrs)
**Objective:** …
**Tools:** …
**Schedule:** [table]
**Part 1 — [Title] · X min** — Objective / Concepts / Hands-On
[…repeat parts…]
**Day 1 — [Client] Use Cases Practised** [4-col table]
> **🎯 End of Day 1 — What [Audience] Build & Walk Away With**
> - Artifact 1
> - Artifact 2

[…repeat days…]

## 5. Program Summary
[Roll-up table]
**Every [Audience] Walks Away With**
- 🛠️ Systems Built: …
- 🏆 Methodology Earned: …

[For India clients ONLY — INR (₹) strictly:]
| Particulars | Amount (INR) |
|---|---|
| … | ₹… |

## Sign-Off Block
Prepared by: Utkarsh Raj · AI Product Manager, Acceler
Reviewed by: [India → Amit Joseph · US/ME/Other → Ryan or Soham · Africa → Amit · Global → Anshuman + Soham]
For queries: [reviewer]@interviewkickstart.com

Acceler | Confidential

## ⚠ Open Questions for the Client
[Only items the notes left unclear — never invent client-specific facts]

[CLOSING]
[/CLOSING]
```

## Save

Save the markdown to:
```
~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/[Client]_[Programme]_v0.1.md
```

Offer to also produce a styled HTML version (which the user can then print-to-PDF or open in Word) using the same content + the IK-Acceler navy cover/closing CSS.
