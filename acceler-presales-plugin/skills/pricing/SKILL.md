---
name: pricing-skills-acceler-proposal-pricing-costing
description: "How to price & cost Acceler/PowerUp B2B training proposals — the bottom-up cost stack (Curriculum + Instructor[Prep&Review+Dry Run+Live] + TA + Infra[VMs+Tools]) → Overheads → Margin → Pricing, the instructor rate card (India $55 / US $110 / special $350-450), first-time-vs-repeat optimization, VM (₹500/learner/day) & tool costing, Elevate volume discounts, India T&C, and Nucleus + Edelweiss worked examples. Companion to [[doc-proposal-skills]] and [[deck-skills]]."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6d83a6a7-37dc-44fa-b73c-61e1418d2a82
---

# Acceler Proposal Pricing & Costing — SKILL.md  (v1)

The price a client sees is built **bottom-up**: Cost stack → Overheads → Margin → Pricing. Tool/VM costs are a **separate provisioning layer** (often excluded from the fee, provisioned by client). Always model in a spreadsheet; quote **INR for India, USD for US**.

---

## 1. The cost stack (build bottom-up, in order)

```
Curriculum
+ Instructor  = Prep & Review  +  SME Training (Dry Run)  +  Live Delivery
+ TA Support  = Assignment Review  +  Live Assistance
+ Infra       = VMs (Nuvepro)  +  AI Tools
= BASE COST
+ Overheads
= TOTAL COST
+ Margin
= PRICING   (then round)
```

Then derive **Per-learner** = Pricing ÷ batch size, and **Per-pax-per-day** for comparison.

---

## 2. Component formulas

**① Curriculum** (content development)
- Theoretical: **New = $263 / class-hour** · **Existing = $113 / class-hour**. (A new 6-hr module ≈ 21 curriculum-dev hrs; 12 class-hrs × $263 ≈ $3,150.)
- **In practice = ₹0 / $0.** Acceler now builds **most content internally** (all tech/engineering, most non-tech, and ~all leadership), with light SME review only. Both Nucleus and Edelweiss = ₹0 curriculum.
- Add **+20–30%** only for a **very niche** program.

**② Instructor** — three parts, each = hours × instructor hourly rate:
- **Live Delivery** = **live hours × rate**.
- **SME Training (Dry Run)** = **live hours × rate** (one internal pass). **= $0 if the SME has delivered this before** (e.g. Edelweiss). Use a **partial** dry run for a refresher (Edelweiss 8-day used 12 hrs, not the full 54).
- **Prep & Review** = **live hours × 2 × rate** for a **first-time / never-delivered SME**. **Reduce toward 1×** when reusing the same SME / repeat delivery. (Nucleus first-time prep = 2×24×$55; repeat = 1×24×$55.)

**③ TA Support**
- **Assignment Review** *(OPTIONAL)* = **₹500 × number of assignments × number of learners** (≈ 1 assignment per session). **This line is optional — keep it for proper sanity, but we usually release the solution rather than grade. Drop it (or set assignments = 0) when the cohort won't have graded assignments.**
- **Live Assistance** = **₹1,000 / hour × live hours** (TA present throughout).

**④ Infra (VMs + Tools)** — **always one combined "Infra — VMs + Tools" line** in the sheet (don't drop Tools). Sometimes the **client provisions this** (then $0 in the fee).
- **VMs (Nuvepro)** = **₹500 / learner / VM-day** × learners × **VM-days**. Raw Nuvepro ≈ ₹350/day/learner + ₹8,000 one-time VM build + SME accounts.
  - **VM-days ≠ program-days.** VMs must stay up across the gaps between sessions: ~1 day before Day 1, ~2–3 days between sessions (sessions run ~2–3/week), and ~1 day after. **Rule of thumb: VM-days = program-days + 3–4 buffer days** (e.g. 5-day program → ~8–9 VM-days). This is *not* "double the duration" — it tracks the real calendar spread. Call the buffer out to the user; a longer always-on window is their call.
- **AI Tools** = per the **tool-costing sheet** (§5), **bundled into the Infra line**. Optimize with free versions first. Template fallback ≈ **$80–100/learner** (4–5 tools × ~$20/account); ~$20/learner for an incidental single-tool window. **Client-provisioned tools (e.g. Claude Code seats the client buys) are excluded** — note them separately, don't fold into the fee.

**⑤ Overheads** — Edelweiss model loads **~100%** (TOTAL COST = 2 × BASE). *(Confirm overhead % per deal; the B2B template uses a lower load.)*

**⑥ Margin** — **25–40%** markup on Total Cost. **Edelweiss used 40%**; the generic B2B template used 25%.

**⑦ Pricing** = Total Cost × (1 + margin), then **rounded** to a clean number.

---

## 3. Instructor rate card

| Line | India | US | Special (leadership / niche / non-tech) |
|---|---|---|---|
| **Live Class Delivery** | **$55/hr** ($50–55) | **$110/hr** ($100–110) | **$350–450/hr** |
| **Prep & Review** | **$75–80/hr** | **$100/hr** | per program |
| **Curriculum (per class-hr)** | New **$263** · Existing **$113** | same | +20–30% if niche |

- **Edelweiss applied a blended ₹5,225/hr (~$62)** for Prep, Dry Run and Live alike (single India rate).
- **TA:** ₹500 / assignment / learner · ₹1,000 / live-hour.
- **VM:** ₹500 / learner / VM-day (see §2④ for the VM-days window rule).
- FX: **ALWAYS pull the live USD→INR rate online before quoting — never hardcode.** ≈ **₹94.5/$** as of Jun 2026 (Investing.com 94.49 / Wise 94.39). The ₹84 in the worked examples below is historical; do not reuse it for new quotes. Internal conversion only — never quoted to the client.

### Live-hours calc
Live hours = **(program days × in-session hrs/day) + technical-coaching hours**.
*Edelweiss 8-day = 48 in-session (8×6) + 6 coaching = **54 live hrs**. 5-day version = 60 live hrs.*

---

## 4. First-time vs repeat delivery (the big optimizer)

| | First-time (new SME/course) | Repeat (same SME) |
|---|---|---|
| Curriculum | New rate (or $0 if internal) | **$0** |
| SME Dry Run | Full (live hrs × rate) | **$0** (or partial refresher) |
| Prep & Review | **2× live hrs** | **~1× live hrs** |
| Live Delivery | live hrs × rate | live hrs × rate |

*Nucleus: First-time ₹520,320 → Repeat (same instructor) **₹272,160** (~half).*
*Edelweiss is treated as repeat-capable (SMEs delivered before) → reduced dry run + prep.*

---

## 5. Tool & VM provisioning layer (separate from the fee)

- Classify every tool **PAID vs FREE**; scope to what's actually used; build an **editable xlsx** (`build_costing.py`) with yellow assumption cells → Low/Expected/High → USD + INR.
- **PAID:** OpenAI/Anthropic APIs (usage), GitHub Copilot ($19/seat/mo), Tabnine, CodeWhisperer, LangSmith (paid tier), Azure/AWS (usage), Docker Business, Pinecone, Cursor.
- **FREE / $0:** LangChain·LangGraph·CrewAI·AutoGen·MCP/A2A·FAISS·Chroma·SPLADE·HNSW·RRF·Hugging Face (local models)·LoRA/QLoRA/PEFT·Python·FastAPI·Streamlit·Gradio·VS Code.
- **Rules of thumb:** LLM API is the dominant variable ($/participant/day; ~$0 with local HF models). Per-seat coding tools = one short window. **Cloud is per-team, not per-learner**, serverless/auto-pause, ~$0 net with free credits. Always include an **on-prem / open-model ~$0 scenario**.
- **VM-days window:** cost VMs over **program-days + 3–4 buffer days**, not just in-session days — the environment stays up across the gaps between sessions (1 before, 2–3 between, 1 after; sessions run ~2–3/week). Surface the buffer to the user as their call.
- **Bundle Tools into the Infra line** with VMs (one "Infra — VMs + Tools" row). Client-provisioned tools (seats the client buys, e.g. Claude Code) are excluded from the fee and noted separately.
- **Edelweiss tool costing (cohort 20):** Copilot $380 + LLM API $1,400 + Azure $75 ≈ **$1,855 (~₹1.56 L)**; on-prem/open-model → ~$380. File `Edelweiss_Tool_Costing_Sheet.xlsx`.
- **Template fallback (per-learner):** Tools ~₹15,744 + VM ~₹7,000 = **₹22,744/learner** (pre-optimization; e.g. 14 learners = ₹318,416). Optimize tools down with free versions.

---

## 6. Volume discounts — "Acceler Elevate" package

| Batches | Discount |
|---|---|
| 2 | 7.5% |
| 4 | 12.5% |
| 6 | 17.5% |
| 8 | 22.5% |
| 10 | 27.5% |

Applied to bundled pricing (Accelerator batches + Masterclass groups). Post-discount price drives per-pax economics.

---

## 7. Worked examples

**Nucleus (24 live hrs · India $55 · 20 learners, without markup):**
| | First-time | Repeat (same instructor) |
|---|---|---|
| Prep & Review | ₹248,160 (2×24×$55) | ₹124,080 (1×) |
| SME Dry Run | ₹124,080 (24×$55) | ₹0 |
| Live Delivery | ₹124,080 (24×$55) | ₹124,080 |
| TA Support | ₹24,000 (24×₹1,000) | ₹24,000 |
| Curriculum / Infra | ₹0 / ₹0 | ₹0 / ₹0 |
| **Total (no markup)** | **₹520,320** (₹26,016/learner) | **₹272,160** (₹13,608/learner) |

**Edelweiss AI Builders Accelerator (8 Days · 54 live hrs · ₹5,225/hr blended):**
- Prep & Review 48×5,225 = 250,800 · Dry Run 12×5,225 = 62,700 · Live 54×5,225 = 282,150 → **Base 595,650**
- Overheads 595,650 → **Total Cost 1,191,300** · Margin 40% = 476,520 → **Pricing 1,667,820 → rounded ₹18,20,000**
- @ 12 pax = **₹151,667/pax** (₹18,958/pax/day) · rate/day ₹227,500
- (5-day version → **₹11,75,000**; ₹235,000/day; ₹97,917/pax @12)
- Tools + VM (provisioning, separate): ₹22,744/learner × 14 = ₹318,416 (optimize per §5)

**Masterclasses (7-group):** 3 hrs each; single MC build ≈ Total ₹66,000 → +overhead → Margin 40% → **Pricing ₹184,800**.

---

## 8. Standard Terms & Conditions (India)

Rates in **INR**, India deliveries only, exclusive of taxes · **Tool costs excluded** (client provisions) · participation **non-transferable** · pricing per agreed modules/sessions/hours · **min 15 / max 20 learners, full-batch pricing** · scope = agreed sessions/mentoring/evals/support (extras chargeable) · capstone **one reattempt/learner** · **cancellation within 15 days = full batch cost** · **one design included** (extra designs chargeable) · excludes travel/lodging/ancillary.

---

## 9. Costing-sheet build pattern (openpyxl)
**The pricing deliverable is always an Excel workbook (.xlsx), not a markdown file** — build it with openpyxl, save under `…/Outputs/[Client]_pricing_v0.1.xlsx`, and keep it **formula-driven off the yellow assumption cells** so the user re-prices by editing one cell. A markdown summary is only a companion shown in chat. Palette: NAVY `1B2A6B` headers · CYAN `27B4E6` sub-heads · ORANGE `F86B3C` total band · YELLOW `FFF6D6` editable cells · GREEN `0A4F2F` free band. Layout: Title → Assumptions (yellow) → cost-stack line items (formula-driven) → Base/Overhead/Margin/Pricing → per-learner & per-pax-per-day → Tool/VM provisioning block → Notes. `showGridLines=False`.

---

## 10. Pricing checklist
- [ ] Cost built bottom-up: Curriculum + Instructor(Prep×2/Dry/Live) + TA + Infra
- [ ] Curriculum $0 if internal (+20–30% only if niche)
- [ ] First-time vs repeat applied (kill dry-run & halve prep on repeat)
- [ ] Correct rate (India $55 / US $110 / special $350–450); live-hours include coaching
- [ ] **FX pulled live** (do not hardcode ₹84; ≈ ₹94.5 Jun 2026) — internal only
- [ ] TA Assignment Review treated as **optional** (drop if not grading); TA Live = ₹1,000/live-hr
- [ ] **Infra = VMs + Tools** in one line · VM-days = program-days + 3–4 buffer (call out to user) · client-provisioned seats excluded
- [ ] Overheads + Margin (25–40%) applied; Pricing rounded
- [ ] Per-learner & per-pax-per-day derived
- [ ] Tool/VM provisioning costed separately (optimize free; on-prem scenario)
- [ ] Volume discount (Elevate) if multi-batch bundle
- [ ] India T&C attached

---

*Built from: Nucleus AI Builder pricing + Edelweiss AI Builders Accelerator (5/8-day) pricing & tool costing + Acceler B2B Overall Costing Template (Jun 2026). Pairs with [[doc-proposal-skills]], [[deck-skills]], [[project-edelweiss]].*
