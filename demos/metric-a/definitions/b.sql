-- B: customers subscribed AT ANY POINT in the last 12 months
--    (started before the window but not cancelled before it counts);
--    gaps between consecutive uses inside the window, pooled over all events.
WITH win AS (
  SELECT TIMESTAMP '2025-10-01' AS lo, TIMESTAMP '2026-10-01' AS hi
), cohort AS (
  SELECT customer_id FROM 'data/subscriptions.parquet', win
  WHERE subscribed_at < hi AND coalesce(cancelled_at, hi) >= lo
), gaps AS (
  SELECT date_diff('second', lag(event_at) OVER w, event_at) / 86400.0 AS gap
  FROM 'data/usage_events.parquet' e JOIN cohort USING (customer_id), win
  WHERE event_at >= lo AND event_at < hi
  WINDOW w AS (PARTITION BY e.customer_id ORDER BY event_at)
)
SELECT avg(gap) AS value FROM gaps WHERE gap IS NOT NULL;
