#!/usr/bin/env bash
# Acceler — one-shot git+LFS bootstrap for voldemortuk/APR-Presales-Product
# Run from inside ~/Downloads/1. PowerUp/APR - Pre-Sales Product/
#
# Usage:
#   bash push.sh
#   git push -u origin main      # ← you run this last (uses your GitHub auth)

set -e

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Acceler — Push to voldemortuk/APR-Presales-Product${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 0. Sanity check — confirm we're in the right folder
if [ ! -f "acceler-os.html" ] || [ ! -d "Knowledge Graph" ]; then
  echo -e "${RED}✗ Run this from inside the APR - Pre-Sales Product folder.${NC}"
  echo "  cd ~/Downloads/\"1. PowerUp\"/\"APR - Pre-Sales Product\""
  exit 1
fi
echo -e "${GREEN}✓${NC} In the right folder: $(pwd)"

# 1. Check git + git-lfs
if ! command -v git &>/dev/null; then
  echo -e "${RED}✗ git not installed.${NC} Install: brew install git"
  exit 1
fi
if ! command -v git-lfs &>/dev/null; then
  echo -e "${YELLOW}!${NC} git-lfs missing — installing now"
  if command -v brew &>/dev/null; then
    brew install git-lfs
  else
    echo -e "${RED}✗ brew not found.${NC} Install brew first: https://brew.sh"
    exit 1
  fi
fi
echo -e "${GREEN}✓${NC} git $(git --version | awk '{print $3}') · git-lfs $(git-lfs version | awk '{print $1}')"

# 2. Initialize repo if not already
if [ ! -d ".git" ]; then
  echo ""
  echo -e "${CYAN}→ git init${NC}"
  git init -b main
else
  echo -e "${GREEN}✓${NC} Repo already initialized"
fi

# 3. Identity (only set if not already)
if [ -z "$(git config user.email 2>/dev/null)" ]; then
  git config user.email "new-programs@interviewkickstart.com"
  git config user.name "Utkarsh Raj"
  echo -e "${GREEN}✓${NC} Set git identity (Utkarsh Raj <new-programs@interviewkickstart.com>)"
fi

# 4. Git LFS
echo ""
echo -e "${CYAN}→ git lfs install${NC}"
git lfs install --local

# .gitattributes already tracks the LFS patterns — verify
echo -e "${GREEN}✓${NC} LFS patterns active:"
git lfs track 2>/dev/null | grep -E "\.(docx|pptx|xlsx|pdf|json)" | head -8

# 5. Show what's about to be committed
echo ""
echo -e "${CYAN}→ Staging files (respecting .gitignore)${NC}"
git add .gitignore .gitattributes README.md
git add .
COUNT=$(git status --short | wc -l | tr -d ' ')
SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo -e "${GREEN}✓${NC} $COUNT files staged · folder size $SIZE (acceler-lms/ and WhatsApp media excluded)"

# 6. Confirm before commit
echo ""
echo -e "${YELLOW}Review what's being committed (first 30):${NC}"
git status --short | head -30
EXTRA=$(git status --short | wc -l)
if [ "$EXTRA" -gt 30 ]; then
  echo "  …and $(($EXTRA - 30)) more"
fi
echo ""
read -r -p "Commit and continue? [y/N] " ANS
if [[ ! "$ANS" =~ ^[Yy]$ ]]; then
  echo "Aborted. Run \`git reset\` to unstage if you want."
  exit 0
fi

# 7. Commit
echo ""
echo -e "${CYAN}→ git commit${NC}"
git commit -m "Acceler B2B Pre-Sales workspace — initial snapshot

Includes:
- acceler-os.html (workspace UI · KG-wired)
- acceler-presales-kt.html (handover slide deck)
- acceler-presales-plugin/ (Claude Code plugin)
- Skills: Doc Proposal · Pricing · Session Mapping · Live Session Deck · PPTX Deck · Mini-UT Context
- Knowledge Graph: 69 clients · 1,072 files · 746 instructors · 39 tools · 30 topics
- Sample Proposals: Nucleus India · Booking India · Gryphon US · MCB Self-Paced
- B2B Channels (team-chat summaries) · Mini-UT Context (chat text exports)

Excluded via .gitignore: acceler-lms/ (3GB LMS build), WhatsApp media, Outputs/, build cache."

# 8. Remote
echo ""
if git remote get-url origin &>/dev/null; then
  echo -e "${GREEN}✓${NC} Remote 'origin' already set: $(git remote get-url origin)"
else
  echo -e "${CYAN}→ Adding remote: voldemortuk/APR-Presales-Product${NC}"
  git remote add origin https://github.com/voldemortuk/APR-Presales-Product.git
fi

# 9. Done — show next step
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Ready to push.${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Now run:"
echo ""
echo -e "  ${YELLOW}git push -u origin main${NC}"
echo ""
echo "If GitHub asks for credentials and you don't have a token set up:"
echo -e "  ${YELLOW}gh auth login${NC}                    # one-time"
echo -e "  ${YELLOW}git push -u origin main${NC}"
echo ""
echo "First push uploads LFS objects too — expect 1-3 minutes depending on connection."
