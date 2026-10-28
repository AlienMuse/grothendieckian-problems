"""The banner of the repository and its social preview (author 2026-10-29: the series' banner, same specification),
rendered as the series banners are (Series 00, master/tools/web_assets.py: hero 240 × 90 mm → 2400 × 900 px; social
200 × 100 mm → 1280 × 640 px; the light layer at twice the output resolution, the vector HUD printed over it, the PDF
rasterised at the output size).

  python tools/banner.py           → repo/assets/hero.png (README), out/social-preview.png (the author uploads it:
                                     Settings → General → Social preview), out/banner-*.pdf; checks → out/BANNER-GATE.md

Data from the single sources: the cells (series, colour, the short name on each cover) from programme.yaml, the range
of problems of each work from the cards, the title block from the papers' metadata. Checks: output size; every line
fits, none collides; type ≥ 7 pt at design size; faces only Segoe UI and the TGP faces, no Type 3; every word of the
title block and of the cells found in the PDF text.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
# the specifications of the series (web_assets.py BANNERS: hero, social), unchanged
SPEC = {"hero": {"size_mm": [240.0, 90.0], "px": (2400, 900), "lift": -168.0, "fill": .93, "left": 9.0, "right": 5.0,
                 "gap": 10.0, "title_max": 44.0,
                 "stars": [[12, 6, .25], [96, 5, .2], [118, 86, .22], [40, 86, .2], [150, 4, .18]]},
        "social": {"size_mm": [200.0, 100.0], "px": (1280, 640), "lift": -176.0, "fill": .86, "left": 9.0, "right": 6.0,
                   "gap": 9.0, "title_max": 40.0,
                   "stars": [[10, 6, .25], [80, 5, .2], [96, 94, .22], [30, 95, .2], [125, 4, .18]]}}
# the hero is a source of the repository (build_repo.py copies it to repo/assets/hero.png); the social preview is
# uploaded by the author (Settings → General → Social preview)
DEST = {"hero": HERE / "figures" / "banner" / "hero.png", "social": HERE / "figures" / "banner" / "social-preview.png"}


def data(bid: str) -> dict:
    prog = yaml.safe_load(F.PROGRAMME.read_text(encoding="utf-8"))
    cards = []
    for f in sorted((HERE / "src" / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    cells = []
    for c in prog["cells"]:
        nums = sorted(x["num"] for x in cards if x["work"] == f"S{c['series']}")
        cells.append({"series": c["series"], "position": c["position"], "colour": c["colour"], "label": c["cover_role"],
                      "range": f"Problems {nums[0]}–{nums[-1]}"})
    m2 = yaml.safe_load((HERE / "src" / "paper-II" / "metadata.yaml").read_text(encoding="utf-8"))
    n_theses = len(yaml.safe_load((HERE / "src" / "theses.yaml").read_text(encoding="utf-8")))
    spec = SPEC[bid]
    return {"id": bid, "size_mm": spec["size_mm"], "lift": spec["lift"], "stars": spec["stars"],
            **{k: spec[k] for k in ("fill", "left", "right", "gap", "title_max")}, "cells": cells,
            "kicker": "THE GROTHENDIECKIAN PROGRAMME · THREE PAPERS",
            "title_lines": ["The 57 Grothendieckian", "Problems"],
            # the subtitle of paper II up to "from the Grothendieckian Programme", which the kicker names: one line at
            # the size of the series' banners in both sizes
            "subtitle": m2["subtitle"].split(" from the Grothendieckian Programme")[0],
            "edition_line": f"3 PAPERS · {n_theses} THESES · {len(cards)} PROBLEMS · VERSION 1.0",
            "author": "Vincent Liu", "imprint": "WiseMotif.ai"}


PAGE = F.PAGE.replace("fig-{fid}.js", "fig-hero.js")


def render(bid: str, port: int) -> list[str]:
    from PIL import Image, ImageStat
    import pikepdf
    import pymupdf
    spec, out = SPEC[bid], []
    w_mm, h_mm = spec["size_mm"]
    ppi = spec["px"][0] / (w_mm / 25.4)
    page = f"banner-{bid}"
    (F.WEB / f"data-{page}.json").write_text(json.dumps(data(bid), ensure_ascii=False, indent=1), encoding="utf-8")
    (F.WEB / f"{page}.html").write_text(PAGE.format(num=0, title="Banner", fid=page, w=w_mm, h=h_mm)
                                        .replace("fig-banner-", "fig-").replace(f"fig-{page}.js", "fig-hero.js"),
                                        encoding="utf-8")
    url = f"http://127.0.0.1:{port}/{page}.html"
    gl = F.WEB / f"gl-{page}.png"
    for budget in (60000, 180000):
        gl.unlink(missing_ok=True)
        r = F.chrome([f"--window-size={round(w_mm * F.CSS_PX_PER_MM)},{round(h_mm * F.CSS_PX_PER_MM)}",
                      f"--force-device-scale-factor={2 * ppi / 96}", f"--virtual-time-budget={budget}",
                      "--enable-logging=stderr", "--v=0", f"--screenshot={gl}", f"{url}?layer=gl"])
        errs = [l for l in r.stderr.splitlines() if "CONSOLE" in l and "rror" in l]
        if errs or not gl.exists():
            return [f"!! {bid}: light layer not rendered: {' | '.join(errs[:3]) or r.stderr[-300:]}"]
        st = ImageStat.Stat(Image.open(gl).convert("L").reduce(8))
        if 8 <= st.mean[0] <= 120 and st.stddev[0] >= 12:
            break
    else:
        return [f"!! {bid}: the light layer is empty"]
    for budget in (20000, 60000):
        r = F.chrome([f"--virtual-time-budget={budget}", "--dump-dom", f"{url}?layer=print"])
        if 'data-fit="' in r.stdout:
            break
    get = lambda k: json.loads(F.unescape(re.search(rf'data-{k}="([^"]*)"', r.stdout).group(1)))
    fit, lines, overlap = get("fit"), get("lines"), get("overlap")
    minpt = float(re.search(r'data-minpt="([^"]*)"', r.stdout).group(1))
    out += [f"!! {bid}: text does not fit: {f}" for f in fit] + [f"!! {bid}: lines collide: {o}" for o in overlap]
    if minpt < 7.0:
        out.append(f"!! {bid}: type {minpt:.2f} pt < 7 pt")
    tmp = F.WEB / f"{page}.tmp.pdf"
    for budget in (20000, 60000, 120000):
        tmp.unlink(missing_ok=True)
        F.chrome(["--no-pdf-header-footer", f"--virtual-time-budget={budget}", f"--print-to-pdf={tmp}", f"{url}?layer=print"])
        if tmp.exists():
            with pymupdf.open(tmp) as d:
                if d[0].get_image_info() and len(d[0].get_text().strip()) > 20:
                    break
    with pymupdf.open(tmp) as d:
        ib = pymupdf.Rect(d[0].get_image_info()[0]["bbox"])
    pdf = HERE / "out" / f"banner-{bid}.pdf"
    with pikepdf.open(tmp) as p:
        mb = [float(v) for v in p.pages[0].obj.MediaBox]
        p.pages[0].obj.MediaBox = pikepdf.Array([round(v, 4) for v in (mb[0] + ib.x0, mb[3] - ib.y1, mb[0] + ib.x1, mb[3] - ib.y0)])
        p.save(pdf)
    tmp.unlink()
    with pymupdf.open(pdf) as d:
        pg = d[0]
        fonts = pg.get_fonts()
        flat = "".join(pg.get_text().split())
        zoom = spec["px"][0] / pg.rect.width
        pm = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples).resize(spec["px"], Image.LANCZOS)
    if "Type3" in {f[2] for f in fonts}:
        out.append(f"!! {bid}: Type 3 font")
    stray = sorted({f[3] for f in fonts if not re.match(r"^[A-Z]{6}\+(SegoeUI|TGP)", f[3])})
    if stray:
        out.append(f"!! {bid}: faces {stray}")
    missing = [l for l in lines if "".join(l.split()) not in flat]
    if missing:
        out.append(f"!! {bid}: lines not in the PDF text: {missing[:3]}")
    DEST[bid].parent.mkdir(parents=True, exist_ok=True)
    im.save(DEST[bid], optimize=True)
    if im.size != spec["px"]:
        out.append(f"!! {bid}: {im.size} ≠ {spec['px']}")
    out.append(f"{bid}: {DEST[bid].relative_to(HERE).as_posix()} {im.size[0]} × {im.size[1]} px, "
               f"{DEST[bid].stat().st_size / 2**20:.2f} MiB; {len(lines)} lines, smallest type {minpt:.2f} pt; "
               f"faces {sorted({f[3].split('+')[-1] for f in fonts})}")
    return out


def main():
    F.sync_design()
    httpd, port = F.serve()
    try:
        report = render("hero", port) + render("social", port)
    finally:
        httpd.shutdown()
    fails = [l for l in report if l.startswith("!!")]
    head = f"# Banner gate: {'ALL PASS' if not fails else f'{len(fails)} FAIL'}"
    (HERE / "out" / "BANNER-GATE.md").write_text(head + "\n\n" + "\n".join(f"- {l}" for l in report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(head)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
