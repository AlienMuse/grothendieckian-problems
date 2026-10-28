"""S1: extract every open item the seven works mark as open, conditional, conjectural, an obligation or a problem
(read-only; source = the page-text and statement-heading caches of the sealed PDFs, master/tools/pdf_cache.py).

  python tools/extract_candidates.py   → candidates/pool.json, candidates/POOL-S0N.md, counts on stdout

Each work marks status in its own notation (runbook §1 rule 2: quote it as the work prints it):
  S01  heading "— Status C." / "(O)" etc.: E established, S synthesis, D definition, R research construction,
       C conjecture, O obligation, Q disputed (Vol. III, Ch. 5, §5.3); text "Open problem", "Research Problem"
  S02  "(T …)", "(D …)", "(M …)", "(X)"; open items "Open Problem 2.14.A … (OPEN)"; Conjecture, Hypothesis, Question
  S03  Problem, Conjecture, Obstruction; text "Open Problem N"; tags [E] [T] [C] in the body
  S04–S06  bracketed tags [ KNOWN ] [ NEW ] [ REPROVED ] [ CONDITIONAL ] [ OPEN ] [ DISPUTED ]
  S07  [ ESTABLISHED ] [ DESIGN ] [ THEOREM ] [ CONJECTURE ] [ FORMAL TARGET ]
A candidate records: work, kind, number, heading, status as printed, page index and printed folio, the page's running
header, and the statement text (to the next statement or section heading, across one page break, ≤ 2,400 chars).
Classical named conjectures stated as background are kept but flagged `classical` (rule 3: not problems).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import CORPUS  # noqa: E402
OUT = HERE / "candidates"

KINDS = ("Definition|Theorem|Proposition|Lemma|Corollary|Conjecture|Problem|Open Problem|Open problem|Research Problem|"
         "Open Question|Question|Hypothesis|Claim|Obstruction|Criterion|Principle|Axiom|Algorithm|Example|Remark|"
         "Construction|Counterexample|Warning|Scholium|Exercise|Observation|Protocol|Procedure|Figure|Table|Plate|"
         "Falsifier|Obligation")
START = re.compile(rf"^(?:{KINDS})\s+[A-Z0-9][\w.\-]*")
SECTION = re.compile(r"^\d+(?:\.\d+)+\s+[A-Z]")
TEXT_OPEN = re.compile(r"^(Open Problem|Open problem|Research Problem|Open Question|Question)\s+([A-Z0-9][\w.\-]*[\w])\b(.*)$")
TAG = re.compile(r"\[\s*(KNOWN|NEW|REPROVED|CONDITIONAL|OPEN|DISPUTED|ESTABLISHED|DESIGN|THEOREM|CONJECTURE|FORMAL TARGET)"
                 r"\s*(?::[^\]]*)?\]")
CLASSICAL = re.compile(
    r"(Riemann|Lindel|Birch|Swinnerton|Hodge conjecture|\babc\b|Masser|Oesterl|Szpiro|Vojta|Langlands|Selberg|Lefschetz|"
    r"standard conjecture|Tate conjecture|Beilinson|Bloch|Kato|Artin|Ramanujan|Montgomery|Deligne|Grothendieck–Katz|"
    r"Shafarevich|Hilbert|Lehmer|Goldbach|twin prime|Mordell|Fontaine|Gross|Zagier|Hasse|Weil|Serre|Sato|Iwasawa|"
    r"Generalized Riemann|GRH|Global reciprocity|Functoriality|Ramanujan–Petersson|Elliott|Chowla|Cramér|Pair correlation)",
    re.I)


def status_of(label, heading, body):
    if label == "S01":
        m = re.search(r"Status ([A-Z](?:/[A-Z])?)\b", heading) or re.search(r"\(([ESDRCOQ](?:/[A-Z])?)(?:,[^)]*)?\)", heading)
        return m.group(1) if m else ""
    if label == "S02":
        m = re.search(r"\((OPEN(?: / [A-Z])?)\)", body[:2400]) or re.search(r"\(([TDMX](?:/[A-Z])*|UNDETERMINED|SUPERSEDED)"
                                                                            r"(?:,[^)]*)?\)", heading)
        return m.group(1) if m else ""
    if label == "S03":
        m = re.search(r"\[([ETCO])\]", heading + " " + body[:400])
        return m.group(1) if m else ""
    tags = TAG.findall(heading) or TAG.findall(body[:300])
    return " / ".join(dict.fromkeys(tags))


def selected(label, kind, status, heading):
    k = kind.lower()
    if label == "S01":
        return status in ("C", "O", "R", "Q", "D/O") or k in ("conjecture",) or "open" in k or "question" in k
    if label == "S02":
        return (status.startswith("OPEN") or status in ("X", "UNDETERMINED") or k in ("conjecture", "hypothesis", "question")
                or "open" in k or "conditional" in heading.lower())
    if label == "S03":
        return k in ("problem", "conjecture", "obstruction", "open problem", "question") or status in ("C", "O")
    if label in ("S04", "S05", "S06"):
        return (any(t in status for t in ("OPEN", "CONDITIONAL", "DISPUTED"))
                or k in ("problem", "conjecture", "obstruction", "question", "open problem"))
    return ("CONJECTURE" in status or "FORMAL TARGET" in status or k in ("conjecture", "problem", "question", "open problem"))


def body_from(pages, idx, needle):
    """Statement text from `needle` on page idx to the next statement / section heading, across one page break."""
    text = pages[idx]
    pos = text.find(needle)
    if pos < 0:
        pos = 0
    lines = text[pos:].split("\n")
    if idx + 1 < len(pages):
        nxt = pages[idx + 1].split("\n")[1:]                  # drop the next page's running header
        lines += nxt
    out, n = [], 0
    for i, line in enumerate(lines):
        s = line.strip()
        if i > 0 and (START.match(s) or SECTION.match(s)):
            break
        if re.fullmatch(r"[0-9ivxlc]{1,6}", s):             # a folio line
            continue
        out.append(s)
        n += len(s) + 1
        if n > 2400:
            break
    return " ".join(x for x in out if x)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pool = []
    for label in [f"S0{i}" for i in range(1, 8)]:
        pg = json.loads((CORPUS / f"{label}.pages.json").read_text(encoding="utf-8"))
        pages, labels = pg["pages"], pg["labels"]
        heads = json.loads((CORPUS / f"{label}.heads.json").read_text(encoding="utf-8"))["heads"]
        seen = set()
        for page, kind, number, heading, first in heads:
            idx = page - 1 if 0 < page <= len(pages) and heading.split(" (")[0][:20] not in pages[page - 1] \
                and heading.split(" (")[0][:20] in pages[page - 2] else page
            idx = min(max(idx, 0), len(pages) - 1)
            if heading.split(" ")[0] not in pages[idx]:
                for j in (idx - 1, idx + 1):
                    if 0 <= j < len(pages) and f"{kind} {number}" in pages[j]:
                        idx = j
                        break
            body = body_from(pages, idx, f"{kind} {number}")
            status = status_of(label, heading, body)
            if not selected(label, kind, status, heading):
                continue
            seen.add((kind.lower(), number))
            pool.append(dict(work=label, kind=kind, number=number, heading=heading.strip(), status=status, page_index=idx,
                             folio=labels[idx] if idx < len(labels) else "", running=pages[idx].split("\n")[0][:160],
                             classical=bool(CLASSICAL.search(heading)), text=body, source="heading"))
        for idx, text in enumerate(pages):
            for line in text.split("\n"):
                m = TEXT_OPEN.match(line.strip())
                if not m or (m.group(1).lower(), m.group(2)) in seen:
                    continue
                kind, number = m.group(1), m.group(2)
                seen.add((kind.lower(), number))
                body = body_from(pages, idx, f"{kind} {number}")
                status = status_of(label, line, body)
                pool.append(dict(work=label, kind=kind, number=number, heading=line.strip()[:200], status=status,
                                 page_index=idx, folio=labels[idx] if idx < len(labels) else "",
                                 running=text.split("\n")[0][:160], classical=bool(CLASSICAL.search(line)), text=body,
                                 source="text"))
    for i, c in enumerate(pool, 1):
        c["id"] = f"{c['work']}-{i:04d}"
    (OUT / "pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    for label in sorted({c["work"] for c in pool}):
        items = [c for c in pool if c["work"] == label]
        md = [f"# Candidate pool — {label} ({len(items)} items; generated by tools/extract_candidates.py)", ""]
        for c in items:
            md += [f"## {c['id']} · {c['kind']} {c['number']} · status `{c['status'] or '-'}` · p. {c['folio']}"
                   f"{' · CLASSICAL' if c['classical'] else ''}", "", f"*{c['running']}*", "", c["text"], ""]
        (OUT / f"POOL-{label}.md").write_text("\n".join(md), encoding="utf-8", newline="\n")
    print("pool:", len(pool))
    for label in sorted({c["work"] for c in pool}):
        items = [c for c in pool if c["work"] == label]
        print(f"  {label}: {len(items):4d}  classical {sum(c['classical'] for c in items):3d}  kinds "
              + ", ".join(f"{k} {v}" for k, v in Counter(c["kind"] for c in items).most_common(6))
              + "  | status " + ", ".join(f"{k or '-'} {v}" for k, v in Counter(c["status"] for c in items).most_common(6)))


if __name__ == "__main__":
    main()
