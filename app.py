from scraper import scrape_products
from analysis import analyze
from models import Session, session
from report import create_report


def main():
    # analyze(session)
    # scrape_products()
    create_report(analyze(session))


if __name__ == "__main__":
    main()
