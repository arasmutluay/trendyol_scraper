from models import Product
from sqlalchemy import func


def print_product_details(product, title):
    if isinstance(product, list):
        for p in product:
            print(f"{title}\n"
                  f"Name: {p.name} \n"
                  f"Price: {p.price} \n"
                  f"Rating: {p.rating} \n"
                  f"Comments Count: {p.comments_count} \n")
    else:
        print(f"{title}\n"
              f"Name: {product.name} \n"
              f"Price: {product.price} \n"
              f"Rating: {product.rating} \n"
              f"Comments Count: {product.comments_count} \n")


# For returning the product's details for analyze functions. Converts Product to a dictionary
def get_product_details(product):
    return {
        "name": product.name,
        "price": product.price,
        "rating": product.rating,
        "comments_count": product.comments_count
    }


def analyze_most_expensive(session):
    most_expensive_product = session.query(Product).order_by(Product.price.desc()).first()
    print_product_details(most_expensive_product, "Most expensive product: ")

    return get_product_details(most_expensive_product)


def analyze_cheapest(session):
    cheapest_product = session.query(Product).order_by(Product.price).first()
    print_product_details(cheapest_product, "Cheapest product: ")

    return get_product_details(cheapest_product)


# def analyze_highest_scored(session):
#     highest_rating = session.query(func.max(Product.rating)).scalar()
#     highest_rated_product = session.query(Product).filter(Product.rating == highest_rating).all()
#
#     print_product_details(highest_rated_product, "Highest rated product: ")
#
#     return highest_rated_product

def analyze_highest_scored(session):
    highest_rating = session.query(func.max(Product.rating)).scalar()
    highest_rated_products = session.query(Product).filter(Product.rating == highest_rating).all()

    for product in highest_rated_products:
        print_product_details(product, "Highest rated product: ")

    return [get_product_details(product) for product in highest_rated_products]


def analyze_most_commented(session):
    most_commented_product = session.query(Product).order_by(Product.comments_count.desc()).first()
    print_product_details(most_commented_product, "Most commented product: ")

    return get_product_details(most_commented_product)


def analyze_average_prices_by_brand(session):
    average_prices = session.query(Product.brand, func.avg(Product.price)).group_by(Product.brand).all()
    print("Average Prices by Brand\n")
    for brand, avg_price in average_prices:
        print(f"Brand: {brand} - Average Price: {avg_price:.2f}")

    return average_prices


def analyze(session):
    results = {
        "most_expensive": analyze_most_expensive(session),
        "cheapest": analyze_cheapest(session),
        "highest_scored": analyze_highest_scored(session),
        "most_commented": analyze_most_commented(session),
        "average_prices_by_brand": analyze_average_prices_by_brand(session)
    }
    return results
