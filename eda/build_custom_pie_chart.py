import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_PATH = "data/processed/transactions_ask_claude_edit.csv"
CHART_PATH = "images/spending_pie.png"

def main():
    df = pd.read_csv(INPUT_PATH)

    # If debit values are negative, flip them
    df["debit"] = df["debit"].abs()

    # Aggregate spending by description
    summary = (
        df.groupby("description_normalized")["debit"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        summary.values,
        labels=summary.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Spending Breakdown by Description in 2025")

    ax.axis("equal")  # makes the pie circular

    fig.tight_layout()
    os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)

    print(f"Chart saved to {CHART_PATH}")

if __name__ == "__main__":
    main()
