---
description: "POST-SESSION stakeholder report. Generate the day-N-recap-report HTML analytics page for the client sponsor / L&D stakeholder: KPIs, per-learner tier categorisation with evidence, engagement by topic, feedback breakdown, action items. For the learner-facing recap, use /acceler-presales:session-recap instead."
argument-hint: "<day number + feedback export/chat log/transcript, or a path to them>"
---

Generate a stakeholder-facing post-session analytics report for this brief.

## Input
```
$ARGUMENTS
```

## How to build

1. Read `skills/session-recap/SKILL.md` in full first, especially **§0** (the data pointers to ask for upfront) and **§3** (stakeholder report structure).
2. This artifact is evidence-driven. If the feedback export, chat log, or transcript aren't provided, ask for them before drafting — don't fabricate names, quotes, or ratings.
3. Confirm the tier-assignment rule with the user before applying it: Beginner/Intermediate/Advanced is assigned from what each learner actually did and asked **that specific day**, never from tenure or job title. State this in the report's own section note.
4. If a prior day's report exists in this session or repo, reuse its exact design tokens and component classes (`.tier-grid`, `.ev-grid`, `.metric-grid`, etc.) so the series stays visually consistent.
5. Follow §4 (prose style) while writing every note, quote caption, and action item.
6. Run the §5 build checklist before presenting the result.
