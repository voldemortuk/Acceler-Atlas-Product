---
description: "Score a pre-sales brief against the Acceler 33-question Discovery Checklist. Returns strength % + section breakdown + must-ask gaps."
argument-hint: "<meeting notes or path to notes file>"
---

Score the brief below against the Acceler Discovery Checklist. Use the skill at `skills/discovery-checklist/SKILL.md`.

## Input

```
$ARGUMENTS
```

If the input is a file path, read it first.

## Output (markdown)

```
# Discovery Strength — [Client name if known]

**Overall: X% complete**  ·  Verdict: [Ready to Propose / Gaps Remain / Thin Brief]

## Section breakdown
| Section | Score | Status |
|---|---|---|
| Why They're Here    | X/6 | … |
| Who's in the Room   | X/5 | … |
| When & How          | X/5 | … |
| Tools & Access      | X/6 | … |
| What They Want Built| X/5 | … |
| Money & Timeline    | X/5 | … |

## Critical questions unanswered (must-asks)
- [list each red question not addressed in the brief]

## Recommended next move
- If ≥ 80% → Ready to propose. Move to `/acceler:similar` then `/acceler:proposal`.
- If 50–79% → Proceed but flag these gaps under "Open Questions for the Client" in the proposal.
- If < 50% → STOP. Book a 30-min follow-up call. Send the must-asks first.
```
