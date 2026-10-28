"""Editorial pass on src/refs.yaml: complete author lists and years from the identifiers (arXiv API; Crossref and
DataCite for DOIs), and report every entry whose printed authors differ from the record. Rewrites only the `author`
and `year` fields of arXiv-only entries; DOI entries are reported for review, not changed.

  python tools/complete_refs.py [--apply]
"""
import re
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import working_proxy  # noqa: E402

P = working_proxy()
PX = {"https": P, "http": P} if P else None
UA = {"User-Agent": "grothendieckian-problems-refcheck/1.0 (mailto:vincent.liu@wisemotif.ai)"}
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def fam(n):
    n = unicodedata.normalize("NFKD", n)
    n = "".join(c for c in n if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z]", "", n.split()[-1]) if n.split() else ""


def main():
    apply = "--apply" in sys.argv
    path = HERE / "src" / "refs.yaml"
    refs = yaml.safe_load(path.read_text(encoding="utf-8"))
    text = path.read_text(encoding="utf-8")
    arx = {k: v["arxiv"] for k, v in refs.items() if v.get("arxiv")}
    r = requests.get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": ",".join(arx.values()), "max_results": 100}), proxies=PX, headers=UA, timeout=120)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    meta = {}
    for e in ET.fromstring(r.content).findall("a:entry", ns):
        aid = re.sub(r"v\d+$", "", e.findtext("a:id", "", ns).split("/abs/")[-1])
        meta[aid] = (int(e.findtext("a:published", "", ns)[:4]), [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)])
    changes = []
    for k, a in arx.items():
        y, au = meta[a]
        mine = refs[k].get("author") or []
        if [fam(x) for x in mine] != [fam(x) for x in au]:
            changes.append((k, "author", mine, au))
        if refs[k].get("type") == "misc" and refs[k].get("year") != y:
            changes.append((k, "year", refs[k].get("year"), y))
    for k, v in refs.items():
        if v.get("doi") and not v["doi"].startswith("10.5281/"):
            time.sleep(0.2)
            rr = requests.get(f"https://api.crossref.org/works/{urllib.parse.quote(v['doi'])}", proxies=PX, headers=UA, timeout=60)
            if not rr.ok:
                continue
            au = [f"{x.get('given', '')} {x.get('family', '')}".strip() for x in rr.json()["message"].get("author", [])]
            mine = v.get("author") or []
            if au and [fam(x) for x in mine] != [fam(x) for x in au]:
                print(f"REVIEW {k}: printed {len(mine)} {mine[:4]} | Crossref {len(au)} {au[:6]}")
    for k, field, old, new in changes:
        print(f"CHANGE {k}.{field}: {old} -> {new}")
        if apply:
            line = next(l for l in text.split("\n") if l.startswith(f"{k}:"))
            if field == "author":
                q = ", ".join('"' + x.replace('"', "'") + '"' for x in new)
                nl = re.sub(r'author: \[[^\]]*\]', f"author: [{q}]", line) if "author:" in line else \
                    line.replace("type: misc,", f"type: misc, author: [{q}],")
            else:
                nl = re.sub(r"year: \d{4}", f"year: {new}", line) if "year:" in line else line.replace(", arxiv:", f", year: {new}, arxiv:")
            text = text.replace(line, nl)
    if apply:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("applied", len(changes))


if __name__ == "__main__":
    main()
