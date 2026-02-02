import pandas as pd


def read_td_chq(debug: bool = False) -> pd.DataFrame:
    df = pd.read_csv(
        "data/raw/td_chq/accountactivity.csv",
        header=None,
        names=["date", "description", "debit", "credit", "balance"],
    )

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df = df.sort_values("date").reset_index(drop=True)

    print(f"[td_chq] {df.shape[0]} rows, {df['date'].min().date()} to {df['date'].max().date()}")

    if debug:
        print(f"  debit total:  ${df['debit'].sum():,.2f}")
        print(f"  credit total: ${df['credit'].sum():,.2f}")
        counts = df.groupby([df["date"].dt.year, df["date"].dt.month]).size()
        print("  rows per month:")
        for (year, month), count in counts.items():
            print(f"    {year}-{month:02d}: {count}")

    return df
