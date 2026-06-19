#!/usr/bin/env python3
"""Merge agent instructor extractions, dedupe, and augment graph.json with
Topic nodes, File->Topic, Instructor nodes, Topic->Instructor and Instructor->Client edges."""
import json, glob, re, os
OUT = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"

# Unified taxonomy — MUST stay in sync with TOPICS in build_graph.py
CANON = {"Prompt Engineering","RAG / Retrieval","Agentic AI","Multi-Agent Systems",
 "GenAI / Foundation Models","NLP","Computer Vision","LLMOps / Production","MLOps",
 "Machine Learning","Data Science","Data Engineering","Data & Analytics",
 "Software Engineering","Systems Design","Cloud & DevOps","SRE / Observability","Security",
 "Technical Program Management","Product Management","Leadership / Strategy",
 "Sales","Curriculum / Pedagogy","Responsible AI / Governance",
 "Workplace Productivity","Automation / No-Code",
 "Finance","Marketing","Networking","HR / People"}

# ---- authoritative topic classifier for instructor bios/titles ------------------
# Re-derives topics from each person's own role + expertise text, with guards so
# incidental mentions (e.g. "...BFSI and HR") and IK contribution roles (Teaching
# Assistant / "TA") never become an expertise tag.
TOPIC_RULES = [
 ("Agentic AI",            r"agentic|ai agent|autonomous agent"),
 ("Multi-Agent Systems",   r"multi.?agent|crew.?ai|autogen|agent orchestrat"),
 ("RAG / Retrieval",       r"\brag\b|retrieval.aug|vector (db|database|store|search)|semantic search|knowledge base"),
 ("Prompt Engineering",    r"prompt engineer|prompt design|prompting"),
 ("GenAI / Foundation Models", r"generative ai|gen\s?ai|foundation model|\bllm(s)?\b|large language model|diffusion|fine.?tun"),
 ("NLP",                   r"\bnlp\b|natural language processing|text mining|named entity|sentiment analysis|speech recognition"),
 ("Computer Vision",       r"computer vision|image (recognition|classification|segmentation|generation)|object detection|opencv"),
 ("LLMOps / Production",   r"llmops|model serving|inference optimi|llm (pipeline|deployment)|productioniz"),
 ("MLOps",                 r"\bmlops\b|ml pipeline|model monitoring|feature store|kubeflow|mlflow|model registry"),
 ("Machine Learning",      r"machine learning|deep learning|neural network|\bml\b|\bmle\b|predictive model|pytorch|tensorflow|reinforcement learning"),
 ("Data Science",          r"data scien|statistical model|\bstatistics\b|experimentation|a/b test|causal infer"),
 ("Data Engineering",      r"data engineer|data pipeline|\betl\b|\bspark\b|\bkafka\b|airflow|data lake|data warehouse|databricks|snowflake|data mesh"),
 ("Data & Analytics",      r"\banalytics\b|business intelligence|\bbi\b|\bsql\b|tableau|power bi|dashboard|data analyst"),
 ("Software Engineering",  r"software engineer|backend|front.?end|full.?stack|micro.?service|distributed system|clean code|\bswe\b|api design|embedded"),
 ("Systems Design",        r"system(s)? design|scalab|high.?throughput|low.?latency|high.?load"),
 ("Cloud & DevOps",        r"kubernetes|docker|\baws\b|\bgcp\b|\bazure\b|devops|terraform|cloud native|platform engineer"),
 ("SRE / Observability",   r"\bsre\b|site reliability|observability|incident (manage|response)|reliability engineer"),
 ("Security",              r"security|cyber|ciso|cissp|threat|penetration|appsec|infosec"),
 ("Technical Program Management", r"technical program (management|manager)|\btpm\b|program manager"),
 ("Product Management",    r"product manage|product manager|product owner|product sense|\bcpo\b|chief product"),
 ("Leadership / Strategy", r"leadership|strateg|\bvp\b|head of|\bdirector\b|\bcto\b|\bceo\b|\bcxo\b|\bcio\b|c-suite|engineering manager|\bfounder\b|principal"),
 ("Finance",               r"\bfinance\b|fintech|trading|\bquant\b|investment|\bbanking\b|risk model|actuar"),
 ("Marketing",             r"\bmarketing\b|growth marketing|\bseo\b|demand gen|brand strategy"),
 ("Networking",            r"network engineer|\bnetworking\b|\bsdn\b|\brouting\b|\bcisco\b|\bbgp\b"),
 ("Responsible AI / Governance", r"responsible ai|ai ethics|ai governance|ai safety|model risk|fairness|explainab"),
 ("Sales",                 r"\bsales\b|sales enablement|\bgtm\b|go.to.market|pre.?sales|solutions consult|business development|account executive"),
 ("Automation / No-Code",  r"no.?code|low.?code|power automate|\bzapier\b|\bn8n\b|workflow automation|\brpa\b"),
 ("Curriculum / Pedagogy", r"curriculum|instructional design|pedagog|learning design"),
]
# HR / People only fires on an HR *profession* signal — never an incidental
# "...and HR" domain mention, and never "talent" alone or "teaching assistant"/"TA".
HR_PROFESSION = re.compile(
    r"\b(chro|chief (people|human resources) officer|hrbp|head of (hr|people|talent)|"
    r"vp,?\s*(of\s*)?(hr|people|human resources)|people (partner|ops|operations|analytics)|"
    r"human resources|talent (acquisition|management)|recruit(er|ment) (lead|manager|head)|"
    r"\bl&d\b|learning (and|&) development|hr (transformation|tech|technology|leader|strategy|analytics))\b",
    re.I)

def classify_topics(blob):
    low = (blob or "").lower()
    # strip the IK contribution role so "teaching assistant"/"TA" never classifies
    low = re.sub(r"teaching assistant|\bt\.?a\.?\b", " ", low)
    found = set()
    for topic, pat in TOPIC_RULES:
        if re.search(pat, low):
            found.add(topic)
    if HR_PROFESSION.search(low):
        found.add("HR / People")
    return found

def norm(n):
    n = re.sub(r"\s*\(.*?\)\s*", " ", n or "")          # drop (IN) etc
    n = re.sub(r"https?://\S+", "", n)
    n = re.sub(r"[^A-Za-z .\-']", " ", n)
    n = re.sub(r"\b(Dr|Mr|Ms|Mrs|Prof)\.?\b", "", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).strip(" .-'\t")          # also strip leading/trailing punct (". Abdul" -> "Abdul")
    return n
def key(n):
    return norm(n).lower().replace(".", "").replace("-", " ").strip()

people = {}
sources_glob = sorted(glob.glob(os.path.join(OUT, "out/batch_*.json"))) + \
               [os.path.join(OUT, "out/pool_instructors.json")]
for fp in sources_glob:
    if not os.path.exists(fp): continue
    d = json.load(open(fp))
    for r in d.get("instructors", []):
        nm = norm(r.get("name", ""))
        k = key(nm)
        if not k or len(k) < 4 or " " not in k:   # require a plausible full name
            continue
        p = people.setdefault(k, {"name": nm, "linkedin": None, "role": None,
            "expertise": set(), "topics": set(), "sources": set(), "clients": set()})
        if len(nm) > len(p["name"]): p["name"] = nm
        if not p["linkedin"] and r.get("linkedin") and "linkedin" in str(r["linkedin"]).lower():
            p["linkedin"] = r["linkedin"]
        if r.get("role") and len(r["role"] or "") > len(p["role"] or ""):
            p["role"] = r["role"]
        for e in r.get("expertise_verbatim", []) or []:
            if e and e.strip(): p["expertise"].add(e.strip())
        # collect upstream topic hints (LLM/pool) but they are NOT trusted blindly
        for t in r.get("topics", []) or []:
            if t in CANON: p["topics"].add(t)
        for s in r.get("source_files", []) or []:
            if s: p["sources"].add(s)
        for c in r.get("clients", []) or []:
            if c: p["clients"].add(c)

# ---- re-derive each person's topics authoritatively, with guards ----------------
for p in people.values():
    blob = " ".join([p["role"] or ""] + sorted(p["expertise"]))
    auto = classify_topics(blob)
    upstream = set(p["topics"])
    # HR is the most over-fired tag: keep it ONLY when the profession guard agrees.
    if "HR / People" in upstream and "HR / People" not in auto:
        upstream.discard("HR / People")
    p["topics"] = (auto | upstream) & CANON

print("unique instructors after merge:", len(people))

# ---- load structural graph + files ----
graph = json.load(open(os.path.join(OUT, "graph.json")))
nodes = {n["id"]: n for n in graph["nodes"]}
edges = graph["edges"]
# strip any prior augmentation so script is idempotent
nodes = {k: v for k, v in nodes.items() if v["type"] not in ("topic", "instructor")}
edges = [e for e in edges if e.get("rel") not in ("covers-topic", "expert-in", "proposed-for")]

def clean_client(c): return re.sub(r"^\d+\.\s*", "", c or "").strip()
real_clients = {n["label"] for n in nodes.values() if n["type"]=="client" and n.get("ctype")=="client"}

# Topic nodes + File->Topic edges (from file node attrs)
topic_count = {}
for n in list(nodes.values()):
    if n["type"] == "file":
        for t in n.get("topics", []) or []:
            if t in CANON:
                topic_count[t] = topic_count.get(t, 0) + 1
inst_per_topic = {}
for p in people.values():
    for t in p["topics"]:
        if t in CANON: inst_per_topic[t] = inst_per_topic.get(t, 0) + 1
for t in CANON:
    tid = "TP:" + t
    nodes[tid] = {"id": tid, "label": t, "type": "topic",
                  "count": max(1, topic_count.get(t, 0) + inst_per_topic.get(t, 0))}
for n in list(nodes.values()):
    if n["type"] == "file":
        for t in set(n.get("topics", []) or []):
            if t in CANON:
                edges.append({"source": n["id"], "target": "TP:" + t, "rel": "covers-topic"})

# Instructor nodes + edges
inst_added = 0; te = 0; ce = 0
for k, p in people.items():
    iid = "I:" + k
    topics = sorted(p["topics"])
    nodes[iid] = {"id": iid, "label": p["name"], "type": "instructor",
        "linkedin": p["linkedin"], "role": p["role"],
        "expertise": sorted(p["expertise"])[:12], "topics": topics,
        "clients": sorted(p["clients"]), "sources": sorted(p["sources"])[:20],
        "count": max(1, len(topics))}
    inst_added += 1
    for t in topics:
        edges.append({"source": "TP:" + t, "target": iid, "rel": "expert-in"}); te += 1
    for c in p["clients"]:
        cc = clean_client(c)
        if cc in real_clients:
            edges.append({"source": iid, "target": "C:" + cc, "rel": "proposed-for"}); ce += 1

graph["nodes"] = list(nodes.values())
graph["edges"] = edges
graph["meta"]["instructors"] = inst_added
graph["meta"]["topics"] = len(CANON)
json.dump(graph, open(os.path.join(OUT, "graph.json"), "w"), indent=1, ensure_ascii=False)

# write a clean instructor roster for reference
roster = sorted([{"name": p["name"], "linkedin": p["linkedin"], "role": p["role"],
    "topics": sorted(p["topics"]), "expertise": sorted(p["expertise"])[:12],
    "clients": sorted(p["clients"])} for p in people.values()], key=lambda x: x["name"])
json.dump({"instructors": roster}, open(os.path.join(OUT, "instructors.json"), "w"), indent=1, ensure_ascii=False)

# topic -> count of instructors
from collections import Counter
tc = Counter(t for p in people.values() for t in p["topics"])
print("instructor nodes:", inst_added, "| expert-in edges:", te, "| proposed-for edges:", ce)
print("topic nodes:", len(CANON))
print("instructors per topic:")
for t, n in tc.most_common(): print(f"   {n:>3}  {t}")
print("with LinkedIn:", sum(1 for p in people.values() if p["linkedin"]))
