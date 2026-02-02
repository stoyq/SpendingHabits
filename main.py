from src.read_td_visa import read_td_visa
from src.read_td_chq import read_td_chq
from src.build_description_map import build_description_map
from src.build_processed import build_processed
from src.build_spending_summary import build_spending_summary

# ── Toggle steps on/off ──────────────────────────────────────────────
STEPS = {
    "read_td_visa": True,
    "read_td_chq": True,
    "build_description_map": True,
    "build_processed": True,
    "build_spending_summary": True,
}

DEBUG = True  # extra detail per step (rows per month, totals, etc.)
CHART_MAX_DEBIT = 200  # exclude transactions above this from the chart (None to include all)
SUMMARY_DATE_FROM = "2025-01-01"  # start date for spending summary (None for no limit)
SUMMARY_DATE_TO = "2025-12-31"    # end date for spending summary (None for no limit)

# ── Pipeline ─────────────────────────────────────────────────────────
visa, chq = None, None

if STEPS["read_td_visa"]:
    visa = read_td_visa(debug=DEBUG)

if STEPS["read_td_chq"]:
    chq = read_td_chq(debug=DEBUG)

if STEPS["build_description_map"]:
    desc_map = build_description_map(visa, chq, debug=DEBUG)

if STEPS["build_processed"]:
    processed = build_processed(visa, chq, desc_map, debug=DEBUG)

if STEPS["build_spending_summary"]:
    spending = build_spending_summary(processed, debug=DEBUG, chart_max_debit=CHART_MAX_DEBIT, date_from=SUMMARY_DATE_FROM, date_to=SUMMARY_DATE_TO)
