"""quote_gate: every passage in curly quotation marks in a problem card (or a thesis) must occur verbatim on one of
the pages the card names, in the work the card names (read-only; sealed-PDF page text, master/tools/pdf_cache.py).

  python tools/quote_gate.py [src/problems/*.yaml] [--theses src/theses.yaml]   → out/QUOTE-GATE.md; exit 1 on failure

Matching: NFKC (mathematical italic letters become plain letters), lower case, and every character that is not a
letter or a digit removed on both sides — so line breaks, hyphenation, spaces and typographic punctuation do not
matter, while every letter and digit must agree in order. A quote is looked for on the named pages and on the next
page (a sentence may cross a page break). Quotes nested inside a quote (“…“base change”…”) are part of the outer
quote. Single words or very short fragments (fewer than 12 letters and digits) are not checked.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import CORPUS  # noqa: E402
FIELDS = ("statement", "established", "solved", "proposer", "status")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def key(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return "".join(c for c in s if c.isalnum())


def quotes(text):
    """Outermost “…” spans, allowing one level of nesting."""
    out, depth, start = [], 0, None
    for i, c in enumerate(text):
        if c == "“":
            if depth == 0:
                start = i + 1
            depth += 1
        elif c == "”" and depth:
            depth -= 1
            if depth == 0:
                out.append(text[start:i])
    return out


_cache = {}


def JACKSON():
    """Text of A. Jackson, Notices AMS 51 (2004), part II, as downloaded to out/sources/ (see runbook §8)."""
    if "jackson" not in _cache:
        import pymupdf
        d = pymupdf.open(HERE / "out" / "sources" / "jackson2004-part2.pdf")
        _cache["jackson"] = key(" ".join(p.get_text() for p in d))
    return _cache["jackson"]


def pages_of(work):
    if work not in _cache:
        d = json.loads((CORPUS / f"{work}.pages.json").read_text(encoding="utf-8"))

        def body(p):     # the page without its running header and folio, so that a quotation can cross a page break
            lines = p.split("\n")[1:]
            return "\n".join(l for l in lines if not re.fullmatch(r"\s*[0-9ivxlc]{1,6}\s*", l))
        _cache[work] = (d["labels"], [key(p) + "|" + key(body(p)) for p in d["pages"]])
    return _cache[work]


def check(work, folios, q):
    labels, keys = pages_of(work)
    k = key(q)
    if len(k) < 12:
        return "short"
    idxs = [i for i, l in enumerate(labels) if l in folios]
    later = None
    for i in idxs:
        full, body = keys[i].split("|")
        nxt = keys[i + 1].split("|")[1] if i + 1 < len(keys) else ""
        if k in full:
            return "ok"
        if k in body + nxt:
            # running on to the next page is allowed only if the quotation begins on the named page; a quotation that
            # lies wholly on the next page is a wrong page (2026-10-28: S02 §1.2.6 cited p. 22, the sentence is on p. 23)
            if k in nxt:
                later = labels[i + 1]
            else:
                return "ok"
    if later:
        return f"next page:{later}"
    anywhere = [labels[i] for i, t in enumerate(keys) if k in t]
    return "elsewhere:" + ",".join(anywhere[:4]) if anywhere else "missing"


def main():
    args = sys.argv[1:]
    files = [Path(a) for a in args if a.endswith(".yaml") and "theses" not in a] or \
        sorted((HERE / "src" / "problems").glob("*.yaml"))
    rows, bad, n = [], 0, 0
    for f in files:
        for card in yaml.safe_load(f.read_text(encoding="utf-8")):
            folios = set(card["pages"])
            for field in FIELDS:
                for q in quotes(str(card.get(field) or "")):
                    r = check(card["work"], folios, q)
                    if r == "short":
                        continue
                    n += 1
                    if r != "ok":
                        bad += 1
                        rows.append(f"| {card['num']} | {field} | {r} | {q[:110]} |")
    th = HERE / "src" / "theses.yaml"
    if th.exists():
        for t in yaml.safe_load(th.read_text(encoding="utf-8")):
            for ev in t.get("evidence", []):
                for q in quotes(ev["text"]):
                    r = check(ev["work"], set(ev["pages"]), q)
                    if r == "short":
                        continue
                    n += 1
                    if r != "ok":
                        bad += 1
                        rows.append(f"| T{t['num']} | evidence | {r} | {q[:110]} |")
    # hand-written paper text: a quotation is checked in the work of the first [@S0x …] citation within 160 characters
    # after it (on the cited page if the citation gives one, else anywhere in the work); quotations without such a
    # citation are listed for manual review (they quote third parties, whose sources are in src/refs.yaml).
    manual = []
    docs = sorted(f for f in (HERE / "src").glob("*/[0-9][0-9]-*.md") if f.parent.name in ("overview", "paper-I", "paper-II"))
    inst = HERE / "src" / "thesis-instances.yaml"
    if inst.exists():
        docs.append(inst)
    for md in docs:
        if md.name.endswith(".cited.md") or md.stem.split("-", 1)[1] in ("part1", "part2", "appendices", "references",
                                                                          "theses", "declarations"):
            continue
        text = md.read_text(encoding="utf-8")
        if md.suffix == ".yaml":
            text = "\n\n".join(" ".join(str(x).split()) for x in yaml.safe_load(text).values())
        pos = 0
        for qt in quotes(text):
            at = text.find(qt, pos)
            pos = at + len(qt)
            end = text.find("\n\n", pos)
            tail = text[pos:end if end > 0 else len(text)]                  # rest of the paragraph
            m = re.search(r"\[@(S0[1-7])([^\]]*)\]", tail)
            jk = re.search(r"\[@Jackson2004", tail)
            if jk and (not m or jk.start() < m.start()):
                if not (HERE / "out" / "sources" / "jackson2004-part2.pdf").exists():   # AMS PDF is not redistributed
                    manual.append(f"{md.parent.name}/{md.name}: “{qt[:90]}” (Jackson 2004: download the PDF to recheck)")
                    continue
                n += 1
                if key(qt) not in JACKSON():
                    bad += 1
                    rows.append(f"| {md.parent.name}/{md.name} | text | not in Jackson 2004 | {qt[:110]} |")
                continue
            if not m:
                if len(key(qt)) >= 12:
                    manual.append(f"{md.parent.name}/{md.name}: “{qt[:90]}”")
                continue
            work, loc = m.group(1), m.group(2)
            folios = set(re.findall(r"pp?\. ([0-9ivxlc]+)", loc))
            labels, _ = pages_of(work)
            r = check(work, folios or set(labels), qt)
            if r == "short":
                continue
            n += 1
            if r != "ok":
                bad += 1
                rows.append(f"| {md.parent.name}/{md.name} | text | {r} | {qt[:110]} |")
    head = [f"# quote_gate: {n - bad}/{n} quotations found verbatim on the named pages", ""]
    if manual:
        head += ["Quotations of third parties (checked by hand against src/refs.yaml sources):", ""] + \
                [f"- {m}" for m in manual] + [""]
    if rows:
        head += ["| card | field | result | quotation |", "|---|---|---|---|"] + rows
    (HERE / "out" / "QUOTE-GATE.md").write_text("\n".join(head) + "\n", encoding="utf-8", newline="\n")
    print(head[0])
    for r in rows:
        print(r)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
