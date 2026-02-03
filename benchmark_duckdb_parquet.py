import duckdb
import time
import psutil
import os

process = psutil.Process(os.getpid())

def mem_gb():
    return process.memory_info().rss / 1024**3


print("=== DUCKDB CSV -> PARQUET CONVERSION ===")

start_mem = mem_gb()
start_time = time.time()

duckdb.sql("""
    COPY (
        SELECT * 
        FROM 'yellow_tripdata_2016-03.csv'
    )
    TO 'yellow_tripdata_2016-03.parquet'
    (FORMAT PARQUET)
""")

conv_time = time.time() - start_time
end_mem = mem_gb()

print(f"Conversion Time: {conv_time:.2f}s")
print(f"Memory Increase (Conversion): {end_mem - start_mem:.2f} GB")


print("\n=== DUCKDB PARQUET QUERY ===")

start_mem = mem_gb()
start_time = time.time()

result = duckdb.sql("""
    SELECT COUNT(*) AS total_trips
    FROM 'yellow_tripdata_2016-03.parquet'
""").fetchall()

query_time = time.time() - start_time
end_mem = mem_gb()

print("Result:", result)
print(f"Query Time: {query_time:.2f}s")
print(f"Memory Increase (Query): {end_mem - start_mem:.2f} GB")
