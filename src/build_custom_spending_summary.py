import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_PATH = "data/processed/transactions_ask_claude_edit.csv"
CHART_PATH = "images/grocery_vs_dining_out.png"


def main():
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])
    df = df[df["target"].isin(["dining out", "grocery"])].copy()
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby(["month", "target"])["debit"].sum().unstack(fill_value=0)

    # Consistent column order
    for col in ["grocery", "dining out"]:
        if col not in monthly.columns:
            monthly[col] = 0
    monthly = monthly[["grocery", "dining out"]]

    fig, ax = plt.subplots(figsize=(14, 7))
    monthly.plot.bar(stacked=False, ax=ax, width=0.8, color={"grocery": "#4CAF50", "dining out": "#FF7043"})

    ax.set_title("Monthly Spending: Grocery vs Dining Out", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_xticklabels([str(p) for p in monthly.index], rotation=45, ha="right")
    ax.legend(title="Category")

    fig.tight_layout()
    os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)
    print(f"Chart saved to {CHART_PATH}")


if __name__ == "__main__":
    main()
