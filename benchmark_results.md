# Benchmark Results — Yellow Taxi 2016-03 🚕

**Environment**
- OS: Windows
- Python: CPython 3.11.9 (project `.venv`)
- pandas: 3.0.0
- pyarrow: 23.0.0 (fastparquet: not installed)
- Dataset: `yellow_tripdata_2016-03.csv` / `.parquet` (rows: 12,210,952; columns: 19)

---

## Read times (I/O only) ⚡

| Format   | Method / Notes                                    | Columns | Time |
|----------|---------------------------------------------------|:-------:|-----:|
| CSV      | pandas.read_csv (full)                            | all     | 25.879 s |
| CSV      | pandas.read_csv (usecols subset)                  | subset  | 12.771 s |
| Parquet  | pd.read_parquet (full)                            | all     | 7.277 s |
| Parquet  | pd.read_parquet (usecols subset)                  | subset  | 1.563 s |
| Parquet  | pyarrow.read_table → .to_pandas (columns subset)  | subset  | 0.291 s + 0.928 s = 1.219 s |

> Note: reading a subset of columns drastically reduces read time. Using `pyarrow.read_table` is very fast for I/O; conversion to pandas (`.to_pandas()`) adds conversion time.

---

## Query / Compute timings (groupby/agg) ⏱️

| Engine / Workflow | Read time | Compute time (groupby/agg) | Total |
|-------------------|---------:|---------------------------:|------:|
| pandas (CSV)      | 25.879 s | 6.418 s                    | 32.297 s |
| pandas (Parquet, usecols optimized) | 0.325 s  | 1.064 s                    | 1.390 s |
| pyarrow → pandas (read_table + to_pandas) | 0.291 s + 0.928 s | (compute measured separately) | ~1.219 s + compute |

> Table shows how splitting I/O vs compute gives a clearer picture of where time is spent.

---

---

## Memory observations 🧠
- Parquet full load: Memory after full load **0.37 GB** (delta ~0.30 GB)
- Parquet usecols load: Memory after usecols **0.97 GB** (delta ~0.59 GB)

(Measurements taken during script runs; memory deltas depend on lifetime of variables and GC.)

---

## Key takeaways ✅
- Parquet is usually faster than CSV when reading (especially for column subsets).
- Always read only the columns you need when using Parquet to minimize I/O and deserialization.
- If max read throughput is critical, try `pyarrow.read_table(..., use_threads=True)` + `.to_pandas()` and measure both steps separately.
- For repeated analytical queries consider DuckDB or Polars (often faster at read+compute over Parquet).

---

## Next steps / recommendations 🔧
- Use `columns=` argument when calling `pd.read_parquet` for query scripts.
- Consider writing partitioned Parquet files (by date) and choosing larger row-groups for better IO patterns.
- Add a small `--record` option to benchmark scripts to append runs to this file automatically.

---

## Detailed comparison tables 📊

### 1) Benchmark scripts (I/O / conversion / memory)

| Tool   | Input | Action / Metric | Time | Memory delta |
|--------|:-----:|-----------------|-----:|-------------:|
| pandas | CSV   | read (full)     | 25.97 s | 2.17 GB |
| pandas | Parquet | read (full)   | 7.277 s | 0.37 GB |
| pandas | Parquet | read (usecols) | 1.563 s | 0.97 GB |
| duckdb | CSV   | query (COUNT)   | 2.58 s | 0.01 GB |
| duckdb | Parquet | query (COUNT) | 0.12 s | 0.00 GB |
| duckdb | CSV→Parquet | conversion | 7.13 s | 0.02 GB |

> Notes: `benchmark_*` scripts measure different things (read-only, conversion, or query). Use the table for quick comparison; refer to individual scripts for full context.

### 2) Query scripts (end-to-end query performance)

| Script / Engine | Input | Read time | Query time | Total / Notes |
|-----------------|:-----:|---------:|-----------:|---------------:|
| `query_pandas_csv.py` (pandas) | CSV | 25.97 s (from benchmark) | 7.98 s | total (read+compute) ≈ 33.95 s |
| `query_pandas_parquet.py` (pandas) | Parquet | 0.321 s | 1.041 s | total ≈ 1.362 s |
| `query_duckdb_csv.py` (duckdb) | CSV | n/a (internal) | 3.320 s | duckdb reads+executes in one step |
| `query_duckdb_parquet.py` (duckdb) | Parquet | n/a (internal) | 0.752 s | duckdb reads+executes in one step |

> Notes: For pandas-based query scripts we separate read vs compute for clarity. DuckDB executes queries end-to-end (it can stream from Parquet/CSV directly) so timings reflect full query execution.



