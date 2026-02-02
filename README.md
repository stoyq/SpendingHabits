# SpendingHabits

A personal finance pipeline that reads TD bank transaction CSVs, normalizes merchant descriptions, categorizes spending, and generates summary reports and charts.

**[Exploratory Charts (EDA)](EDA.md)**

## Project Structure

```
SpendingHabits/
├── main.py                              # Pipeline entry point with configuration
├── src/
│   ├── read_td_visa.py                  # Reads TD Visa CSV exports
│   ├── read_td_chq.py                   # Reads TD Chequing CSV export
│   ├── build_description_map.py         # Normalizes merchants and maps categories
│   ├── build_processed.py               # Combines sources into one transactions file
│   ├── build_spending_summary.py        # Aggregates spending and generates charts
│   ├── build_custom_spending_summary.py # Grocery vs dining out bar chart (standalone)
│   ├── build_custom_pie_chart.py        # Spending pie chart by merchant (standalone)
│   ├── build_custom_count_chart.py      # Visit count bar chart by merchant (standalone)
│   └── build_custom_visits_chart.py     # Monthly transaction count by target (standalone)
├── data/
│   ├── raw/
│   │   ├── td_visa/                     # TD Visa CSV exports (multiple files)
│   │   └── td_chq/                      # TD Chequing CSV export
│   ├── processed/                       # Pipeline outputs (CSVs and PNGs)
│   └── description_map.csv             # Merchant normalization and category mapping
└── .gitignore
```

## Pipeline

Run the full pipeline:

```
python main.py
```

### Steps

1. **read_td_visa** - Reads all TD Visa CSV files from `data/raw/td_visa/`
2. **read_td_chq** - Reads the TD Chequing CSV from `data/raw/td_chq/`
3. **build_description_map** - Loads or creates `data/description_map.csv`, normalizing raw transaction descriptions into merchant names and assigning category/subcategory
4. **build_processed** - Merges visa + chequing transactions with the description map, outputs `data/processed/transactions.csv`
5. **build_spending_summary** - Aggregates spending by category/subcategory, outputs `data/processed/spending_by_category.csv` and a monthly stacked bar chart

Each step can be toggled on/off via the `STEPS` dict in `main.py`.

### Configuration (`main.py`)

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `True` | Print extra detail per step |
| `CHART_MAX_DEBIT` | `200` | Exclude transactions above this amount from the chart (`None` to include all) |
| `SUMMARY_DATE_FROM` | `"2025-01-01"` | Start date filter for spending summary (`None` for no limit) |
| `SUMMARY_DATE_TO` | `"2025-12-31"` | End date filter for spending summary (`None` for no limit) |

## Standalone Scripts

These scripts run independently from the main pipeline and read from `data/processed/transactions_ask_claude_edit.csv`:

```bash
python src/build_custom_spending_summary.py   # Grocery vs dining out monthly bar chart
python src/build_custom_pie_chart.py          # Spending pie chart by merchant
python src/build_custom_count_chart.py        # Visit count by merchant (>= 5 visits)
python src/build_custom_visits_chart.py       # Monthly transaction count by target
```

## EDA

See [EDA.md](EDA.md) for exploratory charts.

## Dependencies

- Python 3.12+
- pandas
- matplotlib
