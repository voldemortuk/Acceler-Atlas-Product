---
description: "Find the best instructors for a domain from the Acceler Knowledge Graph (773 indexed profiles). Ranked by topic match, geography, tier."
argument-hint: "<domain or topic + geography + budget posture>"
---

Find instructors matching this brief from the Acceler Knowledge Graph.

## Input
```
$ARGUMENTS
```

## How to query

1. Read `knowledge/instr_candidates.json` — the indexed pool (773 instructors with LinkedIn URLs, roles, topics).
2. Cross-reference `knowledge/graph.json` for:
   - `expert-in` edges (instructor → topic)
   - `proposed-for` edges (instructor → past clients)
3. Filter by:
   - **Topic match** (primary) — instructor's `expert-in` topics overlap with the brief's domain
   - **Geography** (if specified) — bias toward instructors with relevant past engagement
   - **Tier** (if specified) — FAANG+ / Standard / Tier-1 India / Special
   - **Availability** — deprioritise anyone already heavily engaged with this client (via `proposed-for`)

## Tier reference

| Tier | India rate | US rate | Use when |
|---|---|---|---|
| FAANG+ | ₹5-7K/hr | $200+/hr | High credibility, exec audience |
| Standard | ₹55/hr ($55) | $110/hr | Default AI Builders |
| Tier-1 India | ₹30-40/hr | — | India budget-tight |
| Special / Leadership | — | $350-450/hr | Niche / leadership / non-tech |

## Output

```
# Instructors for: [Domain]

**Recommended tier for this brief:** [Tier] — [why]

## Top matches from the knowledge base

### 1 · [Name]
- **Role:** [from instr_candidates.json]
- **LinkedIn:** [URL]
- **Topic match:** [topics they're expert in that overlap the brief]
- **Past delivery:** [previous Acceler engagements if any from proposed-for edges]
- **Why they fit:** [1 line]

### 2 · [Name]
[same shape]

### 3 · [Name]
[same shape]

## If no strong match (10% edge case)

If the domain is one we don't have an SME network for (Capgemini AI for Sales pattern), say so honestly. Recommend:
- LinkedIn search filters to use
- 2-3 sample profile shapes the team can source against
- Loop in [Animesh / Navdeep / domain-appropriate sourcer] internally to source

## Notes
- [Anything the brief reveals that should influence selection — language, time zone, regulated industry constraints, certifications needed]
```
