import re
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Map word ratings found in HTML to numeric values
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_real_catalog(max_pages=5):
    all_books = []
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    headers = {"User-Agent": "Mozilla/5.0"}

    print(f"Step 1: Scraping {max_pages} catalog pages from books.toscrape.com...")

    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Skipping page {page}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            # 1. Extract Title
            title = article.h3.a["title"]

            # 2. Extract Price (£51.77 -> 51.77 float)
            price_text = article.find("p", class_="price_color").text
            price = float(re.sub(r"[^\d.]", "", price_text))

            # 3. Extract Star Rating class (e.g., "star-rating Three" -> 3)
            rating_classes = article.find("p", class_="star-rating")["class"]
            rating_word = [c for c in rating_classes if c != "star-rating"][0]
            rating = RATING_MAP.get(rating_word, 3)

            # 4. Extract In-Stock Status (1 if in stock, 0 if out)
            availability = article.find("p", class_="instock availability").text.strip()
            in_stock = 1 if "In stock" in availability else 0

            all_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "in_stock": in_stock
            })

    print(f"Extracted {len(all_books)} listings from the live web.")
    return pd.DataFrame(all_books)

def run_pipeline():
    # Scrape 5 pages (100 real books)
    df = scrape_real_catalog(max_pages=5)

    print("Step 2: Cleaning and validating scraped data...")
    df = df.dropna(subset=["price"])
    df = df[df["price"] > 0]

    print("Step 3: Storing records into SQLite relational database...")
    conn = sqlite3.connect("ecommerce_data.db")
    df.to_sql("products", conn, if_exists="replace", index=False)
    conn.close()

    print(f"ETL Complete! {len(df)} records stored in 'ecommerce_data.db'.")

if __name__ == "__main__":
    run_pipeline()