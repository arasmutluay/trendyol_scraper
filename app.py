from scraper import scrape_products
from analysis import analyze
from models import Session, session


def main():
    analyze(session)
    # scrape_products()


if __name__ == "__main__":
    main()
