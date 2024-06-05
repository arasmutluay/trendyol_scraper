from models import Product
from sqlalchemy import func


def get_most_expensive(session):
    return session.query(Product).order_by(Product.price.desc()).first()


def get_cheapest_product(session):
    return session.query(Product).order_by(Product.price).first()


def get_highest_scores(session):
    highest_rating = session.query(func.max(Product.rating)).scalar()

    return session.query(Product).filter(Product.rating == highest_rating).all()


def get_most_comments(session):
    return session.query(Product).order_by(Product.comments_count.desc()).first()


def get_average_prices_by_brand(session):
    avg_prices_by_brand = session.query(
        Product.brand,
        func.avg(Product.price).label('average_price')
    ).group_by(Product.brand).all()

    return avg_prices_by_brand
