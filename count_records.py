import gzip
from pathlib import Path
from google.transit import gtfs_realtime_pb2

f = sorted(Path("raw_polls").glob("*.pb.gz"))[-1]
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(gzip.decompress(f.read_bytes()))

entities = len(feed.entity)
trip_updates = 0
stu_total = 0
stu_counts = []

for e in feed.entity:
    if e.HasField("trip_update"):
        trip_updates += 1
        n = len(e.trip_update.stop_time_update)
        stu_total += n
        stu_counts.append(n)

stu_counts.sort()
print(f"file: {f.name}")
print(f"entities: {entities:,}")
print(f"trip_updates: {trip_updates:,}")
print(f"stop_time_updates total: {stu_total:,}")
if stu_counts:
    print(f"per trip - min {stu_counts[0]}, median {stu_counts[len(stu_counts)//2]}, max {stu_counts[-1]}")