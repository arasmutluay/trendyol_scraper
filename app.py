from scraper import scrape_products
from analysis import (
    get_most_expensive,
    get_cheapest_product,
    get_highest_scores,
    get_most_comments,
    get_average_prices_by_brand
)
from models import Session


def main():
    session = Session()
    most_expensive_product = get_most_expensive(session)
    print(f"Most Expensive Product\n"
          f"Name: {most_expensive_product.name} \n"
          f"Price: {most_expensive_product.price} \n"
          f"Rating: {most_expensive_product.rating} \n"
          f"Comments Count: {most_expensive_product.comments_count} \n")

    cheapest_product = get_cheapest_product(session)
    print(f"Cheapest Product\n"
          f"Name: {cheapest_product.name} \n"
          f"Price: {cheapest_product.price} \n"
          f"Rating: {cheapest_product.rating} \n"
          f"Comments Count: {cheapest_product.comments_count} \n")

    most_commented_product = get_most_comments(session)


    print(f"Most Commented Product\n"
          f"Name: {most_commented_product.name} \n"
          f"Price: {most_commented_product.price} \n"
          f"Rating: {most_commented_product.rating} \n"
          f"Comments Count: {most_commented_product.comments_count} \n")

    highest_scored_product = get_highest_scores(session)
    print(f"Highest Rated Products\n")
    for product in highest_scored_product:
        print(f"Name: {product.name} \n"
              f"Price: {product.price} \n"
              f"Rating: {product.rating} \n"
              f"Comments Count: {product.comments_count} \n")

    session.close()

    #scrape_products()


if __name__ == "__main__":
    main()
