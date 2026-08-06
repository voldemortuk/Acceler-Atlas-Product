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

1. Read `knowledge/graph.json` — the real instructor pool lives here as `instructor` nodes (773), each with `label`, `role`, `expertise`, `topics`, `clients`, `linkedin`, `count`. (`instr_candidates.json` is only a file index, not the instructor pool.)
2. Use the edges:
   - `proposed-for` (instructor → client/file) — real delivery/engagement footprint
   - topic membership via each instructor's `topics` array (the `expert-in` edge runs topic → instructor)
3. Read `knowledge/instructor_delivery_flags.json` — human override of who is actually staffable (the KG cannot know this).
4. Filter by:
   - **Topic match** (primary) — instructor's `topics` overlap the brief's domain
   - **Geography** (if specified) — bias toward instructors with relevant past engagement
   - **Tier** (if specified) — FAANG+ / Standard / Tier-1 India / Special
   - **Availability** — deprioritise anyone already heavily engaged with this client (via `proposed-for`)

## Pre-sales vs post-sales (ALWAYS apply)

The KG ranks on topic + credibility; it cannot tell you who Acceler can actually hire. Two different jobs:

- **Pre-sales shortlist (proposal credibility):** marquee names that win the pitch. Marquee external keynote/author names are fine here.
- **Post-sales shortlist (DELIVERABLE):** only SMEs we can actually staff. **Exclude every name in `instructor_delivery_flags.json → pre_sales_only`** (currently Cassie Kozyrkov, Michelle K. Lee, Eric Siegel). Rank the rest by a **deliverability heuristic**:
  - **+ active IK instructor** (role/expertise mentions "Instructor @ IK" / teaching / bootcamp) — most reliable
  - **+ dense real `proposed-for` footprint** (more past engagements = more staffable)
  - **+ in-house IK staff** (e.g. Head of Curriculum) = guaranteed
  - **− pure external marquee** with little/no `proposed-for` = treat as pre-sales only

**Default behaviour:** if the brief implies real delivery (words like *deliver, run, staff, who will teach, hire, post-sales, top N SMEs*), lead with the **Post-Sales (deliverable)** list and offer the pre-sales marquee names separately. If it's clearly only for a proposal, lead with pre-sales. When unsure, show **both** lists, clearly labelled. Never silently promote a `pre_sales_only` name into a deliverable list.

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

## Post-Sales — Deliverable shortlist (who we can actually staff)
[Lead with this when the brief implies delivery. pre_sales_only names are EXCLUDED here.]

### 1 · [Name]
- **Role:** [from graph.json]
- **LinkedIn:** [URL]
- **Topic match:** [topics overlapping the brief]
- **Deliverability:** [active IK instructor / in-house / N past proposed-for engagements]
- **Past delivery:** [clients from proposed-for edges]
- **Why they fit:** [1 line]

### 2 · [Name]
[same shape]
…(Top 5)

## Pre-Sales — Proposal-credibility names (marquee; confirm before promising delivery)
[List marquee names incl. any pre_sales_only ones, each tagged. Use to win the pitch, not to staff.]
- **[Name]** — [role] — ⚠ *pre-sales only: [reason from flags file]* / or *deliverable too*

## If no strong match (10% edge case)

If the domain is one we don't have an SME network for (Capgemini AI for Sales pattern), say so honestly. Recommend:
- LinkedIn search filters to use
- 2-3 sample profile shapes the team can source against
- Loop in [Animesh / Navdeep / domain-appropriate sourcer] internally to source

## Notes
- [Anything the brief reveals that should influence selection — language, time zone, regulated industry constraints, certifications needed]
```
