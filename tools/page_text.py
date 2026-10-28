"""Print the text of printed pages of a sealed work (read-only), with running header and folio.

  python tools/page_text.py S02 viii 21 22 … [--chars 6000]
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import CORPUS  # noqa: E402


def main():
    label, args = sys.argv[1], sys.argv[2:]
    cap = int(args[args.index("--chars") + 1]) if "--chars" in args else 6000
    folios = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--chars")]
    d = json.loads((CORPUS / f"{label}.pages.json").read_text(encoding="utf-8"))
    for f in folios:
        idxs = [i for i, l in enumerate(d["labels"]) if l == f]
        if not idxs:
            print(f"#### {label} p. {f}: NOT FOUND\n")
            continue
        i = idxs[0]
        print(f"#### {label} p. {f} (idx {i})")
        print(d["pages"][i].replace("\n", " ")[:cap])
        print()


if __name__ == "__main__":
    main()
