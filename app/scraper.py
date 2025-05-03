from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3

BASE_URL = "https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts&page={page}"
DB_PATH = "products.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            rating TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_product(name, price, rating):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, rating) VALUES (?, ?, ?)", (name, price, rating))
    conn.commit()
    conn.close()

def scrape_flipkart():
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # Uncomment when stable
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    for page in range(1, 11):  # pages 1 to 10
        url = BASE_URL.format(page=page)
        print(f"\nScraping page {page}: {url}")
        driver.get(url)

        try:
            # Wait for product grid to load
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._1xHGtK._373qXS")))
        except Exception as e:
            print(f"[!] Timeout waiting for products on page {page}: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_containers = soup.select("div._1xHGtK._373qXS")

        if not product_containers:
            print("[!] No products found on this page.")
            continue

        print(f"Found {len(product_containers)} products on page {page}")

        for container in product_containers:
            name_tag = container.select_one("a.IRpwTa")
            price_tag = container.select_one("div._30jeq3")
            rating_tag = container.select_one("div._3LWZlK")

            name = name_tag.text.strip() if name_tag else "N/A"
            price = price_tag.text.strip() if price_tag else "N/A"
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            print(f"- {name} | {price} | Rating: {rating}")
            save_product(name, price, rating)

    driver.quit()

if __name__ == "__main__":
    init_db()
    scrape_flipkart()
