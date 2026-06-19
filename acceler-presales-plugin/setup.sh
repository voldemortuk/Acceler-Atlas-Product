#!/usr/bin/env bash
# Acceler Pre-Sales Plugin — first-run setup
# Verifies workspace, symlinks live skills/knowledge from the workspace to the plugin.
# Usage: bash setup.sh  [--repo <git-url> | --rsync <source-path>]

set -e

WORK="$HOME/Downloads/1. PowerUp/APR - Pre-Sales Product"
PLUG="$HOME/.claude/plugins/acceler-presales"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Acceler Pre-Sales Plugin — Setup${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Parse args
REPO=""; RSYNC_SRC=""
while [ $# -gt 0 ]; do
  case $1 in
    --repo)  REPO="$2"; shift 2;;
    --rsync) RSYNC_SRC="$2"; shift 2;;
    *) shift;;
  esac
done

# Step 1 — workspace check
if [ -d "$WORK" ]; then
  FILES=$(find "$WORK" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo -e "${GREEN}✅ Workspace found:${NC} $WORK"
  echo -e "   $FILES files indexed"
else
  echo -e "${RED}❌ Workspace NOT found at:${NC} $WORK"
  if [ -n "$REPO" ]; then
    echo -e "${YELLOW}→ Cloning from $REPO${NC}"
    mkdir -p "$HOME/Downloads/1. PowerUp"
    git clone "$REPO" "$WORK"
  elif [ -n "$RSYNC_SRC" ]; then
    echo -e "${YELLOW}→ Syncing from $RSYNC_SRC${NC}"
    mkdir -p "$HOME/Downloads/1. PowerUp"
    rsync -av "$RSYNC_SRC/" "$WORK/"
  else
    echo ""
    echo -e "${YELLOW}You need to get the workspace folder onto this machine first.${NC}"
    echo "  Option A:  bash setup.sh --repo <git-url>"
    echo "  Option B:  bash setup.sh --rsync <source-path>"
    echo "  Option C:  Download manually from Drive (ask Utkarsh for the link)"
    echo "             and place at: $WORK"
    echo ""
    echo "  Then re-run: bash setup.sh"
    exit 1
  fi
fi

# Step 2 — verify key subfolders
echo ""
echo -e "${CYAN}Verifying workspace structure...${NC}"
for d in "Doc Proposal Builder" "Pricing" "Live Session-Deck-Builder" "Knowledge Graph" "Mini-UT Context" "B2B Channels" "Instructors "; do
  if [ -d "$WORK/$d" ]; then
    echo -e "  ${GREEN}✓${NC} $d"
  else
    echo -e "  ${RED}✗${NC} $d  ${YELLOW}(missing — get the latest from Utkarsh)${NC}"
  fi
done

# Step 3 — symlink live skills/knowledge so updates flow
echo ""
echo -e "${CYAN}Linking plugin to live workspace (so updates flow automatically)...${NC}"
mkdir -p "$PLUG/skills/doc-proposal" "$PLUG/skills/pricing" "$PLUG/skills/requirement-mapping" \
         "$PLUG/skills/live-session-deck" "$PLUG/skills/pptx-deck" "$PLUG/skills/mini-ut-context"

link() {
  local target="$1" link="$2" name="$3"
  if [ -f "$target" ] || [ -d "$target" ]; then
    rm -f "$link" 2>/dev/null || true
    ln -sf "$target" "$link"
    echo -e "  ${GREEN}↪${NC} $name"
  else
    echo -e "  ${YELLOW}–${NC} $name ${YELLOW}(source missing)${NC}"
  fi
}

# Knowledge (KG)
rm -rf "$PLUG/knowledge" 2>/dev/null || true
if [ -d "$WORK/Knowledge Graph/_kg" ]; then
  ln -s "$WORK/Knowledge Graph/_kg" "$PLUG/knowledge"
  echo -e "  ${GREEN}↪${NC} knowledge/ → Knowledge Graph/_kg"
fi

# Skill files
link "$WORK/Doc Proposal Builder/Doc_Proposal_Skills.md"                       "$PLUG/skills/doc-proposal/SKILL.md"          "doc-proposal"
link "$WORK/Pricing/Pricing_Skills.md"                                          "$PLUG/skills/pricing/SKILL.md"               "pricing"
link "$WORK/Requirement to Session Mapping Builder /Session_Mapping_Skills.md"  "$PLUG/skills/requirement-mapping/SKILL.md"   "requirement-mapping"
link "$WORK/Live Session-Deck-Builder/Live_Session_Deck_Skills.md"              "$PLUG/skills/live-session-deck/SKILL.md"     "live-session-deck"
link "$WORK/Deck Proposal Builder /HTML-to-PPTX Converter/HTML_to_PPTX_Skills.md" "$PLUG/skills/pptx-deck/SKILL.md"            "pptx-deck"
link "$WORK/Mini-UT Context/context.md"                                          "$PLUG/skills/mini-ut-context/SKILL.md"       "mini-ut-context (principles)"
link "$WORK/Mini-UT Context/utkarsh_context.md"                                  "$PLUG/skills/mini-ut-context/utkarsh_context.md" "mini-ut-context (utkarsh profile)"
link "$WORK/Instructors /Acceler B2B Instructor Pool.md"                         "$PLUG/skills/mini-ut-context/Instructor_Pool.md" "instructor pool"

# Step 4 — outputs folder
mkdir -p "$WORK/Outputs"
echo ""
echo -e "  ${GREEN}✓${NC} Outputs folder ready at: $WORK/Outputs"

# Step 5 — done
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Setup complete.${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Try it now — open Claude Code in any terminal (Warp / iTerm / VS Code / etc):"
echo ""
echo "  claude"
echo "  /acceler:full-cycle"
echo ""
echo "Or any individual stage:"
echo "  /acceler:discovery · /acceler:similar · /acceler:proposal · /acceler:deck"
echo "  /acceler:pricing · /acceler:instructors · /acceler:coverage"
echo ""
echo "Workspace: $WORK"
echo "Outputs:   $WORK/Outputs"
echo ""
