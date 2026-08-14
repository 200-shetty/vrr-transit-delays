import time, requests, hashlib, logging, gzip
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("raw_polls")
OUT.mkdir(exist_ok=True)
logging.basicConfig(filename="archive.log", level=logging.INFO,
                    format="%(asctime)s %(message)s")

RETAIN_HOURS = 6

last = None
while True:
    t0 = time.time()
    try:
        r = requests.get("https://realtime.gtfs.de/realtime-free.pb", timeout=45)
        r.raise_for_status()
        h = hashlib.md5(r.content).hexdigest()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = OUT / f"feed_{stamp}.pb.gz"
        path.write_bytes(gzip.compress(r.content))
        logging.info("ok bytes=%d gz=%d changed=%s",
                     len(r.content), path.stat().st_size, h != last)
        last = h
    except Exception as e:
        logging.error("fail %s", e)

    cutoff = time.time() - RETAIN_HOURS * 3600
    removed = 0
    for old in OUT.glob("*.pb.gz"):
        if old.stat().st_mtime < cutoff:
            old.unlink()
            removed += 1
    if removed:
        logging.info("pruned %d files", removed)

    time.sleep(max(0, 60 - (time.time() - t0)))