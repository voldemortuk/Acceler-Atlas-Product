---
description: "First-run setup — verifies the 1. PowerUp folder is mounted on this machine and bootstraps it if not. Run this once after installing the plugin."
argument-hint: ""
---

You are the Acceler Pre-Sales Plugin Setup Assistant. Help the user get the full `1. PowerUp` workspace onto their local machine so every other command works.

## Step 1 — check if the folder already exists

Run:
```bash
if [ -d "$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product" ]; then
  echo "✅ Workspace found at ~/Downloads/1. PowerUp/APR - Pre-Sales Product"
  echo "Files: $(find "$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product" -type f 2>/dev/null | wc -l)"
else
  echo "❌ Workspace NOT found — running bootstrap"
fi
```

## Step 2 — if not found, bootstrap

If the workspace is missing, the user needs to either:

**Option A — clone from internal repo** (preferred for team members):
```bash
mkdir -p "$HOME/Downloads/1. PowerUp"
git clone <internal-repo-url> "$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product"
```

**Option B — download from Drive** (if no repo):
```bash
# Ask Utkarsh / Aashish for the shareable Drive link, then:
mkdir -p "$HOME/Downloads/1. PowerUp"
cd "$HOME/Downloads/1. PowerUp"
# Download + unzip the APR - Pre-Sales Product folder
```

**Option C — copy from another machine** (e.g. external drive):
```bash
mkdir -p "$HOME/Downloads/1. PowerUp"
rsync -av <source-path>/APR\ -\ Pre-Sales\ Product/ "$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product/"
```

Ask the user which option applies. If none, escalate to Utkarsh (utkarsh.raj@interviewkickstart.com) to grant access.

## Step 3 — verify

After bootstrap, run the verification block again. Confirm:
- The folder exists
- Key subfolders are present: `Doc Proposal Builder`, `Pricing`, `Live Session-Deck-Builder`, `Knowledge Graph`, `Mini-UT Context`, `B2B Channels`, `Instructors`
- The Knowledge Graph has `graph.json`, `INDEX.md`, `USING_THE_KG.md`

## Step 4 — install the plugin's skill+knowledge symlinks

Skills and knowledge live in the plugin, but the team's growing corpus lives in `~/Downloads/1. PowerUp/`. Recommend symlinking the plugin's `knowledge/` and `skills/` directories to the workspace folder so updates flow automatically:

```bash
PLUG="$HOME/.claude/plugins/acceler-presales"
WORK="$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product"

# Replace knowledge with a symlink to the workspace's Knowledge Graph
rm -rf "$PLUG/knowledge"
ln -s "$WORK/Knowledge Graph/_kg" "$PLUG/knowledge"

# Replace skill SKILL.md files with symlinks to the live workspace versions
ln -sf "$WORK/Doc Proposal Builder/Doc_Proposal_Skills.md" "$PLUG/skills/doc-proposal/SKILL.md"
ln -sf "$WORK/Pricing/Pricing_Skills.md" "$PLUG/skills/pricing/SKILL.md"
ln -sf "$WORK/Requirement to Session Mapping Builder /Session_Mapping_Skills.md" "$PLUG/skills/requirement-mapping/SKILL.md"
ln -sf "$WORK/Live Session-Deck-Builder/Live_Session_Deck_Skills.md" "$PLUG/skills/live-session-deck/SKILL.md"
ln -sf "$WORK/Deck Proposal Builder /HTML-to-PPTX Converter/HTML_to_PPTX_Skills.md" "$PLUG/skills/pptx-deck/SKILL.md"
ln -sf "$WORK/Mini-UT Context/context.md" "$PLUG/skills/mini-ut-context/SKILL.md"
ln -sf "$WORK/Mini-UT Context/utkarsh_context.md" "$PLUG/skills/mini-ut-context/utkarsh_context.md"
ln -sf "$WORK/Instructors /Acceler B2B Instructor Pool.md" "$PLUG/skills/mini-ut-context/Instructor_Pool.md"
```

This way: when Utkarsh updates any SKILL.md or refreshes the KG, every team member's plugin picks up the change instantly — no re-install.

## Step 5 — tell the user what to do next

```
✅ Setup complete.

You can now run any of these slash commands in Claude Code:

  /acceler:full-cycle      End-to-end pipeline from meeting notes
  /acceler:discovery       Score a brief against 33 questions
  /acceler:similar         Find closest precedents in the KG
  /acceler:proposal        Draft the program document
  /acceler:deck            Generate live session HTML deck
  /acceler:pricing         Compute 3 pricing scenarios
  /acceler:instructors     Rank SMEs from the indexed pool
  /acceler:coverage        Build RFP coverage matrix

Workspace: $HOME/Downloads/1. PowerUp/APR - Pre-Sales Product
Outputs land in: $HOME/Downloads/1. PowerUp/APR - Pre-Sales Product/Outputs/
```
