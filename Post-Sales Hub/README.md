# Acceler Atlas · Delivery, documentation hub

The docs hub for the post-sales plugin (`acceler-post-sales`). The plugin itself lives in
[voldemortuk/acceler-presales-plugin](https://github.com/voldemortuk/acceler-presales-plugin), in the `post-sales/` folder.

- `index.html` and `img/`: the hub, one static page.
- `middleware.js`: the same Google Sign-In gate as `Knowledge Graph/deploy/`. The site answers 503 until
  `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` and `SESSION_SECRET` are set in Vercel. The site's
  `/__auth/callback` address must also be added to the Google OAuth client as a redirect URI.

Published from Tanmaya's Vercel: run `npx vercel --prod` from inside this folder.
Every change is pushed here and published, in that order.

Maintained by Utkarsh Raj and Tanmaya Kharyal.
