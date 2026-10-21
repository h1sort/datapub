-- A: subscription STARTED in the 12 months before the cutoff;
--    mean over customers of each customer's average gap between consecutive uses.
WITH cohort AS (
  SELECT customer_id FROM 'data/subscriptions.parquet'
  WHERE subscribed_at >= TIMESTAMP '2025-10-01'
    AND subscribed_at <  TIMESTAMP '2026-10-01'
), gaps AS (
  SELECT e.customer_id,
         date_diff('second', lag(event_at) OVER w, event_at) / 86400.0 AS gap
  FROM 'data/usage_events.parquet' e JOIN cohort USING (customer_id)
  WHERE event_at < TIMESTAMP '2026-10-01'
  WINDOW w AS (PARTITION BY e.customer_id ORDER BY event_at)
), per_customer AS (
  SELECT customer_id, avg(gap) AS avg_gap FROM gaps
  WHERE gap IS NOT NULL GROUP BY 1
)
SELECT avg(avg_gap) AS value FROM per_customer;
