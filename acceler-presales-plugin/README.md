# Acceler B2B Pre-Sales — Claude Code Plugin

Turns the full Acceler pre-sales workflow into one Claude Code plugin you install in any terminal (Warp, iTerm, Terminal.app, VS Code, JetBrains). Uses your existing Claude Max / Pro / API subscription — no separate API key needed.

## What it does

When a client requirement lands, the plugin orchestrates the full pipeline:

```
Requirement (notes / RFP)
   ↓
/acceler:discovery   →  score against 33 questions
   ↓
/acceler:similar     →  find closest precedents in the Knowledge Graph
   ↓
/acceler:proposal    →  draft program document (IK-Acceler house style)
   ↓
/acceler:deck        →  generate live session deck (HTML, sister to PPTX)
   ↓
/acceler:pricing     →  bottom-up cost stack (INR India · USD US strict)
   ↓
/acceler:instructors →  rank SMEs from the indexed pool (773 profiles)
```

Or run the whole pipeline at once: **`/acceler:full-cycle`**.

## What's inside

- **Skills** (`skills/`) — every Acceler skill markdown, auto-loaded by Claude Code when relevant
  - `doc-proposal/` — IK-Acceler proposal house style v2
  - `pricing/` — bottom-up cost stack, INR/USD strict, first-time vs repeat
  - `requirement-mapping/` — 3-col coverage matrix with gap flagging
  - `live-session-deck/` — HTML deck builder (4-movement arc · 15 slide types)
  - `pptx-deck/` — match-a-reference PPTX rebuild pattern
  - `mini-ut-context/` — Utkarsh's operating profile + Mini-UT principles
- **Commands** (`commands/`) — slash commands for each pipeline step
- **Knowledge** (`knowledge/`) — the Acceler Knowledge Graph
  - `graph.json` (2.6 MB) · `files.json` (761 KB) · `instr_candidates.json` (14 KB)
  - `INDEX.md` — one-page digest of all 61 clients with pricing bands
  - `USING_THE_KG.md` — how the agent should query the graph
- **Samples** (`samples/`) — reference proposals to lift patterns from

## Install (60 seconds)

### Pre-req
You need **Claude Code** installed. If you don't have it:
```bash
brew install claude    # macOS via Homebrew
# or download from claude.com/code
```

Then sign in:
```bash
claude /login
```

### Install the plugin

**Option A — install from this folder directly (fastest):**
```bash
cp -r "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/acceler-presales-plugin" "$HOME/.claude/plugins/acceler-presales"
```

**Option B — install via Claude Code slash:**
```bash
claude
/plugin install /Users/voldemort/Downloads/1.\ PowerUp/APR\ -\ Pre-Sales\ Product/acceler-presales-plugin
```

**Option C — install via Warp:**
1. Open Warp terminal
2. Run `claude` to start a Claude Code session
3. Run `/plugin install <path>` with the plugin folder path

Verify install:
```bash
claude
/plugin list
# you should see: acceler-presales (0.1.0)
```

## Use it (in any terminal)

Open Claude Code in your terminal (Warp / iTerm / VS Code / etc):
```bash
claude
```

Then run any of:

```
/acceler:full-cycle      Drive the entire pipeline end-to-end from meeting notes
/acceler:discovery       Score a brief against the 33-question checklist
/acceler:similar         Find the closest past Acceler precedents (KG-powered)
/acceler:proposal        Draft the program document (IK-Acceler house style)
/acceler:deck            Generate the live session HTML deck
/acceler:pricing         Compute the cost stack (INR India · USD US strict)
/acceler:instructors     Rank SMEs from the indexed pool
```

Each command takes a brief / notes / topic as input. The orchestrator (`full-cycle`) chains them with appropriate handoffs and review gates.

## Refreshing the Knowledge Graph

The KG is built from the historical Drive folder. To refresh after new proposals land:

```bash
cd "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"
python3 build_corpus.py       # only when new files added
python3 build_graph.py         # classify + extract tools/topics/pricing
python3 merge_instructors.py   # merge + classify instructors
python3 build_html.py          # render graph.html
# then copy the regenerated files into the plugin:
cp graph.json files.json instr_candidates.json INDEX.md USING_THE_KG.md \
   "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/acceler-presales-plugin/knowledge/"
```

## Architecture notes

- **No backend.** Everything runs in your Claude Code session. The plugin's skills + commands give Claude the instructions; the KG gives it precedent data.
- **No API key juggling.** Uses whatever Claude Code is authenticated against (Claude Max / Pro / API).
- **Top-tier models.** Opus 4.x via Claude Code by default — 200K-1M context, best instruction following.
- **Reusable.** Anyone with Claude Code installed can install this plugin and get the same pre-sales workflow.

## Companion tools

- **Acceler OS** (`acceler-os.html`) — the visual workspace that runs the same logic in a browser (Cowork artifact)
- **KT Deck** (`acceler-presales-kt.html`) — the handover document for someone taking over the role
- **Discovery Checklist** (`Acceler-PreSales-Discovery-Checklist.html`) — standalone 33-question scorer

---

*v0.1.0 · Jun 2026 · Utkarsh Raj · Acceler / Interview Kickstart B2B*
