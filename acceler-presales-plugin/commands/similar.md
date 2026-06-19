---
description: "Find the top 3-5 closest precedents in the Acceler Knowledge Graph for a new brief. Returns client + programme + pricing band + tools + linked files."
argument-hint: "<brief description: industry, programme type, scale, geography>"
---

Find the top closest precedents in the Acceler Knowledge Graph for this brief.

## Input
```
$ARGUMENTS
```

## How to query

1. Read `knowledge/INDEX.md` for a fast scan of all 61 clients with their programmes, tools, and pricing bands.
2. Read `knowledge/graph.json` if you need edge-level data (file → tool, file → topic, instructor → topic).
3. Read `knowledge/USING_THE_KG.md` for the agent-facing query patterns.

Match precedents by (in priority order):
1. **Industry / domain** match (BFSI / fintech / telecom / SaaS / consulting / PE / etc.)
2. **Programme** match (AI Builder · AI Leaders · AI Enablers · Custom · Masterclass)
3. **Scale** match (batch size band · live hours band)
4. **Geography** match (India / US / GCC / Europe / APAC / Africa)

## Output

```
# Closest Precedents — [client name from brief]

## Best match: [Client X]
- **Programme:** [name]  ·  **Year:** [if known]
- **Why it fits:** [1-line — industry × programme × scale]
- **Pricing band:** [from INDEX.md — rates, deal size, margin if available]
- **Tools used:** [top 5]
- **Files:** [paths from graph.json, relative to ~/Downloads/1. PowerUp/]

## Second match: [Client Y]
[same shape]

## Third match: [Client Z]
[same shape]

## Recommended anchor
**Use [Client X] as the primary template.** Lift structure, day-by-day rhythm, and pricing band. Customise client-specific facts (audience profile, industry references, capstone use case).

## Why other patterns didn't fit (optional)
[1-2 lines acknowledging deals you considered but ruled out — Edelweiss-style long-format too heavy for a 2-day · MCB self-paced wrong delivery model · etc.]
```

If no clean match exists (truly novel domain or programme), say so honestly and recommend Custom build with NPT consultation.
