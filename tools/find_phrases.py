"""Locate phrases in the seven sealed works (read-only): printed page and a short context for each hit.

  python tools/find_phrases.py "phrase one" "phrase two" … [--works S01,S02] [--max 4]

Matching ignores case and collapses whitespace and line-break hyphenation, so a phrase split across lines is found.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import CORPUS  # noqa: E402


def norm(s):
    s = re.sub(r"-\n(?=[a-z])", "", s)
    return re.sub(r"\s+", " ", s).lower()


def main():
    args = sys.argv[1:]
    works = args[args.index("--works") + 1].split(",") if "--works" in args else [f"S0{i}" for i in range(1, 8)]
    cap = int(args[args.index("--max") + 1]) if "--max" in args else 4
    skip = {args.index(f) + 1 for f in ("--works", "--max") if f in args}
    phrases = [a for i, a in enumerate(args) if not a.startswith("--") and i not in skip]
    for label in works:
        d = json.loads((CORPUS / f"{label}.pages.json").read_text(encoding="utf-8"))
        texts = [norm(p) for p in d["pages"]]
        for ph in phrases:
            q = norm(ph)
            hits = [i for i, t in enumerate(texts) if q in t]
            if not hits:
                continue
            print(f"== {label} \"{ph}\": {len(hits)} page(s)")
            for i in hits[:cap]:
                t = texts[i]
                k = t.find(q)
                print(f"   p. {d['labels'][i]} (idx {i}) | {d['pages'][i].split(chr(10))[0][:70]} | …{t[max(0, k - 90):k + len(q) + 140]}…")


if __name__ == "__main__":
    main()
