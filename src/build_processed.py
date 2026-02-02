import pandas as pd
import os

PROCESSED_PATH = "data/processed/transactions.csv"


def build_processed(visa: pd.DataFrame, chq: pd.DataFrame, desc_map: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    visa = visa.assign(data_source="td_visa")
    chq = chq.assign(data_source="td_chq")
    combined = pd.concat([visa, chq], ignore_index=True)

    merged = combined.merge(desc_map[["description", "merchant", "category", "subcategory"]], on="description", how="left")

    merged = merged.rename(columns={"merchant": "description_normalized"})
    df = merged[["date", "data_source", "description", "description_normalized", "debit", "credit", "category", "subcategory"]].copy()
    df = df.sort_values("date").reset_index(drop=True)

    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"[build_processed] {len(df)} rows, {df['date'].min().date()} to {df['date'].max().date()}")

    if debug:
        print(f"  debit total:  ${df['debit'].sum():,.2f}")
        print(f"  credit total: ${df['credit'].sum():,.2f}")
        missing = df["category"].isna() | (df["category"] == "")
        if missing.any():
            print(f"  WARNING: {missing.sum()} rows with missing category")
        cat_counts = df["category"].value_counts()
        print("  rows per category:")
        for cat, count in cat_counts.items():
            print(f"    {cat}: {count}")
        counts = df.groupby([df["date"].dt.year, df["date"].dt.month]).size()
        print("  rows per month:")
        for (year, month), count in counts.items():
            print(f"    {year}-{month:02d}: {count}")

    return df
