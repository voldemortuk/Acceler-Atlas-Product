# Acceler B2B Pre-Sales — Claude Code Plugin

Turns the full Acceler pre-sales workflow into one Claude Code plugin you install in any terminal (Warp, iTerm, Terminal.app, VS Code, JetBrains). Uses your existing Claude Max / Pro / API subscription — no separate API key needed.

## What it does

When a client requirement lands, the plugin orchestrates the full pipeline:

```
Requirement (notes / RFP)
   ↓
/acceler-presales:discovery   →  score against 33 questions
   ↓
/acceler-presales:similar     →  find closest precedents in the Knowledge Graph
   ↓
/acceler-presales:proposal      →  draft program document (IK-Acceler house style)
   ↓
/acceler-presales:proposal-deck →  pre-sales PITCH deck (KASE HTML · client-facing)
   ↓
/acceler-presales:session-deck  →  post-sales DELIVERY deck (live session · sister to PPTX)
   ↓
/acceler-presales:session-recap        →  post-delivery LEARNER recap (per session day)
/acceler-presales:session-recap-report →  post-delivery STAKEHOLDER report (per session day)
   ↓
/acceler-presales:pricing     →  bottom-up cost stack (INR India · USD US strict)
   ↓
/acceler-presales:instructors →  rank SMEs from the indexed pool (773 profiles)
```

Or run the whole pipeline at once: **`/acceler-presales:full-cycle`**.

> Slash commands are namespaced by the plugin: `/acceler-presales:<command>`.

## What's inside

- **Skills** (`skills/`) — every Acceler skill markdown, auto-loaded by Claude Code when relevant
  - `doc-proposal/` — IK-Acceler proposal house style v2
  - `pricing/` — bottom-up cost stack, INR/USD strict, first-time vs repeat
  - `requirement-mapping/` — 3-col coverage matrix with gap flagging
  - `proposal-deck/` — pre-sales pitch deck on the KASE engine (data-driven `SLIDE_DATA` slides · ~80 templates · engine + e& reference bundled)
  - `live-session-deck/` — post-sales live delivery deck (4-movement arc · 15 slide types)
  - `session-recap/` — post-delivery recap pair: learner-facing `dayN-learner-recap` + stakeholder-facing `dayN-recap-report`
  - `pptx-deck/` — HTML→PPTX image-fidelity converter for the proposal deck (`build_pptx.py` bundled · per-slide 2× PNG → 16:9 PPTX)
  - `mini-ut-context/` — Utkarsh's operating profile + Mini-UT principles
- **Commands** (`commands/`) — slash commands for each pipeline step
- **Knowledge** (`knowledge/`) — the Acceler Knowledge Graph
  - `graph.json` (2.6 MB) · `files.json` (761 KB) · `instr_candidates.json` (14 KB)
  - `INDEX.md` — one-page digest of all 61 clients with pricing bands
  - `USING_THE_KG.md` — how the agent should query the graph
- **Samples** (`samples/`) — reference proposals to lift patterns from

## Install (from the private GitHub marketplace)

This repo **is** the marketplace. You install and update the plugin straight from Git — no local download, no file copying.

### Pre-reqs
1. **Claude Code** installed (`brew install claude`, or from claude.com/code) and signed in (`claude /login`).
2. **Access to this private repo.** Authenticate once so Claude Code can clone it:
   ```bash
   gh auth login          # GitHub CLI — or have SSH keys set up
   ```
   Ask Utkarsh to add you as a repo collaborator first.

### A · First-time install (Git only)
```bash
claude
/plugin marketplace add voldemortuk/acceler-presales-plugin
/plugin install acceler-presales@acceler-local
```

### B · Already have it via the old local-file method? Migrate to Git
Do **not** uninstall or remove the old marketplace first (removing it would auto-uninstall the plugin). Re-adding under the same name silently swaps the source from your local folder to this repo:
```bash
claude
/plugin marketplace add voldemortuk/acceler-presales-plugin   # replaces the local 'acceler-local' source
/plugin marketplace update acceler-local                        # pull latest from Git
```
The plugin stays installed as `acceler-presales@acceler-local`, now sourced from GitHub.
*(Optional, to force a clean re-download: `/plugin uninstall acceler-presales@acceler-local` then `/plugin install acceler-presales@acceler-local`.)*

### Verify
```bash
/plugin list                # should show: acceler-presales (0.3.0)
/plugin marketplace list     # 'acceler-local' should point to voldemortuk/acceler-presales-plugin (not a local path)
```

## Updating

Whenever a new version is published:
```bash
/plugin marketplace update acceler-local
```
(Updates ship only when the maintainer bumps `version` in `.claude-plugin/plugin.json` — see [CONTRIBUTING.md](CONTRIBUTING.md).)

## Use it (in any terminal)

Open Claude Code in your terminal (Warp / iTerm / VS Code / etc):
```bash
claude
```

Then run any of:

```
/acceler-presales:full-cycle      Drive the entire pipeline end-to-end from meeting notes
/acceler-presales:discovery       Score a brief against the 33-question checklist
/acceler-presales:similar         Find the closest past Acceler precedents (KG-powered)
/acceler-presales:proposal        Draft the program document (IK-Acceler house style)
/acceler-presales:proposal-deck   Generate the pre-sales pitch deck (KASE HTML)
/acceler-presales:session-deck    Generate the post-sales live delivery deck (HTML)
/acceler-presales:session-recap        Generate the post-delivery learner recap (HTML)
/acceler-presales:session-recap-report Generate the post-delivery stakeholder report (HTML)
/acceler-presales:pricing         Compute the cost stack (INR India · USD US strict)
/acceler-presales:instructors     Rank SMEs from the indexed pool
```

Each command takes a brief / notes / topic as input. The orchestrator (`full-cycle`) chains them with appropriate handoffs and review gates.

## Refreshing the Knowledge Graph

The KG is built from the historical Drive folder. To refresh after new proposals land, then publish via this repo:

```bash
cd "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"
python3 build_corpus.py       # only when new files added
python3 build_graph.py         # classify + extract tools/topics/pricing
python3 merge_instructors.py   # merge + classify instructors
python3 build_html.py          # render graph.html
# copy the regenerated files into this repo's knowledge/ (the source of truth):
cp graph.json files.json instr_candidates.json INDEX.md USING_THE_KG.md \
   "$HOME/acceler-presales-plugin/knowledge/"
# then publish: bump version in .claude-plugin/plugin.json, commit & push
cd "$HOME/acceler-presales-plugin" && git add -A && git commit -m "KG refresh" && git push
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

*v0.3.0 · Jul 2026 · Utkarsh Raj · Acceler / Interview Kickstart B2B · [CHANGELOG](CHANGELOG.md) · [CONTRIBUTING](CONTRIBUTING.md)*
