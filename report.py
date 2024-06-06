import matplotlib.pyplot as plt
import pandas as pd
from models import session
from analysis import analyze


def generate_report():
    with session:
        results = analyze(session)
    return results


def plot_most_expensive_product(data):
    plt.figure(figsize=(6, 4))
    plt.bar(data["name"], data["price"], color='red')
    plt.xlabel('Product')
    plt.ylabel('Price')
    plt.title('Most Expensive Product')
    plt.tight_layout()
    plt.savefig('most_expensive_product.png')
    plt.show()


def create_report(results):
    plot_most_expensive_product(results["most_expensive"])

    summary_data = {
        "Metric": ["Most Expensive Product"],
        "Product Name": [results["most_expensive"]["name"]],
        "Price": [results["most_expensive"]["price"]],
        "Rating": [results["most_expensive"]["rating"]],
        "Comments Count": [results["most_expensive"]["comments_count"]]
    }
    summary_df = pd.DataFrame(summary_data)
    print("SUMMARY: ", summary_df)

    summary_df.to_csv('report_summary.csv', index=False)
