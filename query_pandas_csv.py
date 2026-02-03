import pandas as pd
import time

df = pd.read_csv('yellow_tripdata_2016-03.csv')
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

start = time.time()

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

query_time = time.time() - start

# Short summary output
print(result.head())
print(f"query_time: {query_time:.3f} s")