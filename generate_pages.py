import os
import sys


# ==========================================================
# CONFIGURATION
# ==========================================================

DEFAULT_PAGES = 50
LINKS_PER_PAGE = 5
OUTPUT_FOLDER = "test_site"


# ==========================================================
# GENERATE TEST WEBSITE
# ==========================================================

def generate_pages(
    num_pages=DEFAULT_PAGES,
    links_per_page=LINKS_PER_PAGE
):

    if num_pages <= 0:
        raise ValueError(
            "Number of pages must be greater than 0."
        )

    # Create test_site folder
    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Remove old HTML pages
    # ------------------------------------------------------

    for filename in os.listdir(
        OUTPUT_FOLDER
    ):

        if filename.endswith(".html"):

            os.remove(
                os.path.join(
                    OUTPUT_FOLDER,
                    filename
                )
            )

    # ------------------------------------------------------
    # Generate new pages
    # ------------------------------------------------------

    for i in range(
        1,
        num_pages + 1
    ):

        links_html = ""

        # Create links to next pages
        for j in range(
            1,
            links_per_page + 1
        ):

            next_page = i + j

            if next_page <= num_pages:

                links_html += f"""
                <li>
                    <a href="page{next_page}.html">
                        Page {next_page}
                    </a>
                </li>
                """

        html = f"""<!DOCTYPE html>

<html>

<head>

    <title>Test Page {i}</title>

    <meta charset="UTF-8">

</head>

<body>

    <h1>Parallel Web Crawler Test Page {i}</h1>

    <p>
        This is test webpage number {i}.
    </p>

    <p>
        This page is part of the controlled dataset
        used for parallel web crawler performance testing.
    </p>

    <h2>Links</h2>

    <ul>
        {links_html}
    </ul>

</body>

</html>
"""

        file_path = os.path.join(
            OUTPUT_FOLDER,
            f"page{i}.html"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(html)

    print()
    print("=" * 50)
    print("TEST WEBSITE GENERATED")
    print("=" * 50)
    print(
        "Pages created :",
        num_pages
    )
    print(
        "Links/page    :",
        links_per_page
    )
    print(
        "Location      :",
        OUTPUT_FOLDER
    )
    print("=" * 50)


# ==========================================================
# COMMAND LINE
# ==========================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        try:

            pages = int(
                sys.argv[1]
            )

        except ValueError:

            print(
                "Please enter a valid number of pages."
            )

            sys.exit(1)

    else:

        pages = DEFAULT_PAGES

    generate_pages(
        pages
    )