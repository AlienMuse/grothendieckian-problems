"""Paths and network settings shared by the published scripts, so that they run both in the project and in the
public repository.

CORPUS: the page-text cache of the sealed PDFs of the seven works (one JSON file per work, written by pdf_cache.py).
In the project it is master/out/work/corpus; elsewhere set GP_CORPUS to the directory that pdf_cache.py wrote.
working_proxy(): the project's proxy detection when available, else the HTTPS_PROXY environment variable.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
_default = HERE.parent / "master" / "out" / "work" / "corpus"
CORPUS = Path(os.environ.get("GP_CORPUS") or (_default if _default.exists() else HERE / "corpus"))


def working_proxy():
    kit = HERE.parent / "release-kit" / "scripts"
    if kit.exists():
        import sys
        sys.path.insert(0, str(kit))
        try:
            from common import working_proxy as wp
            return wp()
        except Exception:
            pass
    return os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
