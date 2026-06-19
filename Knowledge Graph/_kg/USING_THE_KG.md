# Using the Knowledge Graph for Pre-Sales Proposals

The knowledge graph turns ~1,072 historical files (every past proposal, deck, costing
sheet, curriculum and instructor record) into a queryable memory of *everything Acceler
has ever pitched*. For APR pre-sales, it is the **retrieval layer** that lets you build a
new proposal from precedent instead of from scratch — the difference between a 2–5 day
turnaround and a same-day one.

## What's in it
- **`graph.html`** — interactive map. Open in any browser (self-contained, no server).
- **`INDEX.md`** — one-page digest: every account's programs, tools and pricing bands.
- **`instructors.json`** — 773 instructors, deduped, tagged by topic, with LinkedIn.
- **`graph.json` / `files.json`** — the raw data (for agents/scripts).

Node types: **Accounts · Programs · Topics · Instructors · Tools · Doc types.**

## The proposal workflow — how to drive it

**1. Find the closest precedent.** Search the new client's *industry + program*
(e.g. a BFSI AI-Builders ask → look at Edelweiss, Nucleus, MCB). Click the account to
see exactly which files were sent, at what price, with which curriculum. Copy the
nearest-fit proposal as your skeleton rather than starting blank.

**2. Anchor the price.** Each account/program now shows clean **pricing bands**:
- **Rates** = per-learner / per-day unit prices ($55, $100, $130, ₹5,000…)
- **Deal size** = total contract values (only from real costing/proposal docs)
- **Margin** = the markup % used

Pull the rate other comparable accounts paid, then run it through the Pricing model
(India $55 / US $110 / special $350–450, 25–40% margin). The bands tell you the market-
accepted number so you don't over- or under-quote.

**3. Scope the curriculum.** Click the **Topic** nodes the client cares about
(e.g. *Agentic AI*, *RAG / Retrieval*, *Workplace Productivity*, *Automation / No-Code*)
to see every past file that covers them. Lift modules from the highest-rated precedent.
The taxonomy now mirrors what the standard decks actually teach.

**4. Staff the delivery.** From any Topic node you get the **instructors expert in it**,
ranked and linked. Filter by the client's domain (the TA/HR mis-tagging is fixed, so a
data scientist no longer shows up under HR). Shortlist 2–3 names per track with LinkedIn
ready for the client.

**5. Reuse the assets.** The account/program views list every deck, costing sheet and
curriculum doc with its file path — open directly to clone the format (and stay on-brand
with the Session-Deck-Builder + Doc/Deck/Pricing skills).

## Where it fits the APR "Mini-UT" vision
This graph is the **knowledge/memory layer** the proposal-automation agents query. A
"find precedent → pull pricing → assemble curriculum → staff instructors → draft deck"
agent pipeline reads `graph.json` / `files.json` instead of re-reading the whole drive
each time. Keeping the graph fresh (re-run the pipeline when new proposals land) is what
keeps the automated proposals grounded in real, winning precedent.

## Refreshing the graph
From this folder:
```
python3 build_corpus.py      # Pass 1 — only when new files are added (re-walks the drive)
python3 build_graph.py        # Pass 2 — classify + extract tools/topics/pricing
python3 parse_pool.py         # instructor sources → pool
python3 merge_instructors.py  # merge + topic classification + augment graph
python3 build_html.py         # render graph.html
```
Topic taxonomy lives in `build_graph.py` (`TOPICS`) and must stay in sync with `CANON`
in `merge_instructors.py`. Instructor topic guards (HR/TA, etc.) live in
`merge_instructors.py` (`classify_topics`, `HR_PROFESSION`).
