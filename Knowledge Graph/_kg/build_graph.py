#!/usr/bin/env python3
"""
Pass 2: enrich files.json with content signals (tools, pricing, duration, topics)
from the text cache, then emit graph.json (nodes+edges) and INDEX.md.
Deterministic, no LLM.
"""
import os, re, json
from collections import defaultdict, Counter

OUT = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"
TXT = os.path.join(OUT, "text")
data = json.load(open(os.path.join(OUT, "files.json")))
files = data["files"]

# ---- content dictionaries --------------------------------------------------------
TOOLS = {
    # --- Assistants / chat LLMs ---
    "Copilot Studio": r"copilot studio",
    "M365 Copilot":   r"m365 copilot|microsoft 365 copilot|\bcopilot\b",
    "Claude":         r"\bclaude\b|anthropic",
    "ChatGPT/GPT":    r"chatgpt|gpt-4|gpt-5|openai|\bgpt\b",
    "Gemini":         r"\bgemini\b",
    "NotebookLM":     r"notebooklm|notebook lm",
    "Perplexity":     r"perplexity",
    # --- AI coding tools ---
    "Cursor":         r"\bcursor\b",
    "GitHub Copilot": r"github copilot",
    "Claude Code":    r"claude code",
    "Windsurf":       r"windsurf",
    "Replit":         r"\breplit\b",
    # --- Orchestration / frameworks ---
    "LangChain":      r"langchain",
    "LangGraph":      r"langgraph",
    "LlamaIndex":     r"llama.?index",
    "CrewAI":         r"crew.?ai",
    "AutoGen":        r"autogen",
    "Semantic Kernel":r"semantic kernel",
    "n8n":            r"\bn8n\b",
    "Power Automate": r"power automate",
    "Power Apps":     r"power apps",
    # --- Foundation-model platforms ---
    "AWS Bedrock":    r"bedrock",
    "Azure OpenAI":   r"azure openai|azure ai foundry",
    "Vertex AI":      r"vertex ai|vertexai",
    "Hugging Face":   r"hugging ?face",
    # --- Enterprise knowledge / productivity ---
    "Glean":          r"\bglean\b",
    "Workday":        r"\bworkday\b",
    # --- ML / data stack ---
    "PyTorch":        r"pytorch",
    "TensorFlow":     r"tensorflow|\bkeras\b",
    "Power BI":       r"power bi",
    "Tableau":        r"tableau",
    "Snowflake":      r"snowflake",
    "Databricks":     r"databricks",
    "Vector DB":      r"vector (db|database|store)|pinecone|weaviate|chroma|qdrant|faiss",
    # --- Capability concepts (kept as tool-tags for backward compat) ---
    "RAG":            r"\brag\b|retrieval.augmented",
    "Agents":         r"\bagent(s|ic)?\b",
    "Multi-Agent":    r"multi.?agent",
    "LLMOps":         r"llmops|mlops",
    "Fine-tuning":    r"fine.?tun",
    "Nuvepro Labs":   r"nuvepro|virtual lab",
}
# Unified topic taxonomy — MUST stay in sync with CANON in merge_instructors.py
TOPICS = {
    "Prompt Engineering": r"prompt engineering|prompting|prompt design",
    "RAG / Retrieval":    r"\brag\b|retrieval.aug|retrieval|knowledge base|vector (db|database|store|search)|semantic search",
    "Agentic AI":         r"agentic|ai agent|autonomous agent",
    "Multi-Agent Systems":r"multi.?agent|crew.?ai|autogen|agent orchestrat",
    "GenAI / Foundation Models": r"generative ai|gen\s?ai|foundation model|large language model|\bllm(s)?\b|diffusion model|\btransformer(s)?\b",
    "NLP":                r"\bnlp\b|natural language processing|text classification|named entity|sentiment analysis",
    "Computer Vision":    r"computer vision|image (recognition|classification|segmentation|generation)|object detection|opencv",
    "LLMOps / Production": r"llmops|model serving|model deployment|inference optimi|productioniz|guardrail",
    "MLOps":              r"\bmlops\b|ml pipeline|model monitoring|feature store|kubeflow|mlflow|model registry",
    "Machine Learning":   r"machine learning|deep learning|neural network|predictive model|classification model|\bml\b",
    "Data Science":       r"data scien|statistical model|experimentation|a/b test|hypothesis test",
    "Data Engineering":   r"data engineer|data pipeline|\betl\b|\bspark\b|\bkafka\b|airflow|data lake|data warehouse|databricks|snowflake",
    "Data & Analytics":   r"data analytics|data analysis|business intelligence|insights|visualization|\bsql\b|nlq|natural language query|tableau|power bi|dashboard",
    "Software Engineering": r"software engineer|backend|front.?end|full.?stack|microservice|clean code|code review|api design",
    "Systems Design":     r"system(s)? design|scalab|high.?availability|distributed system",
    "Cloud & DevOps":     r"kubernetes|docker|\baws\b|\bazure\b|\bgcp\b|devops|terraform|ci/cd|cloud native",
    "SRE / Observability": r"\bsre\b|site reliability|observability|incident manage|reliability engineer",
    "Security":           r"security|cybersecurity|threat|vulnerab|penetration|appsec",
    "Technical Program Management": r"technical program management|\btpm\b|program manager",
    "Product Management": r"product manager|product management|product owner|roadmap|product sense",
    "Leadership / Strategy": r"leadership|strategic|leaders|c-suite|exco|executive|cxo|transformation",
    "Sales":              r"sales (enablement|training|team|process|pipeline|productivity)|\bgtm\b|go.to.market|account executive|business development|revenue (team|enablement)",
    "Workplace Productivity": r"m365 copilot|microsoft 365 copilot|google (suite|workspace)|document intelligence|productivity booster|meeting (toolkit|summary|notes)|office productivity|powerpoint copilot|excel copilot",
    "Automation / No-Code": r"no.?code|low.?code|power automate|\bzapier\b|make\.com|\bn8n\b|workflow automation|process automation|\brpa\b|relevance ?ai",
    "Curriculum / Pedagogy": r"curriculum|module|hands.on|capstone|assignment|learning objective|instructional design",
    "Responsible AI / Governance": r"responsible ai|ai ethics|ai governance|model risk|ai safety|fairness|explainab|red team|hallucinat|data (privacy|sensitiv)|guardrail",
    "Finance":            r"\bfinance\b|fintech|trading|investment|banking|underwriting",
    "Marketing":          r"marketing|growth marketing|\bseo\b|demand gen|campaign",
    "Networking":         r"network engineering|\bsdn\b|routing|\bbgp\b",
    "HR / People":        r"\bhrbp\b|human resources|people ops|talent management|workforce|payroll|\bl&d\b|learning (and|&) development",
}

CUR = re.compile(r"(₹\s?[\d,]+(?:\.\d+)?(?:\s?(?:lakh|lac|cr|crore|k|/?\s?learner|/?\s?day|per learner|per day))?|\$\s?[\d,]+(?:\.\d+)?(?:\s?(?:k|m|/?\s?learner|/?\s?day|per learner|per day))?)", re.I)
DAYS  = re.compile(r"(\d{1,2})\s*[- ]?\s*day(?:s)?\b", re.I)
HOURS = re.compile(r"(\d{1,3})\s*[- ]?\s*(?:hour|hr|min)", re.I)
COHORT= re.compile(r"(\d{1,3})\s*(?:participant|learner|leader|attendee|pax|people|cohort)", re.I)
MARGIN= re.compile(r"(\d{1,2}(?:\.\d+)?)\s*%\s*(?:margin|markup)", re.I)

def find(dct, txt):
    low = txt.lower()
    return [k for k, pat in dct.items() if re.search(pat, low)]

# ---- pricing normalisation: turn noisy raw tokens into labelled bands -------------
def _amount(tok):
    """Return (currency, numeric_value) or None."""
    low = tok.lower()
    cur = "₹" if "₹" in tok else "$"
    m = re.search(r"([\d,]+(?:\.\d+)?)", tok)
    if not m:
        return None
    val = float(m.group(1).replace(",", ""))
    if "lakh" in low or "lac" in low:        val *= 1e5
    elif "cr" in low or "crore" in low:      val *= 1e7
    elif re.search(r"\d\s*m\b", low):        val *= 1e6
    elif re.search(r"\d\s*k\b", low):        val *= 1e3
    return (cur, val)

def _fmt(cur, val):
    def trim(x): return f"{x:.2f}".rstrip("0").rstrip(".")
    if cur == "₹":
        if val >= 1e7: return f"₹{trim(val/1e7)} Cr"
        if val >= 1e5: return f"₹{trim(val/1e5)} L"
        return f"₹{val:,.0f}" if val == int(val) else f"₹{trim(val)}"
    if val >= 1e6: return f"${trim(val/1e6)}M"
    if val >= 1e4: return f"${trim(val/1e3)}K"
    return f"${val:,.0f}" if val == int(val) else f"${trim(val)}"

# thresholds separating per-unit rates from whole-deal / package values
_UNIT_MAX = {"$": 5000, "₹": 200000}

def summarise_pricing(raw_tokens, margin=None, keep_deals=True):
    """Bucket raw pricing tokens into {rates, deals, margin}; drop noise.
    `keep_deals` is True only for costing/proposal docs — elsewhere large
    numbers are usually market-size / revenue noise, not real deal values."""
    rates, deals = {}, {}          # formatted -> value (dedupe by formatted label)
    for tok in raw_tokens:
        a = _amount(tok)
        if not a:
            continue
        cur, val = a
        if cur == "$" and val < 5:        # $1/$2/$3 → token-cost noise
            continue
        if cur == "₹" and val < 100:
            continue
        if val <= _UNIT_MAX[cur]:
            rates[_fmt(cur, val)] = val
        elif keep_deals:
            deals[_fmt(cur, val)] = val
    def order(d):
        return [k for k, _ in sorted(d.items(), key=lambda kv: kv[1])]
    out = {"rates": order(rates)[:8], "deals": order(deals)[:6]}
    if margin:
        out["margin"] = margin
    return out

# ---- enrich each file ------------------------------------------------------------
for f in files:
    f["tools"] = []; f["topics"] = []; f["pricing"] = []; f["duration"] = None; f["cohort"] = None
    tp = os.path.join(TXT, f["id"] + ".txt")
    if not os.path.exists(tp):
        continue
    txt = open(tp, encoding="utf-8", errors="ignore").read()
    head = txt[:20000]
    f["tools"]  = find(TOOLS, head)
    f["topics"] = find(TOPICS, head)
    if not f["program"]:
        # infer program from content topics
        if "Agentic AI" in f["topics"] or "Multi-Agent Systems" in f["topics"]:
            f["program"] = "AI Builder"
        elif "Leadership / Strategy" in f["topics"]:
            f["program"] = "AI for Leaders"
        elif "Product Management" in f["topics"]:
            f["program"] = "AI for PMs"
    prices = CUR.findall(txt)
    m = MARGIN.search(txt)
    margin = (m.group(1) + "% " + ("markup" if "markup" in m.group(0).lower() else "margin")) if m else None
    bands = summarise_pricing([p.strip() for p in prices], margin)
    f["price_bands"] = bands
    # flat list (rates + deals + margin) kept for search / simple chips
    f["pricing"] = bands["rates"] + bands["deals"] + ([bands["margin"]] if margin else [])
    d = DAYS.findall(head); h = HOURS.findall(head)
    if d:
        f["duration"] = max(set(d), key=d.count) + "-day"
    elif h:
        f["duration"] = h[0] + (" hr" if "hour" in head.lower() or "hr" in head.lower() else " min")
    c = COHORT.findall(head)
    if c: f["cohort"] = c[0]

# ---- build graph -----------------------------------------------------------------
nodes = {}
edges = []
def node(nid, label, ntype, **attrs):
    if nid not in nodes:
        nodes[nid] = {"id": nid, "label": label, "type": ntype, "count": 0, **attrs}
    nodes[nid]["count"] += 1
    return nid

def edge(s, t, rel):
    edges.append({"source": s, "target": t, "rel": rel})

# friendly client labels: strip leading "N. " etc
def clean_client(c):
    return re.sub(r"^\d+\.\s*", "", c).strip()

client_programs = defaultdict(Counter)   # client -> program -> n
client_tools    = defaultdict(Counter)
program_tools   = defaultdict(Counter)
client_files    = defaultdict(list)

ROOTY = {"_Root", "Doc Versions", "APR - Pre-Sales Product", "AK - Cold Reachouts",
         "Generic Decks", "Marketing Decks", "Investor Slides", "Mentor Profiles",
         "Onboarding Forms", "Content for Ryan", "Doc Versions"}

for f in files:
    c = clean_client(f["client"])
    ctype = "asset" if f["client"] in ROOTY else "client"
    node("C:" + c, c, "client", ctype=ctype)
    client_files[c].append(f["id"])
    if f["program"]:
        node("P:" + f["program"], f["program"], "program")
        client_programs[c][f["program"]] += 1
        edge("F:" + f["id"], "P:" + f["program"], "covers")
    if f["doctype"]:
        node("D:" + f["doctype"], f["doctype"], "doctype")
    for t in f["tools"]:
        node("T:" + t, t, "tool")
        client_tools[c][t] += 1
        if f["program"]:
            program_tools[f["program"]][t] += 1
    # file node (lightweight; full detail kept in files.json)
    nodes["F:" + f["id"]] = {
        "id": "F:" + f["id"], "label": f["name"], "type": "file",
        "client": c, "program": f["program"], "doctype": f["doctype"],
        "version": f["version"], "ext": f["ext"], "path": f["path"],
        "tools": f["tools"], "topics": f["topics"], "pricing": f["pricing"],
        "price_bands": f.get("price_bands"),
        "duration": f["duration"], "cohort": f["cohort"], "count": 1,
    }
    edge("F:" + f["id"], "C:" + c, "belongs-to")
    if f["doctype"]:
        edge("F:" + f["id"], "D:" + f["doctype"], "is-a")

# aggregated client->program and client->tool edges (backbone)
for c, progs in client_programs.items():
    for p, n in progs.items():
        edges.append({"source": "C:" + c, "target": "P:" + p, "rel": "engages", "weight": n})
for c, ts in client_tools.items():
    for t, n in ts.items():
        if n >= 1:
            edges.append({"source": "C:" + c, "target": "T:" + t, "rel": "uses", "weight": n})

graph = {"nodes": list(nodes.values()), "edges": edges,
         "meta": {"clients": len([n for n in nodes.values() if n["type"]=="client" and n.get("ctype")=="client"]),
                  "programs": len([n for n in nodes.values() if n["type"]=="program"]),
                  "files": len(files),
                  "tools": len([n for n in nodes.values() if n["type"]=="tool"])}}

with open(os.path.join(OUT, "graph.json"), "w") as f:
    json.dump(graph, f, indent=1)

# re-dump enriched files
with open(os.path.join(OUT, "files.json"), "w") as f:
    json.dump(data, f, indent=1)

# ---- INDEX.md --------------------------------------------------------------------
lines = ["# Acceler — Pre-Sales Knowledge Graph Index", ""]
lines.append(f"_{graph['meta']['files']} files · {graph['meta']['clients']} clients · "
             f"{graph['meta']['programs']} programs · {graph['meta']['tools']} tools_\n")
by_client = defaultdict(list)
for f in files:
    by_client[clean_client(f["client"])].append(f)
order = sorted(by_client.items(), key=lambda kv: (-len(kv[1]), kv[0]))
for c, fs in order:
    progs = Counter(f["program"] for f in fs if f["program"])
    tools = Counter(t for f in fs for t in f["tools"])
    lines.append(f"## {c}  ({len(fs)} files)")
    if progs: lines.append("- **Programs:** " + ", ".join(f"{p} ({n})" for p,n in progs.most_common()))
    if tools: lines.append("- **Tools/Tech:** " + ", ".join(f"{t}" for t,_ in tools.most_common(8)))
    # notable pricing — labelled bands, deduped across the client's files
    rates, deals, margins = [], [], []
    for f in fs:
        b = f.get("price_bands") or {}
        rates += b.get("rates", []); deals += b.get("deals", [])
        if b.get("margin"): margins.append(b["margin"])
    rates  = list(dict.fromkeys(rates))[:6]
    deals  = list(dict.fromkeys(deals))[:4]
    margins= list(dict.fromkeys(margins))[:2]
    parts = []
    if rates:   parts.append("Rates " + " · ".join(rates))
    if deals:   parts.append("Deal size " + " · ".join(deals))
    if margins: parts.append("Margin " + " · ".join(margins))
    if parts: lines.append("- **Pricing:** " + "  |  ".join(parts))
    lines.append("")
with open(os.path.join(OUT, "INDEX.md"), "w") as f:
    f.write("\n".join(lines))

print("nodes:", len(nodes), "edges:", len(edges))
print("meta:", graph["meta"])
print("files with tools:", sum(1 for f in files if f["tools"]))
print("files with pricing:", sum(1 for f in files if f["pricing"]))
