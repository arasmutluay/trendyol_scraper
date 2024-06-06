from scraper import scrape_products
from analysis import analyze
from models import Session, session
from report import create_report, generate_report


def main():
    # analyze(session)
    # scrape_products()
    results = generate_report()
    create_report(results)


if __name__ == "__main__":
    main()
