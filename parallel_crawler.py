import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

import time
import csv
import os


# -----------------------------
# Configuration
# -----------------------------

START_URL = "http://localhost:8000/page1.html"

MAX_PAGES = 50

DEFAULT_WORKERS = 4

# Artificial delay used only for benchmarking
SIMULATED_DELAY = 0.1


# =========================================================
# Fetch and process one webpage
# =========================================================

def fetch_page(
    url,
    start_url,
    delay=SIMULATED_DELAY
):

    try:

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
                "User-Agent":
                "ParallelWebCrawler/1.0"
            }

        )


        if response.status_code != 200:

            return None


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

        links = []


        for link in soup.find_all(
            "a",
            href=True
        ):

            new_url = urljoin(
                url,
                link["href"]
            )


            if not new_url.startswith("http"):

                continue


            # Same domain
            if (
                urlparse(new_url).netloc
                !=
                urlparse(start_url).netloc
            ):

                continue


            links.append(new_url)


        return {

            "url": url,

            "title": title,

            "links": links,

            "links_found": len(links)

        }


    except Exception as e:

        print(
            "Error crawling",
            url,
            ":",
            e
        )

        return None


# =========================================================
# Parallel crawler
# =========================================================

def crawl_parallel(

    start_url=START_URL,

    max_pages=MAX_PAGES,

    workers=DEFAULT_WORKERS,

    delay=SIMULATED_DELAY,

    verbose=True

):

    visited = set()

    queue = [start_url]

    results = []


    start_time = time.perf_counter()


    while queue and len(visited) < max_pages:


        # --------------------------------
        # Create current batch
        # --------------------------------

        current_batch = []


        while (

            queue

            and

            len(current_batch) < workers

            and

            len(visited) + len(current_batch)
            < max_pages

        ):

            url = queue.pop(0)


            if url in visited:

                continue


            # Mark as scheduled
            visited.add(url)

            current_batch.append(url)


        if not current_batch:

            break


        if verbose:

            print(
                "\nStarting parallel batch:"
            )

            for url in current_batch:

                print(
                    "  →",
                    url
                )


        # --------------------------------
        # Create worker threads
        # --------------------------------

        with ThreadPoolExecutor(
            max_workers=workers
        ) as executor:


            future_tasks = {

                executor.submit(
                    fetch_page,
                    url,
                    start_url,
                    delay
                ): url

                for url in current_batch

            }


            # --------------------------------
            # Collect completed tasks
            # --------------------------------

            for future in as_completed(
                future_tasks
            ):

                url = future_tasks[future]


                try:

                    result = future.result()


                except Exception as e:

                    print(
                        "Worker error:",
                        e
                    )

                    continue


                if result is None:

                    continue


                # --------------------------------
                # Store result
                # --------------------------------

                results.append({

                    "url":
                    result["url"],

                    "title":
                    result["title"],

                    "links_found":
                    result["links_found"]

                })


                # --------------------------------
                # Add newly discovered URLs
                # --------------------------------

                for new_url in result["links"]:


                    if (

                        new_url not in visited

                        and

                        new_url not in queue

                    ):

                        queue.append(
                            new_url
                        )


    # --------------------------------
    # Execution time
    # --------------------------------

    execution_time = (

        time.perf_counter()

        -

        start_time

    )


    # --------------------------------
    # Save results
    # --------------------------------

    os.makedirs(
        "results",
        exist_ok=True
    )


    with open(

        "results/parallel_results.csv",

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
    # Display results
    # --------------------------------

    if verbose:

        print(
            "\n" + "=" * 40
        )

        print(
            "PARALLEL CRAWLER RESULTS"
        )

        print(
            "=" * 40
        )

        print(
            "Workers:",
            workers
        )

        print(
            "Pages Crawled:",
            len(results)
        )

        print(
            "Execution Time:",
            round(
                execution_time,
                3
            ),
            "seconds"
        )

        print(
            "Results saved to:",
            "results/parallel_results.csv"
        )


    return execution_time


# --------------------------------
# Main
# --------------------------------

if __name__ == "__main__":

    crawl_parallel(

        start_url=START_URL,

        max_pages=MAX_PAGES,

        workers=DEFAULT_WORKERS,

        delay=SIMULATED_DELAY

    )