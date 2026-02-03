import pandas as pd
import time

# Read from Parquet instead of CSV
# Assumes `yellow_tripdata_2016-03.parquet` is present in the working directory

# Read only the columns we need to minimize I/O and deserialization time
cols = ['tpep_pickup_datetime','trip_distance','fare_amount','passenger_count','total_amount']
read_start = time.perf_counter()
df = pd.read_parquet('yellow_tripdata_2016-03.parquet', columns=cols)
read_time = time.perf_counter() - read_start

# Ensure datetime column is parsed
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

# Run the query and time the compute separately
start = time.perf_counter()

filtered = df[
    (df['fare_amount'] > 0) & 
    (df['trip_distance'] > 0) & 
    (df['passenger_count'].between(1, 6))
]

result = filtered.groupby(
    filtered['tpep_pickup_datetime'].dt.floor('h')
).agg({
    'tpep_pickup_datetime': 'count',
    'trip_distance': 'mean',
    'total_amount': ['mean', 'sum']
}).sort_index()

query_time = time.perf_counter() - start


# Short summary output
print(result.head())
print(f"read_time: {read_time:.3f} s")
print(f"query_time: {query_time:.3f} s")
print(f"total_time: {(read_time+query_time):.3f} s")
