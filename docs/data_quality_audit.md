# Data quality audit — V1.1

## Dataset profile
- Raw row count: 3,604
- Expected unique SKU-month combinations: 3,600
- Distinct SKUs: 100
- Monthly periods: 36 (2024-01 to 2026-12)
- Duplicate SKU-month rows beyond first occurrence: 4
- Missing Supplier values: 17
- Stock-balance exceptions: 25

## Validation controls

| Control | Expected result |
|---|---:|
| Raw record count | 3,604 |
| Unique SKU-month combinations | 3,600 |
| Duplicate rows beyond first occurrence | 4 |
| Missing Supplier values | 17 |
| Stock-balance exceptions | 25 (deliberately injected) |
| Revenue = Units_Sold × Price_EUR | 0 exceptions |
| Units_Sold ≤ Opening_Stock + Receipts | 0 exceptions |
| Stockout_Flag matches demand > available stock | 0 exceptions |
| Forecast_Variance = Demand_Units − Forecast_Units | 0 exceptions |
| Forecast_Accuracy formula | 0 exceptions |
| Stock_Cover_Months formula | 0 exceptions |
| Inventory continuity between consecutive months | 0 exceptions in canonical records |

## Interpretation
The 25 stock-balance exceptions, 17 missing supplier values and 4 duplicate rows are deliberate test cases. A successful validation run should detect exactly those exceptions, while all other arithmetic and continuity checks should pass.

The dashboard's sales, demand, inventory and SKU aggregates are calculated on the canonical 3,600 SKU-month observations (first occurrence per SKU + Date). The Data Quality tab counts all 3,604 raw records so that duplicate records remain visible.

## Reproducibility
Run from the repository root:

```bash
python src/validate_data.py
```

The script exits with a non-zero status if an unexpected check fails.
