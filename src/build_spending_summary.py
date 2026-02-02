import pandas as pd
import matplotlib.pyplot as plt
import os

SUMMARY_PATH = "data/processed/spending_by_category.csv"
CHART_PATH = "images/monthly_spending_by_category.png"


def build_spending_summary(processed: pd.DataFrame, debug: bool = False, chart_max_debit: float | None = None, date_from: str | None = None, date_to: str | None = None) -> pd.DataFrame:
    if date_from is not None:
        processed = processed[processed["date"] >= pd.Timestamp(date_from)]
    if date_to is not None:
        processed = processed[processed["date"] <= pd.Timestamp(date_to)]

    summary = (
        processed
        .groupby(["category", "subcategory"], dropna=False)
        .agg(
            total_debit=("debit", "sum"),
            total_credit=("credit", "sum"),
            transactions=("debit", "size"),
        )
        .sort_values("total_debit", ascending=False)
        .reset_index()
    )

    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
    summary.to_csv(SUMMARY_PATH, index=False)

    cat_summary = (
        summary.groupby("category")
        .agg(total_debit=("total_debit", "sum"), total_credit=("total_credit", "sum"), transactions=("transactions", "sum"))
        .sort_values("total_debit", ascending=False)
    )

    print(f"[spending_summary] {len(summary)} subcategories across {len(cat_summary)} categories, "
          f"total spending: ${summary['total_debit'].sum():,.2f}")
    print("  spending per category:")
    for cat, row in cat_summary.iterrows():
        print(f"    {cat}: ${row['total_debit']:,.2f} ({int(row['transactions'])} txns)")

    if debug:
        print(f"  total credits: ${summary['total_credit'].sum():,.2f}")
        print(f"  top 10 subcategories by debit:")
        for _, row in summary.head(10).iterrows():
            print(f"    {row['category']} > {row['subcategory']}: ${row['total_debit']:,.2f} ({int(row['transactions'])} txns)")

    _plot_monthly_stacked_bar(processed, max_debit=chart_max_debit)

    return summary


def _plot_monthly_stacked_bar(processed: pd.DataFrame, max_debit: float | None = None) -> None:
    EXCLUDE = {"Financial", "Transfer", "Income"}
    df = processed[~processed["category"].isin(EXCLUDE)].copy()
    if max_debit is not None:
        df = df[df["debit"].isna() | (df["debit"] <= max_debit)]
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby(["month", "category"])["debit"].sum().unstack(fill_value=0)

    # Sort categories by total spend descending so biggest slices are at bottom
    cat_order = monthly.sum().sort_values(ascending=False).index
    monthly = monthly[cat_order]

    fig, ax = plt.subplots(figsize=(14, 7))
    monthly.plot.bar(stacked=True, ax=ax, width=0.8)

    ax.set_title("Monthly Spending by Category", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_xticklabels([str(p) for p in monthly.index], rotation=45, ha="right")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)

    fig.tight_layout()
    os.makedirs(os.path.dirname(CHART_PATH), exist_ok=True)
    fig.savefig(CHART_PATH, dpi=150)
    plt.close(fig)
    print(f"[spending_summary] chart saved to {CHART_PATH}")
