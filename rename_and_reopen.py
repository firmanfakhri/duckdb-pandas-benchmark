"""
Quick script to rename this folder and reopen in VS Code.
Run this, and it will:
1. Rename the folder to 'duckdb-pandas-benchmark'
2. Automatically reopen it in VS Code
"""

import os
import shutil
import subprocess
import time

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
new_name = "duckdb-pandas-benchmark"
new_path = os.path.join(parent_dir, new_name)

print(f"Current directory: {current_dir}")
print(f"New directory will be: {new_path}")
print("\nThis will:")
print("1. Close VS Code (save your work first!)")
print("2. Rename the folder")
print("3. Reopen in VS Code")

response = input("\nProceed? (y/n): ")

if response.lower() != 'y':
    print("Cancelled.")
    exit()

print("\nRenaming folder...")
try:
    # Close VS Code windows (Windows only)
    subprocess.run(["taskkill", "/F", "/IM", "Code.exe"],
                   stderr=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL)
    time.sleep(2)  # Wait for VS Code to close

    # Rename the directory
    os.chdir(parent_dir)  # Move to parent first
    os.rename(os.path.basename(current_dir), new_name)

    print(f"✓ Renamed to: {new_name}")

    # Reopen in VS Code
    print("✓ Reopening in VS Code...")
    subprocess.Popen(["code", new_path])

    print("\n✓ Done! VS Code should reopen with the renamed folder.")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nManual steps:")
    print("1. Close VS Code")
    print(f"2. Rename folder manually to: {new_name}")
    print("3. Reopen in VS Code")
