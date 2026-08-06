---
description: "Compute Acceler proposal pricing — bottom-up cost stack, 3 scenarios (first / repeat / Elevate volume). INR for India · USD for US (strict)."
argument-hint: "<inputs: client, geography, days, hrs/day, batch, tier, curriculum, overhead%, margin%, elevate%>"
---

Compute pricing using the Acceler bottom-up cost stack.

## Input
```
$ARGUMENTS
```

If inputs are missing, ask for the key ones (geography · days × hrs/day · batch · tier · curriculum state · SME state · overhead% · margin%).

## How to compute

1. Read `skills/pricing/SKILL.md` for the full cost stack, rate card, first-time vs repeat rules, and India T&C.
2. Compute the cost stack:
   ```
   Curriculum + Instructor(Prep + DryRun + Live) + TA(Assign + Live) + Infra(VMs + Tools)
   = BASE
   + Overheads (× overhead%)
   = TOTAL COST
   + Margin (× margin%)
   = PRICING (round to nearest thousand)
   ```
3. Surface observed pricing bands from `knowledge/INDEX.md` for comparable deals (same geography × programme × scale).

## Currency rule (STRICT)

- **India clients = INR (₹) only.** Never USD. Never mix.
- **US / Middle East / Other = USD ($) only.** Never INR.
- **FX: ALWAYS pull the live USD→INR rate online before quoting — never hardcode.** ≈ ₹94.5/$ as of Jun 2026 (re-check; ₹84 is stale). Internal conversion only — never quoted to client.

## Output — primary deliverable is an Excel sheet (.xlsx)

**Always produce an Excel workbook as the deliverable, not a markdown file.** Build it with `openpyxl` following the costing-sheet pattern in `skills/pricing/SKILL.md` §9 (NAVY headers · CYAN sub-heads · ORANGE total band · **YELLOW editable assumption cells** · GREEN free/provisioning band · `showGridLines=False`). The sheet must be **formula-driven** off the yellow assumption cells (batch, live hrs, rates, FX, VM-days/buffer, tools, assignment count, overhead %, margin %) so the user can re-price by editing one cell. Scenario A / A′ (alt batch) / B (repeat) / C (Elevate, if any) each get their own block; end with per-learner & per-pax-per-day, a Tool/VM provisioning block, and a Notes block.

Then show the same numbers inline in chat as a quick markdown summary (the structure below) so the user sees the result without opening the file — but the **file you save is the .xlsx**.

```
# [Client] · Pricing — [Geography] · [LiveHrs] live hrs · [Batch] learners

**Currency:** [INR (₹) / USD ($)]  ·  **Margin:** [%]  ·  **Overhead:** [%]  ·  **FX:** ₹[live rate]/$ (internal, live-checked [date])

## Observed bands from comparable deals (KG anchor)
- [Client X] · [programme] · [pricing band]
- [Client Y] · [programme] · [pricing band]

## Scenario A — First Delivery
| Line item | Calculation | Amount |
|---|---|---|
| Curriculum | … | … |
| Instructor — Prep & Review | 2 × live × rate | … |
| Instructor — SME Dry Run | live × rate | … |
| Instructor — Live Delivery | live × rate | … |
| TA — Assignment Review *(optional — drop if not grading)* | ₹500 × assignments × batch | … |
| TA — Live Assistance | ₹1,000 × live | … |
| Infra — VMs + Tools | (₹500 × batch × VM-days) + tools; VM-days = days + 3–4 buffer (or 0 if client provisions) | … |
| **BASE COST** |  | **…** |
| Overheads (X%) |  | … |
| **TOTAL COST** |  | **…** |
| Margin (Y%) |  | … |
| **PRICING (rounded)** |  | **…** |
| Per-learner | Pricing ÷ batch | … |
| Per-pax-per-day |  | … |

## Scenario B — Repeat Delivery (same SME)
[Same table; Prep halved, Dry Run = 0, Curriculum = 0]

## Scenario C — Elevate / Volume (only if discount > 0%)
[Apply discount; show post-discount per-pax]

## India T&C (attach if India)
Rates in INR · India only · taxes excluded · tools excluded (client provisions) · 15-20 learners full-batch · cancellation within 15 days = full cost · one design included.

## Notes & assumptions
- [Rate, why; curriculum state; first-time vs repeat reasoning; KG-anchored sanity check]
```

Save the **Excel workbook** (primary deliverable) to:
```
~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/[Client]_pricing_v0.1.xlsx
```

Optionally also drop a markdown companion (`[Client]_pricing_v0.1.md`) alongside it if the user wants a readable text version — but the xlsx is the default output. Offer a CSV export only if the user asks for Google Sheets.
