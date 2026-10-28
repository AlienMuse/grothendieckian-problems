"""The thirteen figures as 600 ppi PNG for the repository and its README (author 2026-10-29: "用 600ppi 的高清版本呈现").

  python tools/figures_png.py      → figures/png600/fig-<id>.png (3119 px across the 132 mm measure) and MANIFEST.json

Each PNG is the figure's PDF rasterised at 600 ppi: the light layer (rendered at 605 ppi) at its own resolution, the
vector text and lines sharp at that resolution; lossless. A PNG is made again only when its PDF changed (the
manifest keeps the SHA-256 of each PDF). Eight processes at most.
"""
from __future__ import annotations

import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "figures"
OUT = SRC / "png600"
PPI = 600
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def one(pdf: str) -> dict:
    import pymupdf
    from PIL import Image
    p = Path(pdf)
    with pymupdf.open(p) as d:
        pm = d[0].get_pixmap(dpi=PPI)
        w_mm = d[0].rect.width / 72 * 25.4
    im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    dst = OUT / p.with_suffix(".png").name
    im.save(dst, optimize=True, dpi=(PPI, PPI))
    return {"pdf": p.name, "pdf_sha256": sha(p), "png": dst.name, "px": list(im.size),
            "ppi": round(im.size[0] / (w_mm / 25.4)), "bytes": dst.stat().st_size}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    man_p = OUT / "MANIFEST.json"
    man = {e["pdf"]: e for e in json.loads(man_p.read_text(encoding="utf-8"))} if man_p.exists() else {}
    pdfs = sorted(SRC.glob("fig-*.pdf"))
    todo = [str(p) for p in pdfs if man.get(p.name, {}).get("pdf_sha256") != sha(p) or not (OUT / p.with_suffix(".png").name).exists()]
    with ProcessPoolExecutor(max_workers=min(8, max(1, len(todo)))) as ex:
        for e in ex.map(one, todo):
            man[e["pdf"]] = e
            print(f"  {e['png']}: {e['px'][0]} × {e['px'][1]} px, {e['ppi']} ppi, {e['bytes'] / 2**20:.1f} MiB")
    man = {k: v for k, v in man.items() if (SRC / k).exists()}
    man_p.write_text(json.dumps(sorted(man.values(), key=lambda e: e["pdf"]), indent=1) + "\n", encoding="utf-8")
    low = [e["png"] for e in man.values() if e["ppi"] < PPI]
    print(f"{len(man)} figures at ≥ {PPI} ppi; {len(todo)} rendered now" + (f"; BELOW {PPI} ppi: {low}" if low else ""))
    sys.exit(1 if low or len(man) != len(pdfs) else 0)


if __name__ == "__main__":
    main()
