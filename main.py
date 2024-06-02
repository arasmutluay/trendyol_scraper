from bs4 import BeautifulSoup
import requests

url = "https://www.trendyol.com/gida-ve-icecek-x-c103946?pi={}"

all_products = []

page_number = 1
while len(all_products) < 200:
    url = url.format(page_number)
    result = requests.get(url)
    doc = BeautifulSoup(result.content, "html.parser")

    product_containers = doc.find_all("div", class_="p-card-chldrn-cntnr card-border")

    for product in product_containers:
        name_tag = product.find("span", class_="prdct-desc-cntnr-ttl")
        description_tag = product.find("span", class_="prdct-desc-cntnr-name")
        price_tag = product.find("div", class_="prc-box-dscntd")

        if name_tag and description_tag and price_tag:
            name = name_tag.get_text(strip=True) + " " + description_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            all_products.append({"name": name, "price": price})

        if len(all_products) >= 200:
            break

    page_number += 1

for i, product in enumerate(all_products[:200], 1):
    print(f"{i}. Name: {product['name']}, Price: {product['price']}")
