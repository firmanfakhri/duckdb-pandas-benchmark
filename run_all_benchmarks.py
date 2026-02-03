"""
Run all benchmarks in sequence and display results.
This script will execute all benchmark scripts and summarize the results.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name):
    """Run a Python script and capture its output."""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace unencodable chars instead of crashing
            timeout=120  # 2 minute timeout
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[WARNING] {script_name} timed out after 2 minutes")
        return False
    except Exception as e:
        print(f"[ERROR] Error running {script_name}: {e}")
        return False

def check_dataset_exists():
    """Check if the dataset file exists."""
    csv_file = 'yellow_tripdata_2016-03.csv'

    if not os.path.exists(csv_file):
        print(f"\n[ERROR] Dataset file not found: {csv_file}")
        print("\nPlease download the dataset first:")
        print("1. Visit: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
        print("2. Download: Yellow Taxi Trip Records - March 2016")
        print(f"3. Save as: {csv_file}")
        return False

    file_size = os.path.getsize(csv_file) / (1024**3)
    print(f"[OK] Dataset found: {csv_file} ({file_size:.2f} GB)")
    return True

def main():
    print("="*60)
    print("DuckDB vs Pandas Benchmark Suite")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check dataset
    if not check_dataset_exists():
        sys.exit(1)

    # Define benchmark order
    benchmarks = [
        ("benchmark_pandas_csv.py", "Pandas CSV Read"),
        ("benchmark_pandas_parquet.py", "Pandas Parquet Read"),
        ("benchmark_duckdb_csv.py", "DuckDB CSV Query"),
        ("benchmark_duckdb_parquet.py", "DuckDB Conversion & Query"),
        ("query_pandas_csv.py", "Pandas CSV Complex Query"),
        ("query_pandas_parquet.py", "Pandas Parquet Complex Query"),
        ("query_duckdb_csv.py", "DuckDB CSV Complex Query"),
        ("query_duckdb_parquet.py", "DuckDB Parquet Complex Query"),
    ]

    results = []

    for script, description in benchmarks:
        if os.path.exists(script):
            success = run_script(script)
            results.append((description, "[OK] Success" if success else "[FAIL] Failed"))
        else:
            print(f"\n[WARNING] Skipping {script} (file not found)")
            results.append((description, "[SKIP] Not found"))

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    for description, status in results:
        print(f"{description:40} {status}")

    print(f"\n{'='*60}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    print("\n[INFO] Check benchmark_results.md for detailed performance metrics!")

if __name__ == "__main__":
    main()
