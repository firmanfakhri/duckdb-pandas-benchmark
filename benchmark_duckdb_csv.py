import duckdb
import time
import psutil
import os

process = psutil.Process(os.getpid())

def mem_gb():
    return process.memory_info().rss / 1024**3


print("=== DUCKDB CSV QUERY ===")

start_mem = mem_gb()
start_time = time.time()

result = duckdb.sql("""
    SELECT COUNT(*) AS total_trips
    FROM 'yellow_tripdata_2016-03.csv'
""").fetchall()

query_time = time.time() - start_time
end_mem = mem_gb()

print("Result:", result)
print(f"Query Time: {query_time:.2f}s")
print(f"Memory Increase: {end_mem - start_mem:.2f} GB")
