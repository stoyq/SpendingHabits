import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/transactions_ask_claude_edit.csv"
CHART_PATH = "data/processed/visit_count_by_description.png"

def main():
    df = pd.read_csv(INPUT_PATH)

    # Count number of transactions per description
    visit_counts = df["description_normalized"].value_counts()

    # Filter out descriptions with fewer than N visits
    visit_counts = visit_counts[visit_counts >= 5]

    # Sort for nicer plotting
    visit_counts = visit_counts.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))

    visit_counts.plot.bar(ax=ax)

    ax.set_title("Number of Visits by Description (≥ 2 visits)")
    ax.set_xlabel("Description")
    ax.set_ylabel("Number of Transactions")

    ax.set_xticklabels(visit_counts.index, rotation=45, ha="right")

    fig.tight_layout()
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)

    print(f"Chart saved to {CHART_PATH}")

if __name__ == "__main__":
    main()
