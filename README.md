# DuckDB vs Pandas Performance Benchmark

A comprehensive performance comparison between **DuckDB** and **Pandas** for analyzing large CSV files, demonstrating the dramatic speed improvements when using DuckDB with Parquet format.

> 📊 **TL;DR**: DuckDB with Parquet is **45x faster** than Pandas with CSV for complex analytical queries, while using 99%+ less memory.

## 🎯 Benchmark Results

### Dataset
- **Source**: NYC Taxi Trip Data (March 2016)
- **Format**: CSV (1.78 GB) → Parquet (318 MB)
- **Rows**: 12,210,952
- **Columns**: 19

### Read Performance (COUNT query)

| Method | Format | Time | Memory | Speed vs Pandas CSV |
|--------|--------|------|--------|---------------------|
| Pandas | CSV | 25.88s | 2.17 GB | 1x (baseline) |
| Pandas | Parquet (full) | 7.28s | 0.37 GB | 3.6x faster |
| Pandas | Parquet (selective) | 1.56s | 0.97 GB | 16.6x faster |
| DuckDB | CSV | 2.58s | 0.01 GB | 10x faster |
| **DuckDB** | **Parquet** | **0.12s** | **0.00 GB** | **215x faster** ⚡ |

### Complex Query Performance (groupby/aggregation)

| Method | Format | Total Time | Speed vs Pandas CSV |
|--------|--------|------------|---------------------|
| Pandas | CSV | 33.95s | 1x (baseline) |
| Pandas | Parquet (optimized) | 1.36s | 25x faster |
| DuckDB | CSV | 3.32s | 10x faster |
| **DuckDB** | **Parquet** | **0.75s** | **45x faster** ⚡ |

## 📁 Repository Structure

```
.
├── README.md                          # This file
├── benchmark_results.md               # Detailed benchmark results
│
├── benchmark_pandas_csv.py            # Pandas CSV read benchmark
├── benchmark_pandas_parquet.py        # Pandas Parquet read benchmark
├── benchmark_duckdb_csv.py            # DuckDB CSV query benchmark
├── benchmark_duckdb_parquet.py        # DuckDB Parquet conversion & query
│
├── query_pandas_csv.py                # Complex query with Pandas CSV
├── query_pandas_parquet.py            # Complex query with Pandas Parquet
├── query_duckdb_csv.py                # Complex query with DuckDB CSV
└── query_duckdb_parquet.py            # Complex query with DuckDB Parquet
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- At least 4GB free RAM
- ~2GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/duckdb-pandas-benchmark.git
cd duckdb-pandas-benchmark

# Install dependencies
pip install duckdb pandas pyarrow psutil
```

### Download Dataset

1. Visit [NYC Yellow Taxi Trip Data on Kaggle](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data)
2. Download **Yellow Taxi Trip Records - March 2016** (`yellow_tripdata_2016-03.csv`)
3. Save as `yellow_tripdata_2016-03.csv` in the project directory

### Run Benchmarks

```bash
# Simple read benchmark (Pandas CSV - ~26 seconds)
python benchmark_pandas_csv.py

# Convert to Parquet + benchmark (DuckDB - ~7 seconds)
python benchmark_duckdb_parquet.py

# Complex query benchmark (Pandas Parquet)
python query_pandas_parquet.py

# Complex query benchmark (DuckDB Parquet - < 1 second!)
python query_duckdb_parquet.py
```

## 📊 Benchmark Scripts Explained

### 1. Read Benchmarks (`benchmark_*.py`)

These scripts measure **read/load performance only**:

- `benchmark_pandas_csv.py` - Load CSV with Pandas
- `benchmark_pandas_parquet.py` - Load Parquet with Pandas (full & selective columns)
- `benchmark_duckdb_csv.py` - Query CSV with DuckDB (COUNT only)
- `benchmark_duckdb_parquet.py` - Convert CSV→Parquet + query

**What they test**: I/O speed, memory usage, file conversion time.

### 2. Query Benchmarks (`query_*.py`)

These scripts measure **real analytical query performance**:

```sql
SELECT
    DATE_TRUNC('hour', tpep_pickup_datetime) as hour,
    COUNT(*) as trip_count,
    AVG(trip_distance) as avg_distance,
    AVG(total_amount) as avg_fare,
    SUM(total_amount) as total_revenue
FROM trips
WHERE fare_amount > 0
    AND trip_distance > 0
    AND passenger_count BETWEEN 1 AND 6
GROUP BY hour
ORDER BY hour
```

**What they test**: Filtering, aggregation, grouping - typical data analysis tasks.

## 🔧 Environment

```
OS: Windows
Python: 3.11.9
pandas: 3.0.0
pyarrow: 23.0.0
DuckDB: 1.1.0
psutil: (for memory monitoring)
```

## 💡 Key Takeaways

### When to Use DuckDB

✅ **Perfect for:**
- Ad-hoc data analysis
- Large CSV/Parquet files (50MB+)
- ETL/ELT pipelines
- Data exploration & prototyping
- Reports and dashboards
- Log file analysis

❌ **NOT for:**
- Transactional systems (OLTP)
- Multi-user concurrent writes
- Real-time applications
- Production services requiring 24/7 uptime

### Performance Tips

1. **Always use Parquet for repeated queries**
   - 82.6% smaller file size
   - Columnar format = read only needed columns
   - Built-in compression

2. **Select only columns you need**
   ```python
   # ❌ Slow
   df = pd.read_parquet('data.parquet')

   # ✅ Fast
   df = pd.read_parquet('data.parquet', columns=['col1', 'col2'])
   ```

3. **DuckDB can query files directly**
   ```python
   # No need to load into memory first!
   result = duckdb.sql("SELECT * FROM 'data.parquet'").df()
   ```

## 🌟 Acknowledgments

- [DuckDB](https://duckdb.org/) - Amazing in-process analytical database
- [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - Public taxi trip data
- [Apache Parquet](https://parquet.apache.org/) - Efficient columnar storage format

## 📬 Contact

Questions or feedback? Drop a comment on the article or open an issue!

---

**⭐ If you found this helpful, please star the repo!**
