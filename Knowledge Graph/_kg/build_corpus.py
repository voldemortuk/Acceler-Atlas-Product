#!/usr/bin/env python3
"""
Pass 1: walk the PowerUp corpus, classify every file (client/program/doc-type/version)
and extract its raw text to a cache. No LLM, no new deps.
Extractors: textutil (docx/doc/rtf), pdftotext (pdf), zipfile+xml (pptx/xlsx), direct read (md/html/txt).
"""
import os, re, json, zipfile, subprocess, hashlib
from xml.etree import ElementTree as ET

ROOT = "/Users/voldemort/Downloads/1. PowerUp"
OUT  = os.path.join(ROOT, "_kg")
TXT  = os.path.join(OUT, "text")
os.makedirs(TXT, exist_ok=True)

SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__", "_kg"}
SKIP_EXT  = {".js", ".ts", ".map", ".mjs", ".cjs", ".cts", ".mts", ".meta", ".sst",
             ".rsc", ".lock", ".woff", ".woff2", ".ttf", ".ico", ".svg", ".css",
             ".eslintrc", ".gitignore", ".node", ".wasm", ".d.ts"}
DOC_EXT   = {".docx", ".doc", ".pptx", ".xlsx", ".pdf", ".md", ".html", ".htm", ".txt", ".rtf"}
IMG_EXT   = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# ---- classification dictionaries -------------------------------------------------
# Top-level dirs that are clients/accounts (everything else loose-at-root => "_Root")
PROGRAM_PATTERNS = [
    ("AI Builder (Pro Code)", r"builder.*pro|pro.?code|pro code"),
    ("AI Builder (Low Code)",  r"builder.*low|low.?code|no.?code|no code"),
    ("AI Builder",             r"\bbuilder\b|builders accelerator|ai builders"),
    ("AI Enabler",             r"\benabler\b"),
    ("AI for Leaders",         r"for leaders|leadership|strategic leaders|leaders build|leaders accelerator"),
    ("AI for PMs",             r"for pms|product manager|ai.?enabled product|for pm\b"),
    ("Masterclass",            r"masterclass|master class"),
    ("Build Lab",              r"build lab|build-lab"),
    ("Cybersecurity Accelerator", r"cybersecurity|security"),
    ("SDLC",                   r"sdlc"),
    ("Discovery / Pre-Sales",  r"discovery|pre.?sales|pre-call|prep\b|onboarding"),
    ("Accelerator",            r"accelerator|accelerators"),
    ("Assessment",             r"assessment|gradesheet|test\b|mcq"),
    ("Intro / Overview",       r"intro|overview|detailed_intro|offering"),
]
DOCTYPE_PATTERNS = [
    ("Costing",      r"costing|pricing|price|costing template|costing sheet"),
    ("Proposal",     r"proposal|sow|statement of work|pitch|brief"),
    ("Curriculum",   r"curriculum|course outline|content|module|detailed content|syllabus"),
    ("Onboarding",   r"onboarding|pre-?requisit|setup|credentials|user manual|tools"),
    ("Assignment",   r"assignment"),
    ("Assessment",   r"assessment|gradesheet|mcq|test\b"),
    ("Profile",      r"profile|instructor|mentor|researcher profiles|list of instructors"),
    ("Requirement",  r"requirement|requirements|response|feedback|questions"),
    ("Deck",         r"\.pptx$|\.pdf$|deck|slides|keynote"),
    ("Email",        r"\bmail\b|email|communication"),
]
EXT_DOCTYPE = {".pptx": "Deck", ".xlsx": "Costing", ".pdf": "Deck",
               ".docx": "Document", ".doc": "Document", ".md": "Note",
               ".html": "Webpage", ".htm": "Webpage"}

def classify_program(name):
    low = name.lower()
    for label, pat in PROGRAM_PATTERNS:
        if re.search(pat, low):
            return label
    return None

def classify_doctype(name, ext):
    low = name.lower()
    for label, pat in DOCTYPE_PATTERNS:
        if re.search(pat, low):
            return label
    return EXT_DOCTYPE.get(ext, "Other")

def parse_version(name):
    low = name.lower()
    m = re.search(r"\bv(\d+)\b", low)
    if m: return "v" + m.group(1)
    m = re.search(r"(\d{1,2}[a-z]{3}\d{2})", low)  # 02Mar26
    if m: return m.group(1)
    m = re.search(r"(\d{8})", low)                 # 20260415
    if m: return m.group(1)
    if "final" in low: return "final"
    if "copy of" in low or re.search(r"\(\d+\)", low): return "copy"
    if "draft" in low: return "draft"
    return None

# ---- text extractors -------------------------------------------------------------
def x_textutil(path):
    try:
        r = subprocess.run(["textutil", "-convert", "txt", "-stdout", path],
                           capture_output=True, timeout=60)
        return r.stdout.decode("utf-8", "ignore")
    except Exception as e:
        return ""

def x_pdf(path):
    try:
        r = subprocess.run(["pdftotext", "-q", "-l", "40", path, "-"],
                           capture_output=True, timeout=120)
        return r.stdout.decode("utf-8", "ignore")
    except Exception:
        return ""

def x_pptx(path):
    out = []
    try:
        z = zipfile.ZipFile(path)
        names = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                       key=lambda s: int(re.search(r"(\d+)", s).group(1)))
        for n in names:
            try:
                root = ET.fromstring(z.read(n))
            except Exception:
                continue
            texts = [el.text for el in root.iter() if el.tag.endswith("}t") and el.text]
            if texts:
                out.append(" ".join(texts))
        z.close()
    except Exception:
        return ""
    return "\n".join(out)

def x_xlsx(path):
    out = []
    try:
        z = zipfile.ZipFile(path)
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root:
                txt = "".join(t.text or "" for t in si.iter() if t.tag.endswith("}t"))
                shared.append(txt)
        for n in [x for x in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", x)]:
            root = ET.fromstring(z.read(n))
            for c in root.iter():
                if c.tag.endswith("}c"):
                    t = c.get("t")
                    v = c.find("{*}v")
                    if v is not None and v.text is not None:
                        if t == "s":
                            try: out.append(shared[int(v.text)])
                            except: pass
                        else:
                            out.append(v.text)
        z.close()
    except Exception:
        return ""
    return " ".join(out)

def x_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        if path.lower().endswith((".html", ".htm")):
            data = re.sub(r"<script[\s\S]*?</script>", " ", data, flags=re.I)
            data = re.sub(r"<style[\s\S]*?</style>", " ", data, flags=re.I)
            data = re.sub(r"<[^>]+>", " ", data)
        return data
    except Exception:
        return ""

def extract(path, ext):
    if ext in (".docx", ".doc", ".rtf"): return x_textutil(path)
    if ext == ".pdf":   return x_pdf(path)
    if ext == ".pptx":  return x_pptx(path)
    if ext == ".xlsx":  return x_xlsx(path)
    if ext in (".md", ".html", ".htm", ".txt"): return x_text(path)
    return ""

# ---- walk ------------------------------------------------------------------------
nodes = {}      # id -> node
clients = {}    # client -> set
files = []
stats = {"scanned": 0, "extracted": 0, "empty": 0, "skipped": 0}

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    rel = os.path.relpath(dirpath, ROOT)
    parts = [] if rel == "." else rel.split(os.sep)
    client = parts[0] if parts else "_Root"
    for fn in filenames:
        if fn.startswith(".") or fn == ".DS_Store":
            continue
        ext = os.path.splitext(fn)[1].lower()
        if ext in SKIP_EXT:
            stats["skipped"] += 1
            continue
        if ext not in DOC_EXT and ext not in IMG_EXT and ext not in (".xlsx",):
            stats["skipped"] += 1
            continue
        full = os.path.join(dirpath, fn)
        relpath = os.path.relpath(full, ROOT)
        stats["scanned"] += 1
        program = classify_program(fn) or (classify_program(rel) if rel != "." else None)
        doctype = classify_doctype(fn, ext) if ext not in IMG_EXT else "Image"
        version = parse_version(fn)
        try: size = os.path.getsize(full)
        except: size = 0

        fid = hashlib.md5(relpath.encode()).hexdigest()[:10]
        txt = ""
        if ext in DOC_EXT:
            txt = extract(full, ext)
            txt = re.sub(r"[ \t]+", " ", txt)
            txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
            if txt:
                with open(os.path.join(TXT, fid + ".txt"), "w", encoding="utf-8") as f:
                    f.write(txt)
                stats["extracted"] += 1
            else:
                stats["empty"] += 1
        files.append({
            "id": fid, "name": fn, "path": relpath, "client": client,
            "program": program, "doctype": doctype, "version": version,
            "ext": ext, "size": size, "chars": len(txt),
        })
        clients.setdefault(client, 0)
        clients[client] += 1

with open(os.path.join(OUT, "files.json"), "w") as f:
    json.dump({"files": files, "clients": clients, "stats": stats}, f, indent=1)

print(json.dumps(stats, indent=1))
print("clients:", len(clients), " files indexed:", len(files))
print("top clients:", sorted(clients.items(), key=lambda x:-x[1])[:12])
