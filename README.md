# Interactive Web Scraper

A Python program that fetches data from a website and presents it in a clean,
readable table. You choose what to scrape, how many pages, and whether to
export the results to CSV. Built as part of an internship task.

## Objective

Fetch data from a website using a web scraping library and present it in a
user-friendly way.

## What it scrapes

This project targets the public **practice sites** at
[toscrape.com](https://toscrape.com), which exist specifically for learning
web scraping:

| Source                  | Data collected                          |
|-------------------------|-----------------------------------------|
| books.toscrape.com      | title, price, star rating, availability |
| quotes.toscrape.com     | quote text, author, tags                |

> **A note on responsible scraping:** these sandbox sites are explicitly meant
> for practice, so they are safe and permitted to scrape. Before scraping any
> real website, always check its `robots.txt` and terms of service, identify
> your scraper with a User-Agent, and add a delay between requests so you don't
> overload the server. This program does all three.

## Libraries used

- [`requests`](https://requests.readthedocs.io/) — downloads the web pages
- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) — parses the HTML

## Files

- `scraper.py` — the interactive scraper
- `test_scraper.py` — tests the parsing logic against sample HTML (no network needed)
- `requirements.txt` — dependencies

## Setup

```bash
pip install -r requirements.txt
```

## How to run

```bash
python scraper.py
```

You'll be asked what to scrape, how many pages, and whether to save a CSV.

Run the tests:

```bash
python test_scraper.py
```

## Example output

```
TITLE                | PRICE  | RATING | AVAILABILITY
-----------------------------------------------------
A Light in the Attic | £51.77 | 3/5    | In stock
Tipping the Velvet   | £53.74 | 5/5    | In stock

  2 record(s) total.
```

## How it works

1. `requests` downloads a page; failures (timeouts, bad status codes) are
   caught so the program doesn't crash.
2. `BeautifulSoup` parses the HTML and CSS selectors pull out the fields.
3. Results are printed as an aligned table and can be exported to CSV.
4. The scraper pauses briefly between pages to stay polite.

## Testing with different websites

The program supports two different sites out of the box (books and quotes),
which is how the "test with different websites" step is covered. The design
makes it easy to add more: add a new entry to the `TARGETS` dictionary with a
URL template and a parser function, and it shows up in the menu automatically.
