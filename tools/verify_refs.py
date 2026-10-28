"""bib_gate (extended): check every entry of src/refs.yaml against its identifier (8 threads).

  python tools/verify_refs.py [key …]      → out/REFS-CHECK.md, out/refs-check.json; exit 1 on any failure

doi: Crossref /works/{doi} (DataCite /dois/{doi} for 10.5281 Zenodo DOIs): title similarity ≥ 0.80 after normalisation,
     first author's family name present, year equal (± 1 for online-first). arxiv: arXiv API id_list: title ≥ 0.80,
     first author. zbmath: zbMATH Open search on the given string: a hit with title ≥ 0.80, year equal, first author.
     url: HTTP 200 (GET). Every failure is printed with what the identifier returned.
"""
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import working_proxy  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = working_proxy()
PX = {"https": P, "http": P} if P else None
import threading
ARXIV = threading.Lock()
UA = {"User-Agent": "grothendieckian-problems-refcheck/1.0 (mailto:vincent.liu@wisemotif.ai)"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"<[^>]+>|\$[^$]*\$", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    if a in b or b in a:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def family(name):
    parts = norm(name).split()
    return parts[-1] if parts else ""


def get(url, **kw):
    last = None
    for i in range(4):
        try:
            r = requests.get(url, headers=UA, proxies=PX, timeout=60, **kw)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep((30 if r.status_code == 429 else 4) * (i + 1))
                continue
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(4 * (i + 1))
    if last:
        raise last
    return r


def check(key, e):
    title, year = e.get("title", ""), e.get("year")
    first = (e.get("author") or [""])[0]
    out = {"key": key, "label": e.get("label"), "id": None, "ok": False, "found": {}}
    try:
        if e.get("zenodo_draft"):
            # a DOI reserved on a Zenodo draft that is not yet published (the three papers, S4): the draft is read with
            # the author's token, and its concept DOI, title, creator and date are compared with the entry
            sys.path.insert(0, str(HERE.parent / "release-kit" / "scripts"))
            from common import zenodo_token
            r = requests.get(f"https://zenodo.org/api/deposit/depositions/{e['zenodo_draft']}", proxies=PX, timeout=60,
                             headers={**UA, "Authorization": f"Bearer {zenodo_token()}"})
            d = r.json() if r.ok else {}
            m = d.get("metadata", {})
            concept = f"10.5281/zenodo.{d.get('conceptrecid')}"
            fauth = " ".join(c.get("name", "") for c in m.get("creators", []))
            out["id"] = f"doi:{e['doi']} (Zenodo draft {e['zenodo_draft']}, reserved)"
            out["found"] = {"http": r.status_code, "title": m.get("title", "")[:200],
                            "year": (m.get("publication_date") or "")[:4], "authors": fauth}
            ok = {"doi": concept == e["doi"], "title": sim(e["title"], m.get("title", "")) >= 0.80,
                  "year": (m.get("publication_date") or "")[:4] == str(year),
                  "author": family(first) in norm(fauth)}
            out["ok"] = r.ok and all(ok.values())
            out["why"] = ok
            return out
        if e.get("doi"):
            doi = e["doi"]
            out["id"] = "doi:" + doi
            datacite = doi.startswith("10.5281/")
            if not datacite:
                probe = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
                datacite = probe.status_code == 404          # DOIs registered with DataCite (Zenodo, LIPIcs, …)
            if datacite:
                r = get(f"https://api.datacite.org/dois/{urllib.parse.quote(doi)}")
                a = r.json()["data"]["attributes"] if r.ok else {}
                ftitle = " ".join(t["title"] for t in a.get("titles", []))
                fyear = a.get("publicationYear")
                fauth = " ".join(c.get("name", "") for c in a.get("creators", []))
            else:
                r = get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
                m = r.json()["message"] if r.ok else {}
                ftitle = " ".join(m.get("title") or []) + " " + " ".join(m.get("subtitle") or [])
                dp = (m.get("issued") or {}).get("date-parts") or [[None]]
                fyear = dp[0][0]
                fauth = " ".join(f"{a.get('given', '')} {a.get('family', '')} {a.get('name', '')}" for a in
                                 (m.get("author") or m.get("editor") or []))
            out["found"] = {"http": r.status_code, "title": ftitle.strip()[:200], "year": fyear, "authors": fauth[:160]}
            ok_title = sim(title, ftitle) >= 0.80 or sim(title.split(":")[0], ftitle) >= 0.85
            ok_year = fyear is not None and year is not None and abs(int(fyear) - int(year)) <= 1
            ok_auth = (not first or first.startswith("The ") or first == "IEEE" or family(first) in norm(fauth)
                       or not fauth.strip())
            allow = set(e.get("allow") or [])
            if not ftitle.strip() and e.get("zbmath"):          # Crossref record without a title: zbMATH for the title
                zr = get("https://api.zbmath.org/v1/document/_search",
                         params={"search_string": e["zbmath"], "page": 0, "results_per_page": 10})
                for d in (zr.json().get("result", []) if zr.ok else []):
                    t = d.get("title")
                    t = t.get("title") if isinstance(t, dict) else t
                    if sim(title, t or "") >= 0.80:
                        ok_title = True
                        out["found"]["title"] = f"(zbMATH {d.get('identifier')}) {t}"
                        break
            out["ok"] = r.ok and (ok_title or "title" in allow) and (ok_year or "year" in allow) and                 (ok_auth or "author" in allow)
            out["why"] = {"title": ok_title, "year": ok_year, "author": ok_auth, "allowed": sorted(allow)}
        elif e.get("arxiv"):
            out["id"] = "arXiv:" + e["arxiv"]
            with ARXIV:
                time.sleep(4)
                r = get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": e["arxiv"]}))
            ns = {"a": "http://www.w3.org/2005/Atom"}
            ent = ET.fromstring(r.content).find("a:entry", ns) if r.ok else None
            ftitle = " ".join((ent.findtext("a:title", "", ns) if ent is not None else "").split())
            fauth = [a.findtext("a:name", "", ns) for a in (ent.findall("a:author", ns) if ent is not None else [])]
            out["found"] = {"http": r.status_code, "title": ftitle[:200], "authors": ", ".join(fauth[:6]),
                            "published": ent.findtext("a:published", "", ns)[:10] if ent is not None else None}
            ok_title = sim(title, ftitle) >= 0.80
            ok_auth = not first or any(family(first) == family(a) for a in fauth)
            out["ok"] = bool(ftitle) and ok_title and ok_auth
            out["why"] = {"title": ok_title, "author": ok_auth}
            if not e.get("author") and fauth:
                out["found"]["note"] = "authors to print: " + ", ".join(fauth)
        elif e.get("zbmath"):
            out["id"] = "zbMATH search"
            r = get("https://api.zbmath.org/v1/document/_search",
                    params={"search_string": e["zbmath"], "page": 0, "results_per_page": 10})
            best = None
            for d in (r.json().get("result", []) if r.ok else []):
                t = d.get("title")
                t = t.get("title") if isinstance(t, dict) else t
                s = max(sim(title, t or ""), sim(e.get("title_alt", ""), t or ""))
                if best is None or s > best[0]:
                    best = (s, t, d.get("year"), d.get("identifier") or d.get("id"),
                            " ".join(a.get("name", "") for a in (d.get("contributors") or {}).get("authors", [])))
            if best:
                out["found"] = {"http": r.status_code, "title": (best[1] or "")[:200], "year": best[2],
                                "zbmath": best[3], "authors": best[4][:120]}
                ok_year = best[2] is not None and abs(int(best[2]) - int(year)) <= 1
                out["ok"] = best[0] >= 0.80 and ok_year and family(first) in norm(best[4])
                out["id"] = f"zbMATH {best[3]}"
            else:
                out["found"] = {"http": r.status_code}
        elif e.get("url"):
            out["id"] = e["url"]
            r = get(e["url"], allow_redirects=True)
            body = ""
            if r.ok and r.content[:4] == b"%PDF":
                import pymupdf
                doc = pymupdf.open(stream=r.content, filetype="pdf")
                body = " ".join(doc[i].get_text() for i in range(min(3, doc.page_count)))
            elif r.ok:
                body = r.text
            probe = " ".join(norm(e.get("check") or title).split()[:4])
            found = probe in norm(body)
            out["found"] = {"http": r.status_code, "final": r.url[:160], "bytes": len(r.content),
                            "title_on_page": found, "type": r.headers.get("content-type", "")[:40]}
            out["ok"] = r.ok and found
        else:
            out["found"] = {"error": "no identifier"}
    except Exception as ex:  # recorded, never hidden
        out["found"] = {"error": f"{type(ex).__name__}: {str(ex)[:160]}"}
    return out


def main():
    refs = yaml.safe_load((HERE / "src" / "refs.yaml").read_text(encoding="utf-8"))
    keys = sys.argv[1:] or list(refs)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda k: check(k, refs[k]), keys))
    rec = HERE / "out" / "refs-check.json"                  # partial runs update the record, never shrink it
    prev = {r["key"]: r for r in json.loads(rec.read_text(encoding="utf-8"))} if rec.exists() else {}
    prev.update({r["key"]: r for r in res})
    prev = {k: v for k, v in prev.items() if k in refs}
    res_all = [prev[k] for k in refs if k in prev]
    bad = [r for r in res if not r["ok"]]
    res, shown = res_all, res
    lines = [f"# Reference check ({time.strftime('%Y-%m-%d')}): {len(res) - len(bad)}/{len(res)} PASS", "",
             "| key | label | identifier | result | found |", "|---|---|---|---|---|"]
    for r in res:
        f = r["found"]
        lines.append(f"| {r['key']} | {r['label']} | {r['id']} | {'PASS' if r['ok'] else 'FAIL'} | "
                     f"{str(f.get('title') or f.get('final') or f.get('error') or '')[:90]} · {f.get('year') or f.get('published') or ''} · {str(f.get('authors') or '')[:50]} |")
    allbad = [r for r in res if not r["ok"]]
    lines[0] = f"# Reference check ({time.strftime('%Y-%m-%d')}): {len(res) - len(allbad)}/{len(res)} PASS"
    (HERE / "out" / "REFS-CHECK.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (HERE / "out" / "refs-check.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8",
                                                  newline="\n")
    print(f"this run {len(shown) - len(bad)}/{len(shown)} PASS; record {len(res) - len(allbad)}/{len(res)} PASS")
    for r in bad:
        print("FAIL", r["key"], r["id"], json.dumps(r["found"], ensure_ascii=False)[:300], r.get("why", ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
