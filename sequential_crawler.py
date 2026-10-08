import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import csv
import os


# -----------------------------
# Configuration
# -----------------------------

START_URL = "http://localhost:8000/page1.html"

MAX_PAGES = 50

# Artificial delay used only for benchmarking
SIMULATED_DELAY = 0.1


def crawl_sequential(
    start_url=START_URL,
    max_pages=MAX_PAGES,
    delay=SIMULATED_DELAY,
    verbose=True
):

    visited = set()

    queue = [start_url]

    results = []

    start_time = time.perf_counter()


    while queue and len(visited) < max_pages:

        url = queue.pop(0)

        if url in visited:
            continue

        try:

            if verbose:
                print("Crawling:", url)

            # --------------------------------
            # Simulated network/processing time
            # --------------------------------

            time.sleep(delay)


            # --------------------------------
            # Download webpage
            # --------------------------------

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "ParallelWebCrawler/1.0"
                }
            )


            if response.status_code != 200:

                if verbose:
                    print(
                        "Failed:",
                        response.status_code,
                        url
                    )

                continue


            visited.add(url)


            # --------------------------------
            # Parse HTML
            # --------------------------------

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            # --------------------------------
            # Extract title
            # --------------------------------

            if soup.title and soup.title.string:

                title = soup.title.string.strip()

            else:

                title = "No Title"


            # --------------------------------
            # Extract links
            # --------------------------------

            links_found = 0


            for link in soup.find_all(
                "a",
                href=True
            ):

                new_url = urljoin(
                    url,
                    link["href"]
                )


                # Only HTTP/HTTPS
                if not new_url.startswith("http"):

                    continue


                # Same domain only
                if (
                    urlparse(new_url).netloc
                    !=
                    urlparse(start_url).netloc
                ):

                    continue


                if (
                    new_url not in visited
                    and
                    new_url not in queue
                ):

                    queue.append(new_url)

                    links_found += 1


            # --------------------------------
            # Store result
            # --------------------------------

            results.append({

                "url": url,

                "title": title,

                "links_found": links_found

            })


        except Exception as e:

            print(
                "Error crawling",
                url,
                ":",
                e
            )


    # --------------------------------
    # Calculate execution time
    # --------------------------------

    execution_time = (
        time.perf_counter()
        -
        start_time
    )


    # --------------------------------
    # Create results folder
    # --------------------------------

    os.makedirs(
        "results",
        exist_ok=True
    )


    # --------------------------------
    # Save CSV
    # --------------------------------

    with open(
        "results/sequential_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,

            fieldnames=[
                "url",
                "title",
                "links_found"
            ]
        )

        writer.writeheader()

        writer.writerows(results)


    # --------------------------------
    # Display result
    # --------------------------------

    print("\n" + "=" * 40)

    print(
        "SEQUENTIAL CRAWLER RESULTS"
    )

    print("=" * 40)

    print(
        "Pages Crawled:",
        len(results)
    )

    print(
        "Execution Time:",
        round(execution_time, 3),
        "seconds"
    )

    print(
        "Results saved to:",
        "results/sequential_results.csv"
    )


    return execution_time


# --------------------------------
# Main
# --------------------------------

if __name__ == "__main__":

    crawl_sequential()