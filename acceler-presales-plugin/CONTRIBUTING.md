# Contributing to acceler-presales

This repo **is** the Claude Code marketplace (`.claude-plugin/marketplace.json` at the root) and the plugin source. It is the single source of truth — edit here, not in any local `…/APR - Pre-Sales Product/acceler-presales-plugin` copy.

## Install (teammates)

```
/plugin marketplace add voldemortuk/acceler-presales-plugin
/plugin install acceler-presales@acceler-local
```

Private repo — authenticate first with `gh auth login` (or SSH). To get updates later:

```
/plugin marketplace update acceler-local
```

## Make a change (contributors)

1. Get added as a **collaborator** on the repo (ask Utkarsh), then branch + PR.
2. Edit the relevant `commands/*.md`, `skills/*/SKILL.md`, or `knowledge/*` files.
3. **Bump the version** in `.claude-plugin/plugin.json` (e.g. `0.2.0` → `0.3.0`) and add a `CHANGELOG.md` entry. *If you don't bump the version, teammates keep the cached copy and your change won't ship.*
4. Validate before pushing: `claude plugin validate .`
5. Open a PR. On merge, teammates pick it up with `/plugin marketplace update acceler-local`.

## Conventions

- Keep the marketplace name `acceler-local` stable — it's the `@suffix` in everyone's install id (`acceler-presales@acceler-local`). Renaming it breaks existing installs.
- `knowledge/` holds confidential data (client names, instructor LinkedIn/PII, pricing). **Keep this repo private.** Never make it public.
- `knowledge/instructor_delivery_flags.json` records who is pre-sales-only vs deliverable — keep it current as engagements land or fall through.
