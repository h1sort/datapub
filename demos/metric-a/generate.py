# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "polars", "pyarrow"]
# ///
"""Synthetic Linear-like project-management SaaS: subscriptions + usage events.

Deterministic (fixed seed). Writes Parquet to ./data/.
"""
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl

SEED = 2026_10_21
N = 640
START = datetime(2024, 1, 1)
END = datetime(2026, 9, 30, 23, 59)  # data ends at the cutoff
OUT = Path(__file__).parent / "data"

rng = np.random.default_rng(SEED)
span_days = (END - START).days

# Personas: (name, share, sessions/day while "on", mean events per session)
PERSONAS = {
    "power": (0.14, 0.90, 5.0),     # bursty heavy users, many issues per sitting
    "regular": (0.36, 0.30, 2.0),
    "sporadic": (0.50, 0.035, 1.3),  # a few uses a month
}
PLANS = ["free-trial-converted", "starter", "team", "business"]
names = list(PERSONAS)
shares = [PERSONAS[k][0] for k in names]

subs, events = [], []
for cid in range(1, N + 1):
    # signups grow over time (SaaS growth): density increasing in t
    t = span_days * np.sqrt(rng.uniform())
    start = START + timedelta(days=float(t), hours=float(rng.uniform(8, 19)))
    persona = rng.choice(names, p=shares)
    _, rate, burst = PERSONAS[persona]
    plan = rng.choice(PLANS, p=[0.15, 0.4, 0.3, 0.15])

    # churn: sporadic users churn fastest; hazard per day
    hazard = {"power": 1 / 1500, "regular": 1 / 700, "sporadic": 1 / 220}[persona]
    life = rng.exponential(1 / hazard)
    cancelled = start + timedelta(days=float(life))
    if cancelled > END:
        cancelled = None
    stop = min(cancelled or END, END)

    # usage decays with tenure (novelty wears off) and has on/off phases
    day = 0.0
    horizon = (stop - start).total_seconds() / 86400
    while True:
        tenure = day
        decay = 0.45 + 0.55 * np.exp(-tenure / 120.0)  # new customers are keener
        lam = rate * decay
        day += rng.exponential(1 / lam)
        if day >= horizon:
            break
        # weekdays only, mostly
        ts = start + timedelta(days=day)
        if ts.weekday() >= 5 and rng.uniform() < 0.8:
            continue
        # a session = a burst of events minutes apart
        k = 1 + rng.poisson(burst - 1)
        offs = np.cumsum(rng.exponential(12, size=k))  # minutes
        for o in offs:
            e = ts + timedelta(minutes=float(o))
            if e <= stop:
                events.append((cid, e))
        # dormant stretches for non-power users
        if persona != "power" and rng.uniform() < 0.06:
            day += rng.uniform(20, 70)
    subs.append((cid, plan, start, cancelled))

OUT.mkdir(exist_ok=True)
sub_df = pl.DataFrame(
    subs, schema=["customer_id", "plan", "subscribed_at", "cancelled_at"], orient="row"
).with_columns(pl.col("subscribed_at").dt.cast_time_unit("us"), pl.col("cancelled_at").dt.cast_time_unit("us"))
ev_df = pl.DataFrame(events, schema=["customer_id", "event_at"], orient="row").sort("customer_id", "event_at")
sub_df.write_parquet(OUT / "subscriptions.parquet", compression="zstd")
ev_df.write_parquet(OUT / "usage_events.parquet", compression="zstd")
print(f"subscriptions: {sub_df.height} rows, usage_events: {ev_df.height} rows")
