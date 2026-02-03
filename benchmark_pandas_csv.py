import pandas as pd
import time

start = time.time()
df = pd.read_csv('yellow_tripdata_2016-03.csv')
load_time = time.time() - start

print(f"Pandas Load Time: {load_time:.2f}s")
print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**3:.2f} GB")