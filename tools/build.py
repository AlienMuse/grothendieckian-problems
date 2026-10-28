"""Build one of the two papers: Markdown (src/<paper>/*.md in ORDER.txt order, metadata.yaml) → Pandoc 3.9.0.2 +
filters/rs.lua → LaTeX (styles/rs-template.tex, amsart) → PDF (LuaHBTeX 1.21.0, TeX Live 2025).

  python tools/build.py paper-I [--name X] [--passes 3]      → out/<X>.pdf, out/work/<paper>/<X>.log

Executables by absolute path (on Windows a bare name resolves on the parent PATH: Series 02, 2026-10-22); every build
starts from clean .aux/.out files (Series 06); the engine line of the log must name TeX Live 2025.
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SERIES = HERE.parent.parent
PANDOC = Path(os.environ.get("GP_PANDOC") or SERIES / "01 Grothendieckian Machine" / "master-tools" / "pandoc-3.9.0.2" / "pandoc.exe")
TEXLIVE = Path(os.environ["GP_TEXLIVE"]) if os.environ.get("GP_TEXLIVE") else Path(__import__("json").loads((HERE / "local.json").read_text(encoding="utf-8"))["texlive"])
EPOCH = "1792886400"                     # 2026-10-25T00:00:00Z, as Series 00 (reproducible PDF dates)
FROM = ("markdown+tex_math_dollars+fenced_divs+bracketed_spans+pipe_tables+footnotes+raw_tex+smart"
        "+link_attributes+header_attributes+yaml_metadata_block")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def run(cmd, **kw):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    return r, time.time() - t0


def main():
    paper = sys.argv[1]
    src = HERE / "src" / paper
    name = arg("--name", paper)
    passes = int(arg("--passes", "3"))
    work = HERE / "out" / "work" / paper
    work.mkdir(parents=True, exist_ok=True)
    order = [l.strip() for l in (src / "ORDER.txt").read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    missing = [f for f in order if not (src / f).exists()]
    if missing:
        sys.exit(f"ORDER.txt names files that do not exist: {missing}")
    for p in list(work.glob("*.aux")) + list(work.glob("*.out")):
        p.unlink()
    env = dict(os.environ, PATH=str(TEXLIVE) + os.pathsep + os.environ["PATH"], SOURCE_DATE_EPOCH=EPOCH,
               FORCE_SOURCE_DATE="1", TZ="UTC", TEXINPUTS=f"{HERE / 'styles'};{HERE / 'figures'};{src};")
    tex = work / f"{name}.tex"
    cmd = [str(PANDOC), f"--from={FROM}", "--lua-filter", str(HERE / "filters" / "rs.lua"),
           "--metadata-file", str(src / "metadata.yaml"), "--template", str(HERE / "styles" / "rs-template.tex"),
           "--number-sections", "--wrap=none", "--to=latex", "--standalone", "-o", str(tex),
           *[str(src / f) for f in order]]
    r, t = run(cmd, cwd=src, env=env)
    (work / f"{name}.pandoc.log").write_text(r.stderr, encoding="utf-8")
    rep = re.search(r"\[rs\.lua\] .*", r.stderr)
    print(f"pandoc: rc={r.returncode} {t:.0f} s; {rep.group(0) if rep else 'no filter report'}")
    for w in [l for l in r.stderr.splitlines() if l.strip() and not l.startswith("[rs.lua]")][:10]:
        print("   ", w[:200])
    if r.returncode or not tex.exists():
        sys.exit(1)
    for i in range(passes):
        r, t = run([str(TEXLIVE / "lualatex.exe"), "--interaction=nonstopmode", "--halt-on-error",
                    f"--jobname={name}", tex.name], cwd=work, env=env)
        log = (work / f"{name}.log").read_text(encoding="utf-8", errors="replace")
        pages = re.search(r"Output written on .*?\((\d+) pages?", log)
        print(f"lualatex pass {i + 1}: rc={r.returncode} {t:.0f} s, pages {pages.group(1) if pages else '?'}")
        err = re.findall(r"(?m)^! .*(?:\n.*){0,3}", log)
        if err:
            print("   first TeX error:", err[0][:400])
        if r.returncode:
            sys.exit(1)
    log = (work / f"{name}.log").read_text(encoding="utf-8", errors="replace")
    over = [float(x) for x in re.findall(r"Overfull \\hbox \((\d+\.\d+)pt too wide\)", log)]
    miss = sorted(set(re.findall(r"Missing character: There is no (.+?) in font", log)))
    undef = sorted(set(re.findall(r"Reference `([^']+)' on page \d+ undefined", log)))
    engine = log.splitlines()[0] if log else "?"
    print(f"overfull hbox: {len(over)} (max {max(over) if over else 0:.1f} pt) | missing glyphs: {len(miss)} {miss[:6]}"
          f" | undefined refs: {len(undef)} {undef[:6]}")
    print(f"engine: {engine}")
    if "(TeX Live 2025)" not in engine:
        sys.exit("engine is not the pinned TeX Live 2025")
    pdf = work / f"{name}.pdf"
    out = HERE / "out" / f"{name}.pdf"
    pdf.replace(out)
    print(f"→ out/{out.name}")


if __name__ == "__main__":
    main()
