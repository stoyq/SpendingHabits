import pandas as pd
import glob


def read_td_visa(debug: bool = False) -> pd.DataFrame:
    files = glob.glob("data/raw/td_visa/accountactivity_*.csv")

    df = pd.concat(
        [pd.read_csv(f, header=None, names=["date", "description", "debit", "credit", "balance"]) for f in files],
        ignore_index=True,
    )

    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df = df.sort_values("date").reset_index(drop=True)

    print(f"[td_visa] {df.shape[0]} rows, {df['date'].min().date()} to {df['date'].max().date()}")

    if debug:
        print(f"  files matched: {len(files)}")
        print(f"  debit total:  ${df['debit'].sum():,.2f}")
        print(f"  credit total: ${df['credit'].sum():,.2f}")
        counts = df.groupby([df["date"].dt.year, df["date"].dt.month]).size()
        print("  rows per month:")
        for (year, month), count in counts.items():
            print(f"    {year}-{month:02d}: {count}")

    return df
