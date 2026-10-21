# new_customer_use_gap_days (v1, owner: Data)

"Frecuencia promedio en días de los clientes suscritos en el último año", written down.

- **Cliente suscrito:** `subscribed_at` within the 365 days before the cutoff, and not cancelled on the cutoff date.
- **Cutoff:** 2026-09-30 (inclusive; implemented as `< 2026-10-01`). Passed as a parameter, never "today".
- **Uso:** one session. Events less than 30 minutes apart count as a single use.
- **Window per customer:** from their own `subscribed_at` to the cutoff.
- **Frecuencia:** mean number of days between consecutive uses, pooled over all gaps of the cohort. Customers with fewer than 2 uses contribute no gaps.
- **Unit:** days. Lower means more frequent.

Implementation: `definitions/agreed.sql`.
