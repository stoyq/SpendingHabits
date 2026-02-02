import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_PATH = "data/processed/transactions_ask_claude_edit.csv"
CHART_PATH = "images/transactions_per_month_by_target.png"

def main():
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

    # Convert date to month
    df["month"] = df["date"].dt.to_period("M")

    # Count transactions per month per target
    monthly_counts = (
        df.groupby(["month", "target"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(14, 7))

    monthly_counts.plot.bar(ax=ax, width=0.8)

    ax.set_title("Number of Transactions per Month by Category")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Transactions")

    ax.set_xticklabels(
        [str(m) for m in monthly_counts.index],
        rotation=45,
        ha="right"
    )

    ax.legend(title="Target")

    fig.tight_layout()
    os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)

    print(f"Chart saved to {CHART_PATH}")

if __name__ == "__main__":
    main()
