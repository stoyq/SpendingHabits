import pandas as pd
import os
import re

MAP_PATH = "data/description_map.csv"


def normalize_merchant(desc: str) -> str:
    s = desc.strip()
    s = re.sub(r"\s+_F$", "", s)
    if re.match(r"AMZN Mktp CA\*", s):
        return "Amazon Marketplace"
    if re.match(r"Amazon\.ca\*", s):
        return "Amazon.ca"
    if re.match(r"SEND E-TFR \*\*\*", s):
        return "E-Transfer Sent"
    if re.match(r"E-TRANSFER \*\*\*", s):
        return "E-Transfer Received"
    if re.match(r"STARBUCKS", s, re.IGNORECASE):
        return "Starbucks"
    if re.match(r"MCDONALD'S", s, re.IGNORECASE):
        return "McDonald's"
    if re.match(r"LONDON DRUGS", s, re.IGNORECASE):
        return "London Drugs"
    if re.match(r"TD ATM", s):
        return "TD ATM"
    return s


def build_description_map(visa: pd.DataFrame, chq: pd.DataFrame, debug: bool = False) -> pd.DataFrame:
    all_descriptions = sorted(
        set(visa["description"].unique()) | set(chq["description"].unique())
    )

    if os.path.exists(MAP_PATH) and os.path.getsize(MAP_PATH) > 0:
        existing = pd.read_csv(MAP_PATH)
        if "subcategory" not in existing.columns:
            existing["subcategory"] = "uncategorized"
        existing_set = set(existing["description"])
    else:
        existing = pd.DataFrame(columns=["description", "merchant", "category", "subcategory"])
        existing_set = set()

    new_rows = []
    for desc in all_descriptions:
        if desc not in existing_set:
            new_rows.append({
                "description": desc,
                "merchant": normalize_merchant(desc),
                "category": "uncategorized",
                "subcategory": "uncategorized",
            })

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = existing

    combined = combined.sort_values(["merchant", "description"]).reset_index(drop=True)
    combined.to_csv(MAP_PATH, index=False)

    print(f"[description_map] {len(combined)} descriptions, {len(new_rows)} new, "
          f"{combined['merchant'].nunique()} merchants")

    if debug:
        n_visa = visa["description"].nunique()
        n_chq = chq["description"].nunique()
        print(f"  unique descriptions — visa: {n_visa}, chq: {n_chq}, combined: {len(all_descriptions)}")
        print(f"  existing in map: {len(existing_set)}, newly added: {len(new_rows)}")
        cat_counts = combined["category"].value_counts()
        print("  rows per category:")
        for cat, count in cat_counts.items():
            print(f"    {cat}: {count}")
        uncategorized = (combined["category"] == "uncategorized").sum()
        if uncategorized:
            print(f"  WARNING: {uncategorized} rows still uncategorized")
        normalized = combined[combined["description"] != combined["merchant"]]
        print(f"  normalized merchants: {len(normalized)} (description != merchant)")

    return combined
