# metric-a

Synthetic data (a Linear-like project tool) and four SQL readings of the 2023 metric
"average frequency in days of customers subscribed in the last year".
Three defensible readings (`definitions/a|b|c.sql`) give three different numbers;
`definitions/agreed.sql` (see `DEFINITION.md`) gives one.

```
make data      # deterministic Parquet files in data/ (seeded)
make metric-a  # data + run all SQL in DuckDB + write ../../deck/data/metric-a.js
make clean     # remove data/
```

Requires `uv`. The slide SQL in `compute.py` is a condensed display version of the real queries.
