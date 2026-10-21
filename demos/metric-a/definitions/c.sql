-- C: "último año" = calendar 2025; customers who subscribed during 2025.
--    Per customer: days observed in 2025 / number of uses in 2025; then averaged.
WITH cohort AS (
  SELECT customer_id, subscribed_at,
         least(coalesce(cancelled_at, TIMESTAMP '2026-01-01'),
               TIMESTAMP '2026-01-01') AS ends
  FROM 'data/subscriptions.parquet'
  WHERE subscribed_at >= TIMESTAMP '2025-01-01'
    AND subscribed_at <  TIMESTAMP '2026-01-01'
), uses AS (
  SELECT customer_id, count(*) AS n FROM 'data/usage_events.parquet'
  WHERE event_at >= TIMESTAMP '2025-01-01' AND event_at < TIMESTAMP '2026-01-01'
  GROUP BY 1
)
SELECT avg(date_diff('second', subscribed_at, ends) / 86400.0 / n) AS value
FROM cohort JOIN uses USING (customer_id);
