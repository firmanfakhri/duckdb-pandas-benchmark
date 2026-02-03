import duckdb
import time

start = time.time()

result = duckdb.sql("""
    SELECT 
        DATE_TRUNC('hour', tpep_pickup_datetime) as hour,
        COUNT(*) as trip_count,
        AVG(trip_distance) as avg_distance,
        AVG(total_amount) as avg_fare,
        SUM(total_amount) as total_revenue
    FROM 'yellow_tripdata_2016-03.csv'
    WHERE fare_amount > 0 
        AND trip_distance > 0
        AND passenger_count BETWEEN 1 AND 6
    GROUP BY DATE_TRUNC('hour', tpep_pickup_datetime)
    ORDER BY hour
""").df()

query_time = time.time() - start
print(f"query_time: {query_time:.3f} s")