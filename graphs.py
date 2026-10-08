import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------------------
# CREATE GRAPHS FOLDER
# --------------------------------------------------

os.makedirs("graphs", exist_ok=True)

# --------------------------------------------------
# READ PERFORMANCE RESULTS
# --------------------------------------------------

file_path = "results/performance_results.csv"

df = pd.read_csv(file_path)

print("\n========================================")
print("GENERATING PERFORMANCE GRAPHS")
print("========================================")

print("\nPerformance Data:")
print(df)

# --------------------------------------------------
# 1. EXECUTION TIME GRAPH
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["workers"],
    df["execution_time"],
    marker="o",
    linewidth=2
)

plt.title("Execution Time vs Number of Workers")
plt.xlabel("Number of Workers")
plt.ylabel("Execution Time (seconds)")
plt.grid(True)

plt.savefig(
    "graphs/execution_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 2. SPEEDUP GRAPH
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["workers"],
    df["speedup"],
    marker="o",
    linewidth=2
)

plt.title("Speedup vs Number of Workers")
plt.xlabel("Number of Workers")
plt.ylabel("Speedup (x)")
plt.grid(True)

plt.savefig(
    "graphs/speedup.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 3. EFFICIENCY GRAPH
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    df["workers"],
    df["efficiency"],
    marker="o",
    linewidth=2
)

plt.title("Parallel Efficiency vs Number of Workers")
plt.xlabel("Number of Workers")
plt.ylabel("Efficiency (%)")
plt.grid(True)

plt.savefig(
    "graphs/efficiency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# COMPLETION MESSAGE
# --------------------------------------------------

print("\n========================================")
print("GRAPHS GENERATED SUCCESSFULLY")
print("========================================")

print("1. graphs/execution_time.png")
print("2. graphs/speedup.png")
print("3. graphs/efficiency.png")