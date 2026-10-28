"""prior_art_gate, step 1: run the search strings of src/litcheck-queries.yaml and record what they return (read-only).

  python tools/litcheck.py [NN …]      → out/litcheck/NN.json, out/litcheck/SUMMARY.md

Sources: arXiv API (one request per 3 s, as arXiv asks), OpenAlex, zbMATH Open, Crossref (8 threads across problems),
and GitHub code search for the repositories listed under `code:` (gh CLI, authenticated, throttled). Each record keeps
the date, the source, the exact search string, the HTTP status and the first ten results (title, year, authors,
venue, DOI or arXiv id). Failures are recorded, not hidden. Conclusions are written by hand into the problem cards.
"""
import datetime as dt
import json
import subprocess
import sys
import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import working_proxy  # noqa: E402

OUT = HERE / "out" / "litcheck"
MAILTO = "vincent.liu@wisemotif.ai"
TODAY = dt.date.today().isoformat()
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROXY = working_proxy()
PROXIES = {"https": PROXY, "http": PROXY} if PROXY else None
ARXIV_LOCK = threading.Lock()
ARXIV_LAST = [0.0]
UA = {"User-Agent": f"grothendieckian-problems-litcheck/1.0 (mailto:{MAILTO})"}


def get(url, **kw):
    for attempt in range(3):
        try:
            return requests.get(url, headers=UA, proxies=PROXIES, timeout=60, **kw)
        except requests.RequestException as e:
            err = e
            time.sleep(5 * (attempt + 1))
    raise err


def arxiv(q):
    with ARXIV_LOCK:
        wait = 3.2 - (time.time() - ARXIV_LAST[0])
        if wait > 0:
            time.sleep(wait)
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": "all:" + " AND all:".join(q.split()), "max_results": 10, "sortBy": "relevance"})
        r = get(url)
        ARXIV_LAST[0] = time.time()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    res = []
    if r.ok:
        for e in ET.fromstring(r.content).findall("a:entry", ns):
            res.append({"title": " ".join(e.findtext("a:title", "", ns).split()),
                        "year": e.findtext("a:published", "", ns)[:4],
                        "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)][:6],
                        "id": e.findtext("a:id", "", ns).replace("http://arxiv.org/abs/", "arXiv:")})
    return r.status_code, res


def openalex(q):
    r = get("https://api.openalex.org/works", params={"search": q, "per-page": 10, "mailto": MAILTO})
    res = []
    if r.ok:
        for w in r.json().get("results", []):
            res.append({"title": w.get("display_name") or "", "year": w.get("publication_year"),
                        "authors": [a["author"]["display_name"] for a in w.get("authorships", [])][:6],
                        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                        "id": w.get("doi") or w.get("id")})
    return r.status_code, res


def zbmath(q):
    r = get("https://api.zbmath.org/v1/document/_search",
            params={"search_string": q, "page": 0, "results_per_page": 10})
    res = []
    if r.ok:
        for d in r.json().get("result", []):
            title = (d.get("title") or {}).get("title") if isinstance(d.get("title"), dict) else d.get("title")
            src = d.get("source") or {}
            res.append({"title": title or "", "year": d.get("year"),
                        "authors": [a.get("name") for a in (d.get("contributors") or {}).get("authors", [])][:6],
                        "venue": (src.get("series") or [{}])[0].get("title") if src.get("series") else None,
                        "id": f"zbMATH {d.get('identifier') or d.get('id')}"})
    return r.status_code, res


def crossref(q):
    r = get("https://api.crossref.org/works", params={"query.bibliographic": q, "rows": 10, "mailto": MAILTO})
    res = []
    if r.ok:
        for it in r.json().get("message", {}).get("items", []):
            res.append({"title": " ".join(it.get("title") or [""]),
                        "year": ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                        "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in it.get("author", [])][:6],
                        "venue": " ".join(it.get("container-title") or []), "id": "doi:" + it.get("DOI", "")})
    return r.status_code, res


GH_LOCK = threading.Lock()


def github(repo, term):
    with GH_LOCK:
        time.sleep(7)                                     # code search: 10 requests / minute
        env = None
        if PROXY:
            import os
            env = dict(os.environ, HTTPS_PROXY=PROXY)
        p = subprocess.run(["gh", "api", "-X", "GET", "search/code", "-f", f"q={term} repo:{repo}", "-f", "per_page=10"],
                           capture_output=True, text=True, encoding="utf-8", env=env)
    if p.returncode:
        return 0, [{"error": p.stderr.strip()[:200]}]
    items = json.loads(p.stdout).get("items", [])
    return 200, [{"path": i["path"], "url": i["html_url"]} for i in items]


SOURCES = {"arXiv": arxiv, "OpenAlex": openalex, "zbMATH Open": zbmath, "Crossref": crossref}


def run_problem(num, queries, code):
    rec = {"problem": int(num), "date": TODAY, "searches": []}
    for q in queries:
        for name, fn in SOURCES.items():
            try:
                status, res = fn(q)
            except Exception as e:  # recorded, never hidden
                status, res = 0, [{"error": f"{type(e).__name__}: {str(e)[:160]}"}]
            rec["searches"].append({"source": name, "query": q, "status": status, "results": res})
    for repo in (code or {}).get("repos", []):
        for term in code["terms"]:
            status, res = github(repo, term)
            rec["searches"].append({"source": f"GitHub code search {repo}", "query": term, "status": status,
                                    "results": res})
    (OUT / f"{int(num):02d}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8",
                                              newline="\n")
    ok = sum(1 for s in rec["searches"] if s["status"] == 200)
    return num, ok, len(rec["searches"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = yaml.safe_load((HERE / "src" / "litcheck-queries.yaml").read_text(encoding="utf-8"))
    code = data.pop("code", {})
    want = sys.argv[1:] or sorted(data, key=int)
    with ThreadPoolExecutor(8) as ex:
        for num, ok, n in ex.map(lambda k: run_problem(k, data[k], code.get(k)), want):
            print(f"problem {int(num):2d}: {ok}/{n} searches answered", flush=True)
    write_summary()


def write_summary():
    """out/litcheck/SUMMARY.md from every record (also after tools/litcheck_retry.py)"""
    data = yaml.safe_load((HERE / "src" / "litcheck-queries.yaml").read_text(encoding="utf-8"))
    data.pop("code", {})
    lines = [f"# Literature-check record ({TODAY}; generated by tools/litcheck.py)", ""]
    for k in sorted(data, key=int):
        f = OUT / f"{int(k):02d}.json"
        if not f.exists():
            continue
        rec = json.loads(f.read_text(encoding="utf-8"))
        lines.append(f"## Problem {int(k)}")
        for s in rec["searches"]:
            again = f", run again {s['retried']}" if s.get("retried") else ""
            lines.append(f"- **{s['source']}** “{s['query']}” (HTTP {s['status']}{again})")
            for r in s["results"][:6]:
                if "error" in r:
                    lines.append(f"  - error: {r['error']}")
                elif "path" in r:
                    lines.append(f"  - {r['path']}")
                else:
                    lines.append(f"  - {r.get('year')} · {r.get('title', '')[:150]} · {', '.join(a for a in r.get('authors', []) if a)[:70]} · {r.get('id')}")
        lines.append("")
    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("SUMMARY.md written")


if __name__ == "__main__":
    main()
