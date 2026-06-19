# Acceler B2B Pre-Sales — Product Workspace

The Acceler / Interview Kickstart B2B Pre-Sales workspace. Everything the team needs to take a client requirement from inbox to signed proposal — skills, knowledge graph, sample proposals, instructor pool, agent pipeline, and the workspace UI.

```
APR — Pre-Sales Product/
├── acceler-os.html                       ← Workspace UI (Cowork artifact + standalone)
├── acceler-presales-kt.html              ← Knowledge Transfer deck for new role-holders
├── Acceler-PreSales-Discovery-Checklist.html  ← 33-question discovery scorer
│
├── acceler-presales-plugin/              ← Claude Code plugin (install on any laptop)
│   ├── README.md
│   ├── setup.sh
│   ├── .claude-plugin/plugin.json
│   ├── commands/                         ← /acceler:full-cycle · :discovery · :similar · :proposal · :deck · :pricing · :instructors · :coverage · :setup
│   ├── skills/                           ← every SKILL.md (auto-loaded by Claude Code)
│   ├── knowledge/                        ← Knowledge Graph (graph.json, INDEX.md, …)
│   └── samples/                          ← 3 reference proposals
│
├── Doc Proposal Builder/                  ← Doc_Proposal_Skills.md + samples
├── Pricing/                               ← Pricing_Skills.md (cost stack, INR/USD)
├── Requirement to Session Mapping Builder/ ← Session_Mapping_Skills.md
├── Live Session-Deck-Builder/             ← Live_Session_Deck_Skills.md (HTML deck format)
├── Deck Proposal Builder/                 ← HTML_Deck_Skills + HTML-to-PPTX
├── Knowledge Graph/                       ← graph.json · INDEX.md · USING_THE_KG.md · build pipeline (Python)
├── Mini-UT Context/                       ← context.md · utkarsh_context.md · WhatsApp text exports
├── B2B Channels/                          ← Team-chat archives (Slack/group summaries)
├── Instructors/                           ← Instructor Pool (acceler-tagged) + Documents/
├── Sample Proposals/                      ← Nucleus · Booking · Gryphon · MCB reference docx
└── Acceler B2B KT/                        ← KT presentation deck for hand-over
```

---

## Install on a new laptop (5 minutes)

```bash
# 1. Install Claude Code + GitHub CLI + Git LFS
brew install --cask claude-code
brew install gh git-lfs
git lfs install
gh auth login
claude /login

# 2. Clone this repo to the exact path the plugin expects
mkdir -p ~/Downloads/"1. PowerUp"
gh repo clone voldemortuk/APR-Presales-Product ~/Downloads/"1. PowerUp/APR - Pre-Sales Product"

# 3. Bootstrap the plugin (symlinks skills + KG to the live workspace)
bash ~/Downloads/"1. PowerUp/APR - Pre-Sales Product/acceler-presales-plugin/setup.sh"

# 4. Use it from any terminal — Warp / iTerm / Terminal / VS Code / JetBrains
claude
/acceler:full-cycle
```

That's it. Uses your existing Claude account (Max / Pro / API). No separate API key.

---

## What the plugin does

When a client requirement lands, run `/acceler:full-cycle` and paste the meeting notes. The orchestrator walks the whole pipeline:

| Stage | Slash command | What it does |
|---|---|---|
| 1 | `/acceler:discovery`    | Score against 33 questions → strength % + gaps |
| 2 | `/acceler:similar`      | Find closest precedents in the Knowledge Graph (61 clients · 1,072 files) |
| 3 | `/acceler:proposal`     | Draft the program document (IK-Acceler house style v2) |
| 4 | `/acceler:deck`         | Generate the live session HTML deck (4-movement arc) |
| 5 | `/acceler:pricing`      | 3-scenario cost stack — First / Repeat / Elevate volume (INR India · USD US strict) |
| 6 | `/acceler:instructors`  | Rank SMEs from the indexed pool (746 profiles · LinkedIn URLs) |
| 7 | `/acceler:coverage`     | Build RFP-to-module coverage matrix with honest gap flagging |

Each stage has a review gate — approve / edit / regenerate before continuing.

Outputs land in `~/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/`.

---

## The two UIs

**Acceler OS** (`acceler-os.html`) — workspace UI. Opens in Cowork sidebar OR any browser.
- Dashboard with KG stats (clients, files, instructors, tools, topics)
- New Proposal flow with strength scoring + closest-precedents card
- Live editable Pricing spreadsheet with observed bands from comparable deals
- Coverage Map builder
- KG-driven Instructors lookup with LinkedIn URLs
- Knowledge tab: 6 views — Clients · Programmes · Topics · Tools · Instructors · Interactive Graph

**KT Deck** (`acceler-presales-kt.html`) — handover slide deck for whoever takes over the role. 33 slides covering mental model, workflow, decisions, pricing, accounts, transition plan.

---

## Refreshing the Knowledge Graph

When new proposals land, refresh the graph so the agent's precedent lookup stays current:

```bash
cd ~/Downloads/"1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"
python3 build_corpus.py       # only when new files added
python3 build_graph.py
python3 merge_instructors.py
python3 build_html.py
# then re-copy outputs into the plugin
```

---

## Security & access

- **This repo is private.** It contains client proposal details, internal chat archives, and instructor profile data. Never make it public.
- **Access:** restricted to the Acceler B2B team (Utkarsh / Karthika / Soham / Aashish / Amit / Anshuman + designated NP Team members).
- **Sensitive content:** WhatsApp media (`.opus` audio, photos, videos) is `.gitignore`d — only the `_chat.txt` text exports are tracked.

---

*v1.0 · Jun 2026 · Acceler / Interview Kickstart B2B Pre-Sales · Maintained by Utkarsh Raj*
