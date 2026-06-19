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
- FX ≈ ₹84 / $ (for internal conversion only — never quoted to client).

## Output (markdown)

```
# [Client] · Pricing — [Geography] · [LiveHrs] live hrs · [Batch] learners

**Currency:** [INR (₹) / USD ($)]  ·  **Margin:** [%]  ·  **Overhead:** [%]  ·  **FX:** ₹84/$ (internal)

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
| TA — Assignment Review | ₹500 × assignments × batch | … |
| TA — Live Assistance | ₹1,000 × live | … |
| Infra — VMs | ₹500 × batch × days (or 0 if client provisions) | … |
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

Save to:
```
~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/[Client]_pricing_v0.1.md
```

Offer to export as XLSX (using openpyxl) or as a CSV the user can drop into Google Sheets.
