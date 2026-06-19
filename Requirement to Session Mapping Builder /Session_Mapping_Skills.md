---
name: session-mapping-skills-acceler-rfp-requirement-coverage-mapping
description: "How to build a Session / Requirement Coverage Mapping for Acceler B2B proposals — a 3-column matrix (client requirement → Acceler program day/module → topics covered) that proves RFP coverage, anchors topics to the client's use cases, and honestly flags GAP/THIN/partial coverage routed to masterclasses or scope confirmation. Includes the openpyxl build pattern. Companion to [[pricing-skills]], [[doc-proposal-skills]], [[deck-skills]]."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6d83a6a7-37dc-44fa-b73c-61e1418d2a82
---

# Acceler Session / Requirement Coverage Mapping — SKILL.md

A **coverage matrix** that maps every client requirement (from their RFP / requirement list) to the exact Acceler program day(s)/module(s) that deliver it, with the topics covered — and **honestly flags gaps**. It proves the proposal answers the brief, surfaces gaps before the client does (trust + masterclass upsell), and ships as the proposal's coverage appendix. Built as a clean, zebra-striped `.xlsx`.

---

## 1. The artifact — 3 columns

| `[Client] Requirement` | `Acceler [Program] Module — Mapping` | `Module Topics` |
|---|---|---|
| The client's requirement, **numbered** as in their RFP | Which **Day(s) / module** cover it | The specific sub-topics, anchored to the client's use cases |

- **One row per requirement** (keep the client's numbering — 1, 2, 3 … even if your day-order differs).
- **Last rows:** the client's **flagship use case** → mapped to the **Capstone / Agentic Fest sample**, and a **Masterclasses** row listing advanced/gap-filling content.

---

## 2. How to build it (process)

1. **Extract the requirement list** verbatim from the client's RFP / "Requirement" slide. Number them exactly as they do.
2. **Map each → program day(s)/module(s).** Use the mapping notation (§3).
3. **List the topics covered**, in the program's language, **anchored to the client's domain use cases** in parentheses — e.g. `(Compliance & Policy Assistant)`, `(Automated Loan Approval, Fraud Investigation)`, `(KYC API scaffold, payment debug)`.
4. **Flag gaps honestly** (§4). Never paper over a gap — mark it, say what's missing, and route it.
5. **Add the flagship use-case row** → Capstone / Agentic Fest sample (e.g. `Symphony AI NLQ Use Case → Agentic Fest Sample 1 (NLQ Agent)`).
6. **Add the Masterclass row** — the advanced/standalone modules that deepen or fill requirements.
7. **Build the xlsx** (§5) and attach as the coverage appendix.

---

## 3. Mapping notation (column B)

- **Single day:** `Day 1 — AI Foundations & Vibe Coding`
- **Spans days:** `Day 2–3 — Orchestration Stack`
- **Introduced → reinforced:** `Day 3 → Day 4 — MCP & Protocols`
- **Day + Masterclass:** `Day 4 + Reliability Masterclass`
- **Partial / concept-only:** `Day 4 — concept`, `Day 2 — partial`, `Day 2/4 — partial + HITL Masterclass`
- Keep the module label human-readable (the theme, not just "Day 4").

---

## 4. Gap flagging (the credibility move)

Three honest states beyond full coverage:

| State | Marker | Meaning | Route |
|---|---|---|---|
| **GAP** | `⚠` on requirement + `GAP:` note | Not currently scoped | Masterclass, future phase, or "confirm scope" |
| **THIN** | `⚠` + `THIN:` note | Touched but shallow | Masterclass deep-dive |
| **partial** | `partial` in mapping | Covered in part | Note what's missing |

- Visually: gap rows get a **peach/pink background** (`FCEFEA`) and the requirement text turns **red** (`C0392B`); covered rows stay navy.
- Write the gap inline: e.g. `GAP: Voice (STT/TTS) not yet scoped`, `THIN: event-driven (Kafka/Event Grid), microservices-vs-monolith, Docker/K8s`, `GAP: hands-on tuning lab — confirm concept-only`.
- **Masterclasses are the primary gap-filler** — most advanced/thin requirements route to one of the 6 (Cost Engineering · Reliability/AI-SRE · AI Product Thinking · HITL & Trust · Experimentation & Lifecycle · Advanced Agentic AI).

---

## 5. openpyxl build pattern

```
Header row (navy #1B2A6B fill, white bold, wrap) — freeze_panes = "A2"
Body rows:
  bg = peach #FCEFEA if gap else (light #F2F4FA on even, white on odd)   # zebra
  col A (Requirement): bold; navy #1B2A6B normally, red #C0392B if gap
  col B (Mapping): 10.5pt, dark
  col C (Topics): 10.5pt #333333, wrap_text, vertical top
  thin borders #D5DAE8
Col widths: A 34 · B 34 · C 90    Row1 height 34
sheet_view.showGridLines = False
```

File naming: `[Client]_RFP_Coverage_Mapping.xlsx` · builder `build_mapping_xlsx.py`.

---

## 6. Writing style for the Topics column
- Dense but scannable: `topic; topic; topic` separated by semicolons.
- Use the program's real tool/technique names (ReAct, FAISS/Chroma, HNSW/SPLADE/RRF, LangGraph, MCP/A2A, LangSmith, OAuth/Managed Identity, SOX/GDPR).
- End relevant rows with the **use-case anchor** in parentheses so the client sees their world reflected.
- Show flow with arrows: `Retrieve→Augment→Generate`, `Planner→SQL-Gen→Validator→Reasoning`.

---

## 7. Edelweiss example (reference)
`Edelweiss_RFP_Coverage_Mapping.xlsx` — 17 numbered requirements + Symphony NLQ use case + 6 Masterclasses, mapped across the AI Builders Accelerator days. Gaps flagged: Conversational/Multimodal (Voice STT/TTS), Fine-Tuning (hands-on lab), Production Architecture (event-driven/microservices/K8s — thin), Data Engineering for AI (streaming ingestion, schema evolution, feature store). Each routed to a day + masterclass or "confirm scope." *(Note: that file pre-dates the 8-day restructure — re-map day numbers to the current 8-day curriculum when reusing.)*

---

## 8. Checklist
- [ ] Every client requirement present, **numbered as in their RFP**
- [ ] Each mapped to a real day/module (notation per §3)
- [ ] Topics in program language, **anchored to client use cases**
- [ ] Gaps flagged honestly (⚠ + GAP/THIN/partial) and **routed** (masterclass / scope confirm)
- [ ] Flagship use-case row → Capstone / Agentic Fest sample
- [ ] Masterclass row included
- [ ] xlsx styled (navy header, zebra, peach gaps, frozen header, no gridlines)
- [ ] Day numbers match the **current** curriculum version

---

*Built from: Edelweiss RFP Coverage Mapping (`build_mapping_xlsx.py`, Jun 2026). Pairs with [[pricing-skills]], [[doc-proposal-skills]], [[deck-skills]], [[project-edelweiss]].*
