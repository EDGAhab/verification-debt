#!/usr/bin/env python3
"""Daily snapshot of the VibeMathed public dataset (CC BY 4.0, attribute VibeMathed)."""
import hashlib
import json
import pathlib
import sys
import time
import urllib.request
from datetime import datetime, timezone

URL = "https://vibemathed.com/api/dataset"
OUT = pathlib.Path(__file__).resolve().parent / "snapshots"
UA = "verification-debt-research (contact: fffeilian@gmail.com)"


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # network or HTTP error
            if attempt == 2:
                sys.exit(f"fetch failed: {e}")
            time.sleep(30)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    raw = fetch()
    data = json.loads(raw)  # stop loudly if the response is not JSON
    digest = hashlib.sha256(raw).hexdigest()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    (OUT / f"{stamp}.json").write_bytes(raw)
    with open(OUT / "index.csv", "a", encoding="utf-8") as f:
        f.write(f"{stamp},{data.get('generated')},{data.get('count')},{digest}\n")
    print(stamp, data.get("count"), digest[:12])


if __name__ == "__main__":
    main()
