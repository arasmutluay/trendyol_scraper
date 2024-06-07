import textwrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import func

from models import session, Product
from analysis import analyze


# PLOT FUNCTIONS

def plot_top_10_most_expensive(session):
    top_10_expensive = session.query(Product).order_by(Product.price.desc()).limit(10).all()
    names = [product.name for product in top_10_expensive]
    prices = [product.price for product in top_10_expensive]
    wrapped_names = ['\n'.join(textwrap.wrap(name, width=30)) for name in names]

    data = pd.DataFrame({
        'Product': wrapped_names,
        'Price': prices
    })

    plt.figure(figsize=(15, 8))

    # For creating a plot
    bar_plot = sns.barplot(x='Price', y='Product', data=data, palette='coolwarm_r', hue='Product')

    # For prices
    for index, value in enumerate(prices):
        bar_plot.text(value, index, f'{value:.2f} TL', color='black', ha="left", va='center')

    plt.xlabel('Price (TL)')
    plt.ylabel('Product')
    plt.title('Top 10 Most Expensive Products')
    plt.tight_layout()
    plt.savefig('./report/plots/top_10_most_expensive.png')
    plt.show()


def plot_top_10_cheapest(session):
    top_10_cheapest = session.query(Product).order_by(Product.price.asc()).limit(10).all()
    names = [product.name for product in top_10_cheapest]
    prices = [product.price for product in top_10_cheapest]
    wrapped_names = ['\n'.join(textwrap.wrap(name, width=30)) for name in names]

    data = pd.DataFrame({
        'Product': wrapped_names,
        'Price': prices
    })

    plt.figure(figsize=(15, 8))

    bar_plot = sns.barplot(x='Price', y='Product', data=data, palette='coolwarm', hue='Product')

    for index, value in enumerate(prices):
        bar_plot.text(value, index, f'{value:.2f} TL', color='black', ha="left", va='center')

    plt.xlabel('Price (TL)')
    plt.ylabel('Product')
    plt.title('Top 10 Cheapest Products')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('./report/plots/top_10_cheapest.png')
    plt.show()


def plot_top_10_most_commented(session):
    top_10_commented = session.query(Product).order_by(Product.comments_count.desc()).limit(10).all()
    names = [product.name for product in top_10_commented]
    comments_count = [product.comments_count for product in top_10_commented]
    wrapped_names = ['\n'.join(textwrap.wrap(name, width=30)) for name in names]

    data = pd.DataFrame({
        'Product': wrapped_names,
        'Comments Count': comments_count
    })

    plt.figure(figsize=(15, 8))

    bar_plot = sns.barplot(x='Comments Count', y='Product', data=data, palette='coolwarm_r', hue='Product')

    for index, value in enumerate(comments_count):
        bar_plot.text(value, index, f'{value}', color='black', ha="left", va='center')

    plt.xlabel('Comments Count')
    plt.ylabel('Product')
    plt.title('Top 10 Most Commented Products')
    plt.tight_layout()
    plt.savefig('./report/plots/top_10_most_commented.png')
    plt.show()


def plot_average_price_by_brand(session):
    avg_prices_by_brand = session.query(Product.brand, func.avg(Product.price)).group_by(Product.brand).all()
    brands = [item[0] for item in avg_prices_by_brand]
    avg_prices = [item[1] for item in avg_prices_by_brand]
    wrapped_brands = ['\n'.join(textwrap.wrap(brand, width=30)) for brand in brands]

    data = pd.DataFrame({
        'Brand': wrapped_brands,
        'Average Price': avg_prices
    }).sort_values(by='Average Price', ascending=False)  # For sorting the bars

    plt.figure(figsize=(30, 30))

    bar_plot = sns.barplot(x='Average Price', y='Brand', data=data, palette='coolwarm_r', hue='Brand')

    # enumerate over average price on DF (since we sorted it there)
    for index, value in enumerate(data['Average Price']):
        bar_plot.text(value, index, f'{value:.2f} TL', color='black', ha="left", va='center')

    plt.xlabel('Average Price (TL)')
    plt.ylabel('Brand')
    plt.title('Average Price by Brand')
    plt.tight_layout()
    plt.savefig('./report/plots/average_price_by_brand.png')
    plt.show()


def plot_number_of_products_per_category(session):
    category_counts = session.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
    categories = [item[0] for item in category_counts]
    counts = [item[1] for item in category_counts]
    wrapped_categories = ['\n'.join(textwrap.wrap(category, width=30)) for category in categories]

    data = pd.DataFrame({
        'Category': wrapped_categories,
        'Count': counts
    }).sort_values(by='Count', ascending=False)

    plt.figure(figsize=(15, 30))

    bar_plot = sns.barplot(x='Count', y='Category', data=data, palette='dark:skyblue', hue='Category')

    for index, value in enumerate(data['Count']):
        bar_plot.text(value, index, f'{value}', color='black', ha="left", va='center')

    plt.xlabel('Number of Products')
    plt.ylabel('Category')
    plt.title('Number of Products per Category')
    plt.tight_layout()
    plt.savefig('./report/plots/products_per_category.png')
    plt.show()


def plot_average_rating_by_category(session):
    avg_ratings_by_category = session.query(Product.category, func.avg(Product.rating)).group_by(Product.category).all()
    categories = [item[0] for item in avg_ratings_by_category]
    avg_ratings = [item[1] for item in avg_ratings_by_category]
    wrapped_categories = ['\n'.join(textwrap.wrap(category, width=30)) for category in categories]

    data = pd.DataFrame({
        'Category': wrapped_categories,
        'Average Rating': avg_ratings
    }).sort_values(by='Average Rating', ascending=False)

    plt.figure(figsize=(30, 30))

    bar_plot = sns.barplot(x='Average Rating', y='Category', data=data, palette='dark:skyblue', hue='Category')

    for index, value in enumerate(data['Average Rating']):
        bar_plot.text(value, index, f'{value:.2f}', color='black', ha="left", va='center')

    plt.xlabel('Average Rating')
    plt.ylabel('Category')
    plt.title('Average Rating by Category')
    plt.tight_layout()
    plt.show()


def create_report(results):
    plot_top_10_most_expensive(session)
    plot_top_10_cheapest(session)
    plot_top_10_most_commented(session)
    plot_average_price_by_brand(session)
    plot_number_of_products_per_category(session)
    plot_average_rating_by_category(session)

    summary_data = {
        "Metric": ["Most Expensive Product"],
        "Product Name": [results["most_expensive"]["name"]],
        "Price": [results["most_expensive"]["price"]],
        "Rating": [results["most_expensive"]["rating"]],
        "Comments Count": [results["most_expensive"]["comments_count"]]
    }
    summary_df = pd.DataFrame(summary_data)

    summary_df.to_csv('./report/report_summary.csv', index=False)
