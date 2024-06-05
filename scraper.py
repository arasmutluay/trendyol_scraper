from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.wait import WebDriverWait

from models import Product, Session


def remove_duplicates(products):
    seen = {}
    unique_products = []
    for product in products:
        identifier = (product['name'], product['category'], product['price'])
        if identifier not in seen:
            seen[identifier] = True
            unique_products.append(product)

    return unique_products


def scrape_product_details(product_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f'https://www.trendyol.com{product_url}')

    name = driver.find_element(By.CSS_SELECTOR, "h1.pr-new-br").text.strip()
    print("Name: " + name)
    price = driver.find_element(By.CSS_SELECTOR, "span.prc-dsc").text.strip()
    print("Price: " + price)
    category = \
        driver.find_element(By.CSS_SELECTOR, "div.product-detail-breadcrumb.full-width").text.strip().split('\n')[-1]
    print("Category: " + category)

    # we wait 5 sec because rating and comments load after the static HTML is loaded.
    rating = None  # because some products do not have comment or rating
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.p-reviews-rate-text")))
        rating = driver.find_element(By.CSS_SELECTOR, "p.p-reviews-rate-text").text.strip()
    except (NoSuchElementException, TimeoutException):
        pass
    print("Rating: ", rating)

    comments_count = None
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.p-reviews-comment-count")))
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
    unique_products = []
    page_number = 1

    while len(unique_products) < 30:
        print(f"Scraping Page Number: {page_number}")

        url = base_url.format(page_number)
        result = requests.get(url)
        doc = BeautifulSoup(result.content, "html.parser")

        product_containers = doc.find_all("div", class_="p-card-chldrn-cntnr card-border")

        for product in product_containers:
            product_url = product.find("a")["href"]  # Get the URL href for each product
            product_details = scrape_product_details(product_url)  # and pass it to scrape_product_details

            #if product_details["comments_count"] is None:
                #product_details["comments_count"] = 0

            all_products.append(product_details)
            unique_products = remove_duplicates(all_products)

            if len(unique_products) >= 30:
                break

        page_number += 1

    for product_details in unique_products:
        product_record = Product(
            name=product_details["name"],
            category=product_details["category"],
            price=float(product_details["price"].replace(' TL', '').replace(',', '')),
            description=product_details["description"],
            rating=float(product_details["rating"]) if product_details["rating"] else None,
            comments_count=int(product_details["comments_count"]) if product_details["comments_count"] else 0
        )

        with Session() as session:
            session.add(product_record)
            session.commit()

    print("Unique Length:", len(unique_products))
    print("All Length:", len(all_products))

    return unique_products
