"""
Tests for the web scraper's parsing logic
==========================================

These tests run the parsers against small HTML snippets that mirror the real
structure of books.toscrape.com and quotes.toscrape.com. This lets us verify
the parsing logic works without making any network requests.

Run with:  python test_scraper.py
"""

from bs4 import BeautifulSoup

from scraper import parse_books, parse_quotes

# A snippet shaped like a books.toscrape.com listing.
BOOKS_HTML = """
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="x.html" title="A Light in the Attic">A Light in the Attic</a></h3>
  <div class="product_price">
    <p class="price_color">£51.77</p>
    <p class="instock availability">In stock</p>
  </div>
</article>
<article class="product_pod">
  <p class="star-rating Five"></p>
  <h3><a href="y.html" title="Tipping the Velvet">Tipping the Velvet</a></h3>
  <div class="product_price">
    <p class="price_color">£53.74</p>
    <p class="instock availability">In stock</p>
  </div>
</article>
"""

# A snippet shaped like a quotes.toscrape.com page.
QUOTES_HTML = """
<div class="quote">
  <span class="text">"The world as we have created it is a process of our thinking."</span>
  <small class="author">Albert Einstein</small>
  <a class="tag">change</a>
  <a class="tag">deep-thoughts</a>
</div>
<div class="quote">
  <span class="text">"It is our choices that show what we truly are."</span>
  <small class="author">J.K. Rowling</small>
  <a class="tag">abilities</a>
</div>
"""


def run_tests():
    passed = 0
    total = 0

    def check(desc, condition):
        nonlocal passed, total
        total += 1
        if condition:
            print(f"PASS  {desc}")
            passed += 1
        else:
            print(f"FAIL  {desc}")

    # --- Books ---
    books = parse_books(BeautifulSoup(BOOKS_HTML, "html.parser"))
    check("Books: found 2 records", len(books) == 2)
    check("Books: first title correct", books[0]["title"] == "A Light in the Attic")
    check("Books: first price correct", books[0]["price"] == "£51.77")
    check("Books: rating parsed (Three -> 3/5)", books[0]["rating"] == "3/5")
    check("Books: rating parsed (Five -> 5/5)", books[1]["rating"] == "5/5")
    check("Books: availability captured", books[0]["availability"] == "In stock")

    # --- Quotes ---
    quotes = parse_quotes(BeautifulSoup(QUOTES_HTML, "html.parser"))
    check("Quotes: found 2 records", len(quotes) == 2)
    check("Quotes: author correct", quotes[0]["author"] == "Albert Einstein")
    check("Quotes: tags joined", quotes[0]["tags"] == "change, deep-thoughts")
    check("Quotes: single tag handled", quotes[1]["tags"] == "abilities")

    print(f"\n{passed}/{total} tests passed.")


if __name__ == "__main__":
    run_tests()
