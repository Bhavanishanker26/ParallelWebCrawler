import csv
import os

from sequential_crawler import (
    crawl_sequential
)

from parallel_crawler import (
    crawl_parallel
)


# =========================================================
# Configuration
# =========================================================

START_URL = "http://localhost:8000/page1.html"

MAX_PAGES = 50

SIMULATED_DELAY = 0.1

WORKER_COUNTS = [
    1,
    2,
    4,
    8
]


# =========================================================
# Performance Test
# =========================================================

def run_performance_test():

    print("\n")
    print("=" * 60)
    print(
        "PARALLEL WEB CRAWLER PERFORMANCE ANALYSIS"
    )
    print("=" * 60)

    print(
        f"Pages       : {MAX_PAGES}"
    )

    print(
        f"Delay/page  : {SIMULATED_DELAY} seconds"
    )

    print(
        f"Workers     : {WORKER_COUNTS}"
    )

    print("=" * 60)


    # =====================================================
    # 1. Sequential baseline
    # =====================================================

    print("\n")
    print(
        "Running SEQUENTIAL crawler..."
    )

    sequential_time = crawl_sequential(

        start_url=START_URL,

        max_pages=MAX_PAGES,

        delay=SIMULATED_DELAY,

        verbose=False

    )


    print(
        "Sequential Time:",
        round(
            sequential_time,
            3
        ),
        "seconds"
    )


    # =====================================================
    # Store performance results
    # =====================================================

    results = []


    # Add sequential baseline

    results.append({

        "method":
        "Sequential",

        "workers":
        1,

        "execution_time":
        round(
            sequential_time,
            3
        ),

        "speedup":
        1.0,

        "efficiency":
        100.0

    })


    # =====================================================
    # 2. Parallel tests
    # =====================================================

    for workers in WORKER_COUNTS:

        # Skip 1 worker because we already measured
        # the actual sequential implementation

        if workers == 1:

            continue


        print("\n")
        print(
            f"Running PARALLEL crawler "
            f"with {workers} workers..."
        )


        parallel_time = crawl_parallel(

            start_url=START_URL,

            max_pages=MAX_PAGES,

            workers=workers,

            delay=SIMULATED_DELAY,

            verbose=False

        )


        # ---------------------------------------------
        # Calculate speedup
        # ---------------------------------------------

        speedup = (
            sequential_time
            /
            parallel_time
        )


        # ---------------------------------------------
        # Calculate efficiency
        # ---------------------------------------------

        efficiency = (
            speedup
            /
            workers
        ) * 100


        print(
            "Execution Time:",
            round(
                parallel_time,
                3
            ),
            "seconds"
        )

        print(
            "Speedup:",
            round(
                speedup,
                3
            ),
            "x"
        )

        print(
            "Efficiency:",
            round(
                efficiency,
                2
            ),
            "%"
        )


        results.append({

            "method":
            "Parallel",

            "workers":
            workers,

            "execution_time":
            round(
                parallel_time,
                3
            ),

            "speedup":
            round(
                speedup,
                3
            ),

            "efficiency":
            round(
                efficiency,
                2
            )

        })


    # =====================================================
    # 3. Save CSV
    # =====================================================

    os.makedirs(
        "results",
        exist_ok=True
    )


    output_file = (
        "results/performance_results.csv"
    )


    with open(

        output_file,

        "w",

        newline="",

        encoding="utf-8"

    ) as file:


        writer = csv.DictWriter(

            file,

            fieldnames=[

                "method",

                "workers",

                "execution_time",

                "speedup",

                "efficiency"

            ]

        )


        writer.writeheader()

        writer.writerows(results)


    # =====================================================
    # 4. Display final table
    # =====================================================

    print("\n")

    print("=" * 70)

    print(
        "FINAL PERFORMANCE RESULTS"
    )

    print("=" * 70)


    print(

        f"{'Method':<15}"
        f"{'Workers':<10}"
        f"{'Time(s)':<12}"
        f"{'Speedup':<12}"
        f"{'Efficiency':<15}"

    )


    print("-" * 70)


    for result in results:

        print(

            f"{result['method']:<15}"

            f"{result['workers']:<10}"

            f"{result['execution_time']:<12}"

            f"{result['speedup']:<12}"

            f"{result['efficiency']:<15}%"

        )


    print("=" * 70)


    print(
        "\nPerformance results saved to:"
    )

    print(
        output_file
    )


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    run_performance_test()