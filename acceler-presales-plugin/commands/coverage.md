---
description: "Build a 3-column RFP coverage matrix — Requirement → Module → Topics — with honest gap flagging (⚠ GAP / ⚠ THIN / partial). Routes gaps to the 6 standard Masterclasses."
argument-hint: "<client name + RFP requirement list (numbered)>"
---

Build a coverage matrix mapping client RFP requirements to Acceler programme modules.

## Input
```
$ARGUMENTS
```

## How to build

1. Read `skills/requirement-mapping/SKILL.md` (or the project-folder `Session_Mapping_Skills.md`).
2. Keep the client's RFP numbering verbatim.
3. Use the mapping notation:
   - `Day 1 — [Theme]`
   - `Day 2-3 — [Theme]`
   - `Day 3 → Day 4 — [Theme]`
   - `Day 4 + [Masterclass]`
   - `partial`
4. Anchor topics to the client's domain use cases in parens.
5. Flag gaps honestly — ⚠ GAP (not scoped), ⚠ THIN (touched but shallow), partial (covered in part).
6. Last two rows:
   - **Flagship use case** → mapped to Capstone / Agentic Fest
   - **Masterclasses row** (6 standard: Cost Engineering · Reliability/AI-SRE · AI Product Thinking · HITL & Trust · Experimentation & Lifecycle · Advanced Agentic AI)

## Output

```
# [Client] — RFP Coverage Map

| [Client] Requirement | Acceler [Programme] — Mapping | Module Topics |
|---|---|---|
| 1. … | Day 1 — Foundations | Prompt engineering; RAG basics; (loan eligibility queries) |
| 2. … | Day 2-3 — Orchestration | LangGraph; ReAct; MCP/A2A; (KYC API scaffold) |
| ⚠ 3. … | GAP: Voice STT/TTS — confirm scope | Route → Reliability Masterclass |
| ⚠ 4. … | THIN: production observability | Route → Reliability/AI-SRE Masterclass |
| 5. … | Day 4 — concept | High-level only; full hands-on routes to deep dive |
| [Flagship use case] | Capstone / Agentic Fest Sample | [Use case build] |
| Masterclasses | Cost Eng · Reliability · AI Product Thinking · HITL & Trust · Experimentation · Advanced Agentic | [Each in 1 line] |

## Coverage Summary
- Total requirements: X
- Fully covered: Y
- Partial / THIN: Z
- GAP: W

## Notes
- [Anything the client should know about scope boundaries]
```

Save to:
```
~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/[Client]_coverage_v0.1.md
```

Optional follow-up: generate an XLSX version (openpyxl) with peach-shaded GAP rows for the client appendix.
