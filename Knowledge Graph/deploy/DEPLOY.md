# Deploying the Knowledge Graph to Vercel (password-protected)

This folder is a ready-to-deploy static site:
- `index.html` — the full graph (self-contained; data + Acceler logo embedded)
- `middleware.js` — serves a branded **Acceler login screen** at the edge and only
  sends `index.html` after a correct username/password (refuses to serve at all unless
  a password is set)

> ⚠️ This site exposes confidential data: 61 client names, 729 instructor LinkedIn
> profiles, and Acceler pricing/margins. **Do not deploy it public.** The login gate
> below runs at the edge — `index.html` is never sent to an unauthenticated visitor.

## One-time deploy (from this `deploy/` folder)

```bash
cd "Knowledge Graph/deploy"
npx vercel              # first run: prompts you to log in, then links/creates a project
```
Accept the defaults (Framework preset = **Other**, no build command, output = current dir).

## Set the password (required — site stays 503 until you do)

In the Vercel dashboard → your project → **Settings → Environment Variables**, add:
- `KG_USER` = e.g. `acceler`
- `KG_PASS` = a strong shared password

…or via CLI:
```bash
npx vercel env add KG_PASS production
npx vercel env add KG_USER production
```

Then promote to production:
```bash
npx vercel --prod
```

Visiting the URL now prompts for the username/password before anything loads.

## Updating later
After re-running the KG pipeline, refresh the deployed copy:
```bash
cp ../_kg/graph.html ./index.html
npx vercel --prod
```

## Notes
- The "Open file" links in file panels are hidden when hosted (the source .docx/.pptx
  files live only on the local drive and are not deployed) — everything else works.
- For team-wide SSO instead of a shared password, use Vercel Pro **Deployment
  Protection → Vercel Authentication** and delete `middleware.js`.
