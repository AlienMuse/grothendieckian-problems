"""Read back from Zenodo the records the overview paper and its Figure 3 print (read-only): for each of the eight
works, the concept DOI resolves, the latest version is 1.0.0, the publication date is the one printed, the licence is
CC BY-NC-ND 4.0, the record is in the community grothendieckian-programme and its creator carries the ORCID iD.

  python tools/zenodo_facts.py      → out/ZENODO-FACTS.md; exit 1 on a difference
"""
import json
import sys
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).resolve().parents[1]
SERIES = HERE.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portable import working_proxy  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ORCID = "0009-0000-8718-222X"


def main():
    prog = yaml.safe_load((SERIES / "programme.yaml").read_text(encoding="utf-8"))
    st = json.loads((SERIES / "release-kit" / "state.json").read_text(encoding="utf-8"))
    want = [("00", st["zenodo_concept_doi"], st["publication_date"])] + \
           [(w["series"], w["concept_doi"], w["publication_date"]) for w in prog["facts"]["works"]]
    p = working_proxy()
    px = {"http": p, "https": p} if p else None
    rows, bad = [], 0
    for series, doi, date in want:
        rid = doi.split(".")[-1]
        r = requests.get(f"https://zenodo.org/api/records/{rid}", proxies=px, timeout=60,
                         headers={"User-Agent": "grothendieckian-problems facts (mailto:vincent.liu@wisemotif.ai)"})
        j = r.json()
        m = j.get("metadata", {})
        comms = [c.get("id") or c.get("slug") or c for c in (m.get("communities") or [])]
        checks = {"concept DOI": j.get("conceptdoi") == doi, "version 1.0.0": str(m.get("version", "")).startswith("1.0.0"),   # printed "1.0.0 (Research Architecture Edition 1)"
                  f"date {date}": m.get("publication_date") == date,
                  "CC BY-NC-ND 4.0": (m.get("license") or {}).get("id", "").lower() == "cc-by-nc-nd-4.0",
                  "community": any("grothendieckian-programme" in str(c) for c in comms),
                  "ORCID": any(c.get("orcid") == ORCID for c in m.get("creators", []))}
        ok = all(checks.values())
        bad += 0 if ok else 1
        rows.append(f"| {series} | {doi} | {m.get('publication_date')} | {m.get('version')} | "
                    + " · ".join(f"{k} {'✓' if v else '✗'}" for k, v in checks.items()) + " |")
    out = ["# Zenodo read-back for the overview paper", "", "| Series | concept DOI | date | version | checks |",
           "|---|---|---|---|---|"] + rows + ["", f"**{'ALL PASS' if not bad else f'{bad} FAIL'}**"]
    (HERE / "out" / "ZENODO-FACTS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
