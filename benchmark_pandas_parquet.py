import pandas as pd
import time
import psutil
import os

print("=== PANDAS PARQUET BENCHMARK ===")
print("pandas", pd.__version__)
try:
    import pyarrow
    print("pyarrow", pyarrow.__version__)
except Exception:
    print("pyarrow not installed")

proc = psutil.Process(os.getpid())

def mem_gb():
    return proc.memory_info().rss / 1024**3

cols = ['tpep_pickup_datetime','trip_distance','fare_amount','passenger_count','total_amount']

# Full file read
start_mem = mem_gb()
start = time.perf_counter()
try:
    df_full = pd.read_parquet('yellow_tripdata_2016-03.parquet')
    read_full = time.perf_counter() - start
    mem_after = mem_gb()
    print(f"read_parquet full: {read_full:.3f}s")
    print(f"Memory after full load: {mem_after:.2f} GB (delta {mem_after - start_mem:.2f} GB)")
    print("shape:", df_full.shape)
except Exception as e:
    print("read_parquet full failed:", e)

# Read only needed columns
start_mem = mem_gb()
start = time.perf_counter()
try:
    df_cols = pd.read_parquet('yellow_tripdata_2016-03.parquet', columns=cols)
    read_cols = time.perf_counter() - start
    mem_after = mem_gb()
    print(f"read_parquet usecols: {read_cols:.3f}s")
    print(f"Memory after usecols load: {mem_after:.2f} GB (delta {mem_after - start_mem:.2f} GB)")
    print("shape:", df_cols.shape)
except Exception as e:
    print("read_parquet usecols failed:", e)

# If pyarrow available, measure read_table -> to_pandas
try:
    import pyarrow.parquet as pq
    start = time.perf_counter()
    table = pq.read_table('yellow_tripdata_2016-03.parquet', columns=cols, use_threads=True)
    read_table = time.perf_counter() - start
    start = time.perf_counter()
    df_from_table = table.to_pandas()
    to_pandas = time.perf_counter() - start
    print(f"pyarrow read_table: {read_table:.3f}s, to_pandas: {to_pandas:.3f}s")
except Exception as e:
    print("pyarrow read_table measurement skipped:", e)

print("=== done ===")
