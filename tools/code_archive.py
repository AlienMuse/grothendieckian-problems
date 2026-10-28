"""The code archive of the three papers (author 2026-10-28, option A, as the companion code of Series 06 and 07): the
repository at the signed tag v1.0.0, without the three PDFs (they are in the records themselves), as one zip for the
Zenodo record of The 57 Grothendieckian Problems.

  python tools/code_archive.py build      verify the tag's signature; `git archive` of the tag → dist/<ZIP>;
                                          every file of the zip compared with the tag's tree (git blob hash);
                                          LICENSE, LICENSE-CODE and NOTICE present → dist/CODE-ARCHIVE.json
  python tools/code_archive.py verify     the same checks on the existing zip (read-only)

The zip is not in SHA256SUMS (sealed earlier over the three PDFs). Its integrity rests on the signed tag: anyone can
check out v1.0.0, verify the tag, and compare the files of the zip with it; its SHA-256 is printed in the record.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE / "repo"
DIST = HERE / "dist"
TAG = "v1.0.0"
ZIP = "grothendieckian-problems-v1.0.0-code.zip"
PREFIX = "grothendieckian-problems-v1.0.0/"
EXCLUDE = ":(exclude)papers/*.pdf"
MUST = ["LICENSE", "LICENSE-CODE", "NOTICE", "README.md", "formal/LICENSE", "formal/lakefile.toml", "problems.json",
        "tools/build.py", "figures/web/lib.js"]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def git(*a, check=True):
    r = subprocess.run(["git", *a], cwd=REPO, capture_output=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(a[:3])}: {(r.stderr or r.stdout).decode(errors='replace')[:600]}")
    return r


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check(path: Path) -> dict:
    v = git("tag", "-v", TAG, check=False)
    if "Good signature" not in v.stderr.decode(errors="replace"):
        sys.exit(f"tag {TAG}: no good signature")
    commit = git("rev-parse", f"{TAG}^{{commit}}").stdout.decode().strip()
    tree = {}
    for line in git("ls-tree", "-r", TAG).stdout.decode("utf-8").splitlines():
        meta, p = line.split("\t", 1)
        if not (p.startswith("papers/") and p.endswith(".pdf")):
            tree[p] = meta.split()[2]
    with zipfile.ZipFile(path) as z:
        files = {i.filename[len(PREFIX):]: z.read(i) for i in z.infolist() if not i.is_dir()}
        comment = z.comment.decode(errors="replace")
    bad = [p for p in tree if p not in files or blob(files[p]) != tree[p]]
    extra = [p for p in files if p not in tree]
    missing = [m for m in MUST if m not in files]
    if bad or extra or missing or commit not in comment:
        sys.exit(f"archive check failed: differ {bad[:5]}, extra {extra[:5]}, missing {missing}, "
                 f"commit in zip comment {commit in comment}")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    rec = {"file": path.name, "sha256": sha, "size": path.stat().st_size, "files": len(files), "tag": TAG,
           "commit": commit, "excluded": "papers/*.pdf (in the Zenodo records themselves)"}
    print(f"{path.name}: {rec['size'] / 2**20:.1f} MiB, {len(files)} files = the tree of {TAG} ({commit[:7]}, signature "
          f"good) without the three PDFs; LICENSE, LICENSE-CODE, NOTICE present; SHA-256 {sha}")
    return rec


def build():
    out = DIST / ZIP
    if out.exists():
        out.unlink()
    r = subprocess.run(["git", "archive", "--format=zip", f"--prefix={PREFIX}", "-o", str(out), TAG, "--", ".", EXCLUDE],
                       cwd=REPO, capture_output=True)
    if r.returncode:
        sys.exit(r.stderr.decode(errors="replace"))
    rec = check(out)
    (DIST / "CODE-ARCHIVE.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")


def verify():
    rec = json.loads((DIST / "CODE-ARCHIVE.json").read_text(encoding="utf-8"))
    now = check(DIST / ZIP)
    if now["sha256"] != rec["sha256"]:
        sys.exit("the zip changed since it was built")
    print("RESULT: PASS")


if __name__ == "__main__":
    {"build": build, "verify": verify}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
