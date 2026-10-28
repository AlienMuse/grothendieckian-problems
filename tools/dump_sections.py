"""Dump the text of named sections of a sealed work (read-only), from the section heading to the next numbered section.

  python tools/dump_sections.py S01 "5.1" "13.35" … [--from PAGEIDX --to PAGEIDX] > out.txt

A section is found by its heading line "N.M Title" (first occurrence inside the page window); the text runs across
page breaks (running headers and folio lines dropped) until the next heading "N.M' Title" or "N+1.1 Title".
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import CORPUS  # noqa: E402
HEAD = re.compile(r"^(\d+(?:\.\d+)+)\s+[A-Z]")


def main():
    label, args = sys.argv[1], sys.argv[2:]
    lo = int(args[args.index("--from") + 1]) if "--from" in args else 0
    hi = int(args[args.index("--to") + 1]) if "--to" in args else None
    want = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--from", "--to"))]
    d = json.loads((CORPUS / f"{label}.pages.json").read_text(encoding="utf-8"))
    pages, labels = d["pages"], d["labels"]
    hi = hi or len(pages)
    stream = []                                   # (page index, line)
    for i in range(lo, hi):
        lines = pages[i].split("\n")[1:]
        stream += [(i, s.strip()) for s in lines if s.strip() and not re.fullmatch(r"[0-9ivxlc]{1,6}", s.strip())]
    for sec in want:
        start = next((k for k, (_, s) in enumerate(stream) if HEAD.match(s) and HEAD.match(s).group(1) == sec), None)
        if start is None:
            print(f"#### {label} §{sec}: NOT FOUND\n")
            continue
        out = [stream[start][1]]
        for k in range(start + 1, min(start + 400, len(stream))):
            m = HEAD.match(stream[k][1])
            if m and m.group(1) != sec and not m.group(1).startswith(sec + "."):
                break
            out.append(stream[k][1])
        i0 = stream[start][0]
        print(f"#### {label} §{sec} · p. {labels[i0]} (page index {i0})")
        print(" ".join(out)[:6000])
        print()


if __name__ == "__main__":
    main()
