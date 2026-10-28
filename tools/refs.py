"""Citations and reference list for the two papers, from src/refs.yaml (single source).

  import refs; refs.cite_text(text) → text with [@key, loc; @key2] replaced by [Label, loc; Label2]
  refs.used(texts) → keys cited;  refs.reference_list(keys) → Markdown fenced div {.references}, AMS style, sorted by label

Unknown keys raise KeyError (the build stops: bib_gate). Only entries that passed tools/verify_refs.py
(out/refs-check.json) may be printed; the build checks this as well.
"""
import json
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
REFS = yaml.safe_load((HERE / "src" / "refs.yaml").read_text(encoding="utf-8"))
CITE = re.compile(r"\[(@[^\[\]]+)\]")


def _one(item):
    item = item.strip()
    m = re.match(r"@([A-Za-z0-9_]+)\s*(?:,\s*(.*))?$", item)
    if not m:
        raise ValueError(f"bad citation item: {item!r}")
    key, loc = m.group(1), m.group(2)
    if key not in REFS:
        raise KeyError(f"unknown reference key: {key}")
    return key, loc


def cite_text(text):
    def rep(m):
        parts = [_one(x) for x in m.group(1).split(";")]
        return "[" + "; ".join(REFS[k]["label"] + (f", {loc}" if loc else "") for k, loc in parts) + "]"
    return CITE.sub(rep, text)


def used(texts):
    keys = []
    for t in texts:
        for m in CITE.finditer(t):
            for x in m.group(1).split(";"):
                k, _ = _one(x)
                if k not in keys:
                    keys.append(k)
    return keys


def verified():
    f = HERE / "out" / "refs-check.json"
    ok = set()
    if f.exists():
        for r in json.loads(f.read_text(encoding="utf-8")):
            if r["ok"]:
                ok.add(r["key"])
    return ok


def _names(lst):
    lst = [a for a in (lst or []) if a]
    if len(lst) <= 2:
        return " and ".join(lst)
    return ", ".join(lst[:-1]) + ", and " + lst[-1]


def entry(key):
    e = REFS[key]
    au = _names(e.get("author"))
    t = e["title"]
    if e["type"] in ("book",):
        s = f"{au}, *{t}*"
        if e.get("edition"):
            s += f", {e['edition']} ed."
        if e.get("series"):
            s += f", {e['series']}"
        s += f", {e.get('publisher', '')}" + (f", {e['address']}" if e.get("address") else "") + f", {e['year']}"
    elif e["type"] == "article":
        s = f"{au}, *{t}*, {e['journal']}"
        if e.get("volume"):
            s += f" **{e['volume']}**"
        s += f" ({e['year']})"
        if e.get("number"):
            s += f", no. {e['number']}"
        if e.get("pages"):
            s += f", {e['pages']}"
    elif e["type"] in ("incollection", "inproceedings"):
        s = f"{au}, *{t}*, {e['booktitle']}"
        if e.get("editor"):
            s += f" ({_names(e['editor'])}, eds.)"
        if e.get("series"):
            s += f", {e['series']}"
        if e.get("publisher"):
            s += f", {e['publisher']}"
        s += f", {e['year']}"
        if e.get("pages"):
            s += f", pp. {e['pages']}"
    else:
        s = (f"{au}, " if au else "") + f"*{t}*"
        if e.get("arxiv") and not e.get("doi"):
            s += ", preprint"
        if e.get("year"):
            s += f", {e['year']}"
    if e.get("note"):
        s += f", {e['note']}"
    if e.get("doi"):
        s += f", doi:[{e['doi']}](https://doi.org/{e['doi']})"
    elif e.get("arxiv"):
        s += f", arXiv:[{e['arxiv']}](https://arxiv.org/abs/{e['arxiv']})"
    elif e.get("url"):
        s += f", <{e['url']}>"
    return f"[{e['label']}] {s}."


def reference_list(keys):
    ok = verified()
    bad = [k for k in keys if k not in ok]
    if bad:
        raise RuntimeError(f"references not verified by tools/verify_refs.py: {bad}")
    keys = sorted(keys, key=lambda k: (not REFS[k]["label"].startswith("S0"), REFS[k]["label"].lower()))
    return "::: references\n" + "\n\n".join(entry(k) for k in keys) + "\n:::\n"
