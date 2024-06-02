from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.wait import WebDriverWait


def scrape_product_details(product_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.trendyol.com" + product_url)

    name = driver.find_element(By.CSS_SELECTOR, "h1.pr-new-br").text.strip()
    print("Name: " + name)
    price = driver.find_element(By.CSS_SELECTOR, "span.prc-dsc").text.strip()
    print("Price: " + price)
    category = driver.find_element(By.CSS_SELECTOR, "div.product-detail-breadcrumb.full-width").text.strip().split('\n')[-1]
    print("Category: " + category)

    # we wait 5 sec because rating and comments load after the static HTML is loaded.
    rating = None  # because some products do not have comment or rating
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.p-reviews-rate-text")))
        rating = driver.find_element(By.CSS_SELECTOR, "p.p-reviews-rate-text").text.strip()
    except (NoSuchElementException, TimeoutException):
        pass
    print("Rating: ", rating)

    comments_count = None
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.p-reviews-comment-count")))
        comments_count = driver.find_element(By.CSS_SELECTOR, "p.p-reviews-comment-count").text.strip().split()[0]
    except (NoSuchElementException, TimeoutException):
        pass
    print("Comments Count: ", comments_count)

    description_items = driver.find_elements(By.CSS_SELECTOR, "div.info-wrapper li")
    description = '\n'.join(item.text.strip() for item in description_items)

    driver.quit()

    return {
        "name": name,
        "category": category,
        "price": price,
        "description": description,
        "rating": rating,
        "comments_count": comments_count
    }


def scrape_products():
    base_url = "https://www.trendyol.com/gida-ve-icecek-x-c103946?pi={}"
    all_products = []
    page_number = 1

    while len(all_products) < 200:
        print(f"Scraping Page Number: {page_number}")

        url = base_url.format(page_number)
        result = requests.get(url)
        doc = BeautifulSoup(result.content, "html.parser")

        product_containers = doc.find_all("div", class_="p-card-chldrn-cntnr card-border")

        for product in product_containers:
            product_url = product.find("a")["href"]  # Get the URL href for each product,
            product_details = scrape_product_details(product_url)  # and pass it to scrape_product_details
            all_products.append(product_details)

            if len(all_products) >= 200:
                break

        page_number += 1

    return all_products


scrape_products()
