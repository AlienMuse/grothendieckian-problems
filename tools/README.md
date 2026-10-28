# Scripts

The scripts that produced and checked the two papers. They read the page text of the sealed PDFs of the seven works:
download the PDFs from Zenodo (DOIs in the papers), extract their page text with `pdf_cache.py`, and set `GP_CORPUS` to
the directory it writes. The single sources of the papers are in `src/`; the records of the checks are in `data/`.

| Script | Role |
|---|---|
| `extract_candidates.py` | candidate open items, by each work's status notation |
| `find_phrases.py`, `page_text.py`, `dump_sections.py` | locate passages and read pages |
| `litcheck.py` | literature check (arXiv, OpenAlex, zbMATH Open, Crossref, GitHub code search) → `data/litcheck/` |
| `verify_refs.py`, `complete_refs.py` | every reference against its DOI, arXiv id, zbMATH record or page → `data/REFS-CHECK.md` |
| `quote_gate.py` | every quotation against the page it cites → `data/QUOTE-GATE.md` |
| `paper_gates.py`, `lean_gate.py` | the remaining gates of the papers → `data/PAPER-GATES.md`, `data/LEAN-GATE.md` |
| `render_paper1.py`, `render_paper2.py`, `build_repo.py` | generate the papers' Markdown and this repository from `src/` |

The papers are typeset with Pandoc 3.9 and LuaHBTeX (TeX Live 2025) using `styles/` and `filters/`.

Licence: Apache-2.0 ([`../LICENSE-CODE`](../LICENSE-CODE)), as `styles/`, `filters/`, `formal/` and `figures/web/`.
