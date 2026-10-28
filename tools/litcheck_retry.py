"""Run again, slowly, the searches of out/litcheck/NN.json that a source refused (HTTP 429, 5xx) and write the answers
into the same record (read-only on the sources; the record keeps the date of each retry).

  python tools/litcheck_retry.py 15 16 17 [--source arXiv] [--wait 12]

arXiv throttles a client that has sent many requests: the retry waits --wait seconds between requests (default 12,
four times what arXiv asks) and tries each search up to four times, doubling the wait after a refusal.
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import litcheck  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "out" / "litcheck"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    nums = [a for a in sys.argv[1:] if a.isdigit() and not sys.argv[sys.argv.index(a) - 1].startswith("--")]
    source, wait = arg("--source", "arXiv"), float(arg("--wait", "12"))
    for n in nums:
        p = OUT / f"{int(n):02d}.json"
        rec = json.loads(p.read_text(encoding="utf-8"))
        for s in rec["searches"]:
            if s["source"] != source or s["status"] == 200:
                continue
            delay = wait
            for attempt in range(4):
                time.sleep(delay)
                status, results = litcheck.SOURCES[source](s["query"])
                print(f"problem {n}: {source} “{s['query'][:50]}” attempt {attempt + 1}: {status}, {len(results)} results")
                if status == 200:
                    s.update(status=200, results=results, retried=dt.date.today().isoformat())
                    break
                delay *= 2
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    litcheck.write_summary()


if __name__ == "__main__":
    main()
