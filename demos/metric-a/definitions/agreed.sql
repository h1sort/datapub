-- AGREED: see DEFINITION.md
-- Active customer = paying on the cutoff date (subscribed_at < cutoff, not cancelled by it)
--   AND subscribed_at in the 365 days up to the cutoff (new-customer cohort).
-- Uses = events in [subscribed_at, cutoff]. Customers with < 2 uses are excluded.
-- Value = pooled mean gap in days between consecutive uses, collapsing events
--   within the same session (< 30 min apart) into one use.
WITH params AS (SELECT TIMESTAMP '2026-10-01' AS cutoff),
cohort AS (
  SELECT customer_id, subscribed_at FROM 'data/subscriptions.parquet', params
  WHERE subscribed_at >  cutoff - INTERVAL 365 DAY AND subscribed_at < cutoff
    AND (cancelled_at IS NULL OR cancelled_at > cutoff)
), ev AS (
  SELECT e.customer_id, event_at,
         date_diff('minute', lag(event_at) OVER w, event_at) AS mins
  FROM 'data/usage_events.parquet' e JOIN cohort c USING (customer_id), params
  WHERE event_at >= c.subscribed_at AND event_at < cutoff
  WINDOW w AS (PARTITION BY e.customer_id ORDER BY event_at)
), uses AS (            -- one row per session ("uso")
  SELECT customer_id, event_at,
         date_diff('second', lag(event_at) OVER w, event_at) / 86400.0 AS gap
  FROM ev WHERE mins IS NULL OR mins >= 30
  WINDOW w AS (PARTITION BY customer_id ORDER BY event_at)
)
SELECT avg(gap) AS value FROM uses WHERE gap IS NOT NULL;
