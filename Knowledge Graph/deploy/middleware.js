// Edge middleware: gates the whole site behind a branded Acceler login screen.
// Real protection — the login page is served at the edge BEFORE index.html (which
// contains the confidential data) is ever sent. Not a bypassable client-side gate.
//
// Set KG_USER and KG_PASS as Environment Variables in the Vercel project.
// Refuses to serve at all if KG_PASS is unset, so the data can't go public by accident.
export const config = { matcher: '/(.*)' };

const COOKIE = 'kg_auth';

async function token(user, pass) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`${user}::${pass}`));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function loginPage(err) {
  const msg = err ? '<div class="err">Incorrect username or password</div>' : '';
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Acceler · Sign in</title><style>
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{display:flex;align-items:center;justify-content:center;background:
 radial-gradient(circle at 30% 20%,#16204a 0%,#0B1228 72%);
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;color:#E8EDF9}
.card{width:340px;background:#121B3A;border:1px solid #243161;border-radius:16px;
 padding:30px 28px;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.logo{font-size:34px;font-weight:800;letter-spacing:-.03em;color:#fff;line-height:1}
.logo .sq{display:inline-block;width:15px;height:15px;background:#27B4E6;border-radius:3px;margin-right:3px}
.sub{font-size:12px;color:#9AA6C8;margin:8px 0 22px;letter-spacing:.04em}
label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;
 color:#9AA6C8;font-weight:700;margin:14px 0 6px}
input{width:100%;background:#0B1228;border:1.5px solid #243161;border-radius:9px;
 padding:11px 12px;font-size:14px;color:#E8EDF9;outline:none}
input:focus{border-color:#27B4E6}
button{width:100%;margin-top:22px;background:#27B4E6;color:#0B1228;font-weight:800;
 font-size:15px;border:0;border-radius:9px;padding:12px;cursor:pointer}
button:hover{background:#3fc0ef}
.err{background:#3a1f2c;border:1px solid #7a3a55;color:#f6c9da;font-size:12.5px;
 padding:9px 11px;border-radius:8px;margin-bottom:4px}
.foot{text-align:center;font-size:10.5px;color:#5B6685;margin-top:18px}
</style></head><body>
<form class="card" method="POST" action="/__login">
 <div class="logo"><span class="sq"></span>acceler</div>
 <div class="sub">Pre-Sales Knowledge Graph</div>
 ${msg}
 <label>Username</label>
 <input name="user" autocomplete="username" autofocus/>
 <label>Password</label>
 <input name="pass" type="password" autocomplete="current-password"/>
 <button type="submit">Sign in</button>
 <div class="foot">Confidential · authorized access only</div>
</form></body></html>`;
  return new Response(html, {
    status: err ? 401 : 200,
    headers: { 'content-type': 'text/html; charset=utf-8' },
  });
}

export default async function middleware(request) {
  const user = process.env.KG_USER || 'acceler';
  const pass = process.env.KG_PASS;
  if (!pass) {
    return new Response('KG_PASS is not set. Add KG_USER / KG_PASS env vars in Vercel, then redeploy.', { status: 503 });
  }

  const url = new URL(request.url);
  const good = await token(user, pass);

  // login form submission
  if (request.method === 'POST' && url.pathname === '/__login') {
    const form = await request.formData();
    if (String(form.get('user') || '') === user && String(form.get('pass') || '') === pass) {
      return new Response(null, {
        status: 302,
        headers: {
          'Set-Cookie': `${COOKIE}=${good}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=86400`,
          'Location': '/',
        },
      });
    }
    return loginPage(true);
  }

  // already signed in?
  const cookie = request.headers.get('cookie') || '';
  if (cookie.split(/;\s*/).includes(`${COOKIE}=${good}`)) {
    return; // continue to the static graph
  }

  return loginPage(false);
}
