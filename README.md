**Goal**

Build a system that detects trips heading toward a late arrival while there is still time to act, and explains why, so that a transit operations team can intervene or inform passengers before the delay becomes the passenger's problem.

The engineering goal underneath it: demonstrate a **production-shaped pipeline** where a **streaming path** and a **batch path** serve one semantic model, and where the streaming path's accuracy is measured.

**Business question**

**Primary:**

**Can we identify trips likely to arrive late at their remaining stops, early enough for operations to act, and can we quantify how much warning we actually provide?**

**Supporting questions the system answers:**

**Which routes, stops and time windows** are systematically unreliable, controlling for conditions?
When a vehicle is late at stop N, does the delay **grow, hold or recover** by stop N+k, and what predicts which?
How much **lead time** do we provide before a trip's delay crosses a threshold that matters?
What fraction of late arrivals do we **catch**, and how many **false alarms** does that cost?

Question 3 and 4 are the ones that make this a data engineering project rather than a dashboard.

**Possible outcomes**

**Primary artifact:** a measured claim of the form:

**Of trips that arrived more than 5 minutes late, the system flagged X% at least N minutes before the delay materialised, at a false positive rate of Y%.**

That single sentence is what you lead the README with and what you say in an interview. Every architectural decision exists to make it defensible.

**Secondary artifacts:**

**Live at-risk trip queue**, refreshed continuously, ranked by severity and remaining intervention window
**Delay propagation view:** pick a trip, see delay grow or recover across its stop sequence
**Route and stop reliability rankings** with baselines that account for hour, weekday and holiday
**A documented feed reliability report:** uptime, staleness, coverage by operator, and what fraction of operators send real predictions versus schedule echoes

**Outcomes that would also count as success:**

**Finding that the feed is too sparse or too optimistic** to support useful prediction, documented with evidence. *A negative result you measured beats a positive result you assumed.* This is genuinely a valid outcome and you should say so upfront, because it removes the incentive to fudge.

**In scope**

**Domain**

**VRR network (Rhein-Ruhr)**, configurable via bounding box and agency allowlist
**All modes present in the feed:** bus, tram, U-Bahn, S-Bahn, regional rail
**Arrival delay at scheduled stops** as the unit of analysis

**Technical**

**Continuous ingestion of GTFS-RT** with raw immutable archival
**Weekly static GTFS ingestion** with slowly-changing-dimension handling
**Stateful stream processing:** dedup, watermarking, per-trip state, threshold detection
**Bronze and silver** in an open table format on object storage
**Gold marts in Snowflake via dbt**, with tests and docs
**Batch reconciliation** of streaming predictions against confirmed outcomes
**Orchestration of the batch path**, with the streaming path running independently
**A public, clickable dashboard**
**Documented handling of:** out-of-order events, source outages, schema changes, backfill and reprocessing
**Holiday and school-term enrichment** for baseline correction

**Explicitly a deliverable, not a footnote:** the reliability and coverage report for the source feed. It's the artifact that proves you engaged with the data rather than the tools.
