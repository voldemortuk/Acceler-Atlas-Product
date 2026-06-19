#!/usr/bin/env python3
"""Parse the 4 dedicated instructor files into the batch-record schema.
Skips ALL PII (phone/PAN/bank/cheque/email). Emits out/pool_instructors.json."""
import csv, re, json, os

SRC = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Instructors "
OUT = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg/out"

# ---- topic mapping (expanded taxonomy) ------------------------------------------
SECTION_MAP = {
 "agentic ai":"Agentic AI", "ai swe instructors":"Software Engineering",
 "microservices":"Software Engineering", "managing technical debt, clean code & dora metrics":"Software Engineering",
 "regression, observability & reliability":"SRE / Observability",
 "sre best practices & observability":"SRE / Observability", "systems design for sre":"Systems Design",
 "customer focus":"Leadership / Strategy", "influencing without authority":"Leadership / Strategy",
 "ai leaders":"Leadership / Strategy", "networking":"Networking",
 "python for data analytics & audit":"Data & Analytics", "sql":"Data & Analytics",
 "intermediate data extraction & analytics":"Data & Analytics",
 "data mesh & medallia":"Data & Analytics", "data mesh":"Data & Analytics", "medallia":"Data & Analytics",
 "prompt engineering":"Prompt Engineering", "ai tools for pms":"Product Management",
 "business case writing":"Product Management", "product sense":"Product Management",
 "kubernetes, docker & aws":"Cloud & DevOps",
 "advanced genai engineering & productionization":"LLMOps / Production",
 "hr":"HR / People", "finance":"Finance", "ai in marketing profiles":"Marketing",
}
DOMAIN_RULES = [
 (r"machine learning|ml switchup|\bmle\b|\bml\b", "Machine Learning"),
 (r"data science|\bds\b", "Data Science"),
 (r"data analyst|business analyst|data analytics|analytics", "Data & Analytics"),
 (r"data engineering", "Data & Analytics"),
 (r"technical program management|\btpm\b", "Technical Program Management"),
 (r"product management|\bpm\b|product manager", "Product Management"),
 (r"backend|fullstack|full stack|frontend|front end|test engineering|embedded|software|\bswe\b", "Software Engineering"),
 (r"engineering manager|engineering leadership|\bem\b", "Leadership / Strategy"),
 (r"genai|generative ai", "LLMOps / Production"),
 (r"\bsre\b|reliability", "SRE / Observability"),
 (r"security|cyber", "Security"),
 (r"finance", "Finance"),
 (r"\bhr\b|people", "HR / People"),
]
KW = {  # bio/interest keyword -> topic
 "Agentic AI": r"agentic|ai agent", "Multi-Agent Systems": r"multi.?agent",
 "RAG / Retrieval": r"\brag\b|retrieval|vector", "LLMOps / Production": r"llmops|mlops|production|deploy|llm pipeline",
 "Machine Learning": r"machine learning|deep learning|\bml\b|neural|models",
 "Data Science": r"data scien|statistic", "Data & Analytics": r"analytics|\bsql\b|tableau|power bi|dashboard",
 "Software Engineering": r"software engineer|backend|full.?stack|microservice|distributed systems|clean code",
 "Systems Design": r"system design|systems design|scalab|high.?load",
 "Cloud & DevOps": r"kubernetes|docker|\baws\b|\bgcp\b|azure|devops|terraform",
 "SRE / Observability": r"\bsre\b|observability|reliability|incident",
 "Security": r"security|cyber|ciso|cissp", "Leadership / Strategy": r"leadership|strategy|director|\bvp\b|head of|cxo|c-suite",
 "Product Management": r"product manage|product sense|roadmap|\bpm\b",
 "Technical Program Management": r"program management|\btpm\b|program manager",
 "Prompt Engineering": r"prompt", "Finance": r"finance|fintech|trading|quant", "Marketing": r"marketing|growth|seo",
 "HR / People": r"\bhr\b|talent|recruit|people ops",
}
def topics_from_text(*txts):
    blob = " ".join(t for t in txts if t).lower()
    out = []
    for topic, pat in KW.items():
        if re.search(pat, blob): out.append(topic)
    return out
def topics_from_domain(dom):
    low = (dom or "").lower(); out = []
    for pat, topic in DOMAIN_RULES:
        if re.search(pat, low): out.append(topic)
    return out

def clean_li(u):
    if not u: return None
    u = u.strip().strip("[]()")
    if "linkedin.com/in/" not in u.lower(): return None
    if u.rstrip("/").lower().endswith("linkedin.com/in"): return None  # empty stub
    return u
def clean_name(n):
    n = re.sub(r"\(\s*(IN|US|UK|CA)\s*\)", "", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).strip(" -–—*\t")
    return n

records = []
def add(name, linkedin=None, role=None, expertise=None, topics=None, source=""):
    name = clean_name(name or "")
    if not name or " " not in name or len(name) < 4: return
    records.append({"name": name, "linkedin": clean_li(linkedin), "role": role,
        "expertise_verbatim": [e for e in (expertise or []) if e],
        "topics": sorted(set(topics or [])), "source_files": [source], "clients": []})

# ---- 1) Markdown pool (topic-structured) ----------------------------------------
md = open(os.path.join(SRC, "Acceler B2B Instructor Pool.md"), encoding="utf-8", errors="ignore").read().splitlines()
cur_topic = None
pending = None  # (name, desc)
def flush(li=None):
    global pending
    if pending:
        nm, desc = pending
        tp = SECTION_MAP.get(cur_topic, None)
        add(nm, li, role=(desc or None), expertise=[desc] if desc else [],
            topics=[tp] if tp else [], source="Acceler B2B Instructor Pool.md")
        pending = None
for line in md:
    h = re.match(r"^##\s*\*?\*?(.+?)\*?\*?\s*$", line.strip())
    if h:
        flush(); cur_topic = h.group(1).strip().lower().strip("* "); continue
    liname = re.match(r"^\s*\*\s+([^\[].*?)\s*$", line)  # name bullet (not a link line)
    lilink = re.search(r"linkedin\.com/in/\S*", line, re.I)
    if lilink and pending:                       # link line for pending name
        flush("https://" + re.sub(r"^https?://", "", lilink.group(0)).rstrip(")]"))
        continue
    if liname and "linkedin.com" not in line.lower():
        flush()
        raw = liname.group(1).strip()
        desc = None
        m = re.split(r"\s[–-]\s", raw, 1)
        if len(m) == 2: raw, desc = m[0], m[1]
        pending = (raw, desc)
flush()

# ---- 2) Senior Instructors.csv --------------------------------------------------
with open(os.path.join(SRC, "Senior Instructors.csv"), newline="", encoding="utf-8", errors="ignore") as f:
    for row in list(csv.reader(f))[1:]:
        if len(row) < 6 or not row[0].strip(): continue
        name, domain, _taking, roleco, edu, li = row[0], row[1], row[2], row[3], row[4], row[5]
        tps = topics_from_domain(domain) + topics_from_text(roleco)
        add(name, li, role=roleco or None, expertise=[x for x in [roleco, domain] if x],
            topics=tps, source="Senior Instructors.csv")

# ---- 3) Instructors.csv (offset by 1 blank col) ---------------------------------
with open(os.path.join(SRC, "Instructors.csv"), newline="", encoding="utf-8", errors="ignore") as f:
    rows = list(csv.reader(f))
for row in rows[2:]:
    if len(row) < 6 or not row[1].strip(): continue
    name, li, _mkt, _web, intro = row[1], row[2], row[3], row[4], row[5]
    add(name, li, role=(intro[:120] or None), expertise=[intro] if intro else [],
        topics=topics_from_text(intro), source="Instructors.csv")

# ---- 4) Directory Responses (SKIP PII cols 16-19) -------------------------------
with open(os.path.join(SRC, "Instructors Directory - Responses.csv"), newline="", encoding="utf-8", errors="ignore") as f:
    rows = list(csv.reader(f))
hdr = rows[0]
for row in rows[1:]:
    if len(row) < 14 or not row[2].strip(): continue
    name = row[2]; li = row[4]; bio = row[5]; interests = row[8]
    domain = (row[13] or row[12]) if len(row) > 13 else ""
    tps = topics_from_domain(domain) + topics_from_text(interests, bio)
    add(name, li, role=(bio[:140] or None), expertise=[x for x in [interests] if x],
        topics=tps, source="Instructors Directory - Responses.csv")

json.dump({"instructors": records}, open(os.path.join(OUT, "pool_instructors.json"), "w"),
          indent=1, ensure_ascii=False)
print("pool records emitted:", len(records))
from collections import Counter
print("by source:", Counter(r["source_files"][0] for r in records))
print("with linkedin:", sum(1 for r in records if r["linkedin"]))
print("with >=1 topic:", sum(1 for r in records if r["topics"]))
