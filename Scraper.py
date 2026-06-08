"""
Interactive Web Scraper
=======================

Fetches data from the public practice sites at https://toscrape.com and
presents it in a clean, readable table. You can scrape:

  - Books  (title, price, rating, availability)  from books.toscrape.com
  - Quotes (quote, author, tags)                 from quotes.toscrape.com

Both sites are sandboxes built specifically for learning web scraping, so
they are safe and allowed to scrape. Always check a real site's robots.txt
and terms of service before scraping it.

Libraries used: requests (fetch pages) and BeautifulSoup (parse HTML).
"""

import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

# A descriptive User-Agent is polite and identifies your scraper.
HEADERS = {"User-Agent": "Internship-WebScraper/1.0 (educational project)"}
TIMEOUT = 10  # seconds


def fetch(url):
    """Download a page and return a BeautifulSoup object, or None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [!] Could not fetch {url}: {exc}")
        return None
    return BeautifulSoup(response.text, "html.parser")


# Maps the star-rating CSS class to a number.
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_books(soup):
    """Extract book records from a books.toscrape.com listing page."""
    books = []
    for item in soup.select("article.product_pod"):
        title = item.h3.a["title"]
        price = item.select_one("p.price_color").get_text(strip=True)
        availability = item.select_one("p.instock.availability").get_text(strip=True)

        rating = 0
        rating_tag = item.select_one("p.star-rating")
        if rating_tag:
            for cls in rating_tag.get("class", []):
                if cls in RATING_WORDS:
                    rating = RATING_WORDS[cls]
        books.append(
            {
                "title": title,
                "price": price,
                "rating": f"{rating}/5",
                "availability": availability,
            }
        )
    return books


def parse_quotes(soup):
    """Extract quote records from a quotes.toscrape.com page."""
    quotes = []
    for item in soup.select("div.quote"):
        text = item.select_one("span.text").get_text(strip=True)
        author = item.select_one("small.author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in item.select("a.tag")]
        quotes.append(
            {
                "quote": text,
                "author": author,
                "tags": ", ".join(tags),
            }
        )
    return quotes


# Configuration for each scrape target.
TARGETS = {
    "books": {
        "label": "Books",
        "url_template": "https://books.toscrape.com/catalogue/page-{page}.html",
        "first_page": "https://books.toscrape.com/catalogue/page-1.html",
        "parser": parse_books,
        "columns": ["title", "price", "rating", "availability"],
    },
    "quotes": {
        "label": "Quotes",
        "url_template": "https://quotes.toscrape.com/page/{page}/",
        "first_page": "https://quotes.toscrape.com/page/1/",
        "parser": parse_quotes,
        "columns": ["quote", "author", "tags"],
    },
}


def scrape(target_key, num_pages):
    """Scrape `num_pages` pages from the given target and return all records."""
    target = TARGETS[target_key]
    all_records = []
    for page in range(1, num_pages + 1):
        url = target["url_template"].format(page=page)
        print(f"  Fetching page {page} ...")
        soup = fetch(url)
        if soup is None:
            break
        records = target["parser"](soup)
        if not records:
            print("  No more records found, stopping.")
            break
        all_records.extend(records)
        time.sleep(0.5)  # be polite: small pause between requests
    return all_records


def print_table(records, columns):
    """Print records as a simple aligned table, truncating long cells."""
    if not records:
        print("  Nothing to display.")
        return

    max_width = 45
    # Compute column widths.
    widths = {}
    for col in columns:
        cell_lengths = [len(str(r[col])[:max_width]) for r in records]
        widths[col] = max(len(col), max(cell_lengths))

    # Header
    header = " | ".join(col.upper().ljust(widths[col]) for col in columns)
    print("\n" + header)
    print("-" * len(header))

    # Rows
    for r in records:
        row = " | ".join(
            str(r[col])[:max_width].ljust(widths[col]) for col in columns
        )
        print(row)
    print(f"\n  {len(records)} record(s) total.")


def save_csv(records, columns, filename):
    """Write records to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)
    print(f"  Saved to {filename}")


def ask_int(prompt, default):
    """Ask for an integer, returning a default if the input is blank/invalid."""
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value > 0 else default
    except ValueError:
        print(f"  Not a number, using {default}.")
        return default


def main():
    print("=" * 50)
    print(" Interactive Web Scraper")
    print("=" * 50)

    while True:
        print("\nWhat would you like to scrape?")
        print("  1. Books   (books.toscrape.com)")
        print("  2. Quotes  (quotes.toscrape.com)")
        print("  0. Exit")

        choice = input("\nYour choice (0-2): ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        target_key = {"1": "books", "2": "quotes"}.get(choice)
        if target_key is None:
            print("Invalid choice. Pick 0, 1, or 2.")
            continue

        pages = ask_int("How many pages? (default 1): ", default=1)
        records = scrape(target_key, pages)

        columns = TARGETS[target_key]["columns"]
        print_table(records, columns)

        if records:
            save = input("\nSave results to CSV? (y/n): ").strip().lower()
            if save == "y":
                filename = f"{target_key}_data.csv"
                save_csv(records, columns, filename)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
