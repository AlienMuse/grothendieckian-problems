"""lean_gate: the Lean statements build against the pinned Mathlib, use no axiom beyond Lean's standard three and
`sorryAx`, and every Lean file belongs to a formalization card (runbook §6).

  python tools/lean_gate.py      → out/LEAN-GATE.md; exit 1 on failure
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
FORMAL = HERE / "formal"
BIN = Path(os.environ["USERPROFILE"]) / ".elan" / "bin"
STANDARD = {"propext", "Classical.choice", "Quot.sound", "sorryAx"}
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def lake(*args, cwd=FORMAL):
    env = dict(os.environ, PATH=str(BIN) + os.pathsep + os.environ["PATH"])
    return subprocess.run([str(BIN / "lake.exe"), *args], cwd=cwd, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def main():
    rows, fails = [], 0
    r = lake("build")
    ok = r.returncode == 0
    errors = [l for l in (r.stdout + r.stderr).splitlines() if re.search(r"\berror\b", l)]
    rows.append(("lake build", ok and not errors, f"rc {r.returncode}; errors {len(errors)}"))
    files = sorted((FORMAL / "GrothendieckianProblems").glob("P*.lean"))
    cards = []
    for f in sorted((HERE / "src" / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    formal_nums = {c["num"] for c in cards if c["kind"] == "formal"}
    for f in files:
        num = int(re.match(r"P(\d+)", f.stem).group(1))
        rows.append((f"{f.name} belongs to a formalization card", num in formal_nums, f"Problem {num}"))
        src = f.read_text(encoding="utf-8")
        ns = re.search(r"namespace (\S+)", src).group(1)
        names = re.findall(r"(?m)^theorem\s+(\S+)", src)
        if re.search(r"(?m)^\s*axiom\s", src):
            rows.append((f"{f.name}: no new axioms", False, "an `axiom` declaration is present"))
        check = FORMAL / "_axioms_check.lean"
        check.write_text(f"import GrothendieckianProblems.{f.stem}\nopen {ns}\n" +
                         "".join(f"#print axioms {ns}.{n}\n" for n in names), encoding="utf-8", newline="\n")
        a = lake("env", "lean", check.name)
        check.unlink()
        used = set(re.findall(r"\b(propext|Classical\.choice|Quot\.sound|sorryAx|[A-Za-z_][\w.]*)\b(?=[,\]])",
                              a.stdout))
        reported = re.findall(r"depends on axioms: \[([^\]]*)\]", a.stdout)
        axioms = {x.strip() for line in reported for x in line.split(",") if x.strip()}
        extra = sorted(axioms - STANDARD)
        rows.append((f"{f.name}: axioms", a.returncode == 0 and len(reported) == len(names) and not extra,
                     f"{len(names)} theorems; axioms used {sorted(axioms)}; outside the standard set {extra or 0}"))
        sorrys = len(re.findall(r"\bsorry\b", src))
        rows.append((f"{f.name}: open statements", True, f"{sorrys} `sorry` (the problem is to remove them)"))
    toolchain = (FORMAL / "lean-toolchain").read_text().strip()
    import json
    pkgs = json.loads((FORMAL / "lake-manifest.json").read_text(encoding="utf-8"))["packages"]
    rev = next(p["rev"] for p in pkgs if p["name"] == "mathlib")
    lines = ["# Lean gate", "", f"Toolchain `{toolchain}`; Mathlib `{rev[:12]}` (pinned in lakefile.toml).", "",
             "| check | result | detail |", "|---|---|---|"]
    for name, ok, detail in rows:
        fails += 0 if ok else 1
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines.append(f"\n**{'ALL PASS' if not fails else f'{fails} FAIL'}**")
    (HERE / "out" / "LEAN-GATE.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
