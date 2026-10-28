"""Page text of the seven sealed works, cached once (runbook steps 1.4 and 2.1; §1 rule 2: the PDFs are only read).

  python tools/pdf_cache.py [S01 …]    → out/work/corpus/S0N.pages.json  ({"pdf", "sha256", "pages": [text, …]})

The text of each page as MuPDF extracts it (reading order, ligatures expanded), with the page label the book prints
(labels.json alongside: printed folio per page). A cache is reused while the sealed file's SHA-256 is unchanged.
8 worker processes; a large book is split into page ranges across them.
"""
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIES_ROOT = ROOT.parent.parent
OUT = ROOT / "out" / "work" / "corpus"
WORKS = {
    "S01": "01 Grothendieckian Machine", "S02": "02 Topos Native Intelligence", "S03": "03 Arithmetic Spectral Descent",
    "S04": "04 Fractured Adelic Geometry", "S05": "05 The Archimedean Prism", "S06": "06 Strained Prismatic Geometry",
    "S07": "07 The Arithmetic Topos",
}
WORKERS = 8
CHUNK = 400


def sealed(label: str) -> Path:
    return next((SERIES_ROOT / WORKS[label] / "release-kit" / "dist").glob("*-Complete.pdf"))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 22):
            h.update(b)
    return h.hexdigest()


def extract(job):
    path, a, b = job
    import pymupdf
    d = pymupdf.open(path)
    out = [(i, d[i].get_text(flags=pymupdf.TEXT_DEHYPHENATE | pymupdf.TEXT_PRESERVE_WHITESPACE), d[i].get_label())
           for i in range(a, b)]
    d.close()
    return out


HEAD_KINDS = ("Theorem|Proposition|Lemma|Corollary|Definition|Conjecture|Algorithm|Figure|Plate|Table|Example|Remark|"
              "Axiom|Principle|Construction|Problem|Observation|Criterion|Exercise|Notation|Hypothesis|Protocol|"
              "Procedure|Question|Obstruction|Claim|Counterexample|Scholium|Warning|Experiment|Programme")
HEAD = __import__("re").compile(rf"^({HEAD_KINDS})\s+([A-Z]{{0,2}}-?\d+(?:[.\-]\d+)*[a-z]?|[A-Z](?:\.\d+)+)\b")


def heads_of(job):
    """bold line openings "Kind number" (statement heads, caption labels): the first bold run of a line, so a
    reference in running text (regular weight) is never counted"""
    path, a, b = job
    import pymupdf
    d = pymupdf.open(path)
    out = []
    kind_only = __import__("re").compile(rf"^({HEAD_KINDS})$")
    for i in range(a, b):
        pending = ""                                   # a bold kind alone at a line end: "Theorem" / "33.37 (…)"
        for blk in d[i].get_text("dict", flags=pymupdf.TEXT_DEHYPHENATE)["blocks"]:
            for line in blk.get("lines", []):
                # spans may be single words with the spaces as spans of their own (Series 07): keep the spaces,
                # stop at the first non-bold span that carries text
                spans = line["spans"]
                if not any(s["text"].strip() for s in spans):
                    continue
                bold = []
                for s in spans:
                    if not s["text"].strip() or s["flags"] & 16 or "Bold" in s["font"] or "bold" in s["font"]:
                        bold.append(s["text"])
                    else:
                        break
                text = "".join(bold).strip()
                if pending and text:
                    text, pending = pending + " " + text, ""
                elif kind_only.match(text) and len(text) == len("".join(s["text"] for s in spans).strip()):
                    pending = text
                    continue
                else:
                    pending = ""
                m = HEAD.match(text)
                if m:
                    rest = "".join(s["text"] for s in spans)[len("".join(bold)):][:60].strip()
                    out.append([i, m.group(1), m.group(2), text[:80], rest])
    d.close()
    return out


def heads(label: str) -> list:
    """[(page index, kind, number, bold text, what follows)] of one work"""
    p = OUT / f"{label}.heads.json"
    if not p.exists():
        build_heads([label])
    return json.loads(p.read_text(encoding="utf-8"))["heads"]


def build_heads(which):
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    jobs, meta = [], {}
    for label in which:
        pdf = sealed(label)
        digest = json.loads((OUT / f"{label}.pages.json").read_text(encoding="utf-8"))["sha256"] \
            if (OUT / f"{label}.pages.json").exists() else sha256(pdf)
        cache = OUT / f"{label}.heads.json"
        if cache.exists() and json.loads(cache.read_text(encoding="utf-8")).get("sha256") == digest:
            continue
        n = pymupdf.open(pdf).page_count
        meta[label] = (pdf, digest)
        jobs += [(label, (str(pdf), a, min(a + CHUNK // 2, n))) for a in range(0, n, CHUNK // 2)]
    res = {label: [] for label in meta}
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        for (label, _), part in zip(jobs, pool.map(heads_of, [j for _, j in jobs])):
            res[label] += part
    for label, (pdf, digest) in meta.items():
        (OUT / f"{label}.heads.json").write_text(json.dumps({"pdf": pdf.name, "sha256": digest, "heads": res[label]},
                                                            ensure_ascii=False), encoding="utf-8")
        print(f"{label}: {len(res[label])} bold heads")


def load(label: str) -> list[str]:
    """the cached page texts of one work (building the cache if needed)"""
    p = OUT / f"{label}.pages.json"
    if not p.exists():
        build([label])
    return json.loads(p.read_text(encoding="utf-8"))["pages"]


def labels(label: str) -> list[str]:
    p = OUT / f"{label}.pages.json"
    if not p.exists():
        build([label])
    return json.loads(p.read_text(encoding="utf-8"))["labels"]


def build(which):
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    jobs, meta = [], {}
    for label in which:
        pdf = sealed(label)
        digest = sha256(pdf)
        cache = OUT / f"{label}.pages.json"
        if cache.exists() and json.loads(cache.read_text(encoding="utf-8")).get("sha256") == digest:
            print(f"{label}: cache current")
            continue
        n = pymupdf.open(pdf).page_count
        meta[label] = (pdf, digest, n)
        jobs += [(label, (str(pdf), a, min(a + CHUNK, n))) for a in range(0, n, CHUNK)]
    if not jobs:
        return
    res = {label: [None] * meta[label][2] for label in meta}
    labs = {label: [None] * meta[label][2] for label in meta}
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        for (label, _), part in zip(jobs, pool.map(extract, [j for _, j in jobs])):
            for i, t, lab in part:
                res[label][i], labs[label][i] = t, lab
    for label, (pdf, digest, n) in meta.items():
        (OUT / f"{label}.pages.json").write_text(json.dumps(
            {"pdf": pdf.name, "sha256": digest, "pages": res[label], "labels": labs[label]}, ensure_ascii=False),
            encoding="utf-8")
        print(f"{label}: {n} pages cached ({sum(len(t) for t in res[label]):,} characters)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    which = [a for a in sys.argv[1:] if a in WORKS] or list(WORKS)
    build(which)
    build_heads(which)
