# Data dictionary

The dataset contains **3,604 raw rows**: 3,600 expected monthly SKU observations (100 illustrative SKUs × 36 months) plus 4 deliberately injected duplicate records. The time series runs from January 2024 to December 2026. All operational values are simulated.

| Field | Definition |
|---|---|
| Date | First day of the reporting month |
| SKU | Synthetic product identifier |
| Brand | Illustrative cosmetics brand label; not brand-reported data |
| Product_Type | Skincare, Makeup or Haircare |
| Subcategory | Product subcategory |
| Price_EUR | Illustrative simulated unit price in euros |
| Demand_Units | Simulated unconstrained demand before stock availability |
| Units_Sold | Fulfilled units; cannot exceed Opening_Stock + Receipts |
| Forecast_Units | Monthly demand forecast |
| Revenue_EUR | Units_Sold × Price_EUR |
| Opening_Stock | Available stock at the start of the month |
| Receipts | Stock received during the month |
| Closing_Stock | Opening_Stock + Receipts − Units_Sold, except for 25 injected inconsistent rows |
| Stock_Target | Target stock calculated from forecast and target coverage |
| Lead_Time_Days | Illustrative supplier lead time |
| Order_Quantity | Illustrative replenishment order quantity |
| Stockout_Flag | 1 when simulated demand exceeds available stock |
| Stock_Cover_Months | Closing_Stock divided by monthly Forecast_Units (denominator floored at 1) |
| Supplier | Illustrative supplier label; blank on 17 injected missing-value rows |
| Data_Quality_Status | OK, Missing, Duplicate or Inconsistent |
| Forecast_Variance | Demand_Units − Forecast_Units |
| Forecast_Accuracy | 1 − absolute forecast error / demand, floored at 0; blank if demand is zero |
| Overstock_Flag | 1 when Closing_Stock exceeds 125% of Stock_Target |
| Low_Cover_Flag | 1 when Stock_Cover_Months is below 0.75 month |
| Stock_Value_EUR | Closing_Stock × Price_EUR |

## Grain and duplicate records
The expected grain is one record per SKU and month. The base panel has 3,600 unique SKU-month combinations. Four duplicate copies are appended as additional rows to create explicit duplicate-key exceptions; the original records remain present.

## Data-quality exceptions
The file deliberately includes:
- 17 rows with a missing Supplier value (status: Missing)
- 4 extra copies of existing SKU + Date keys (status: Duplicate)
- 25 rows where Closing_Stock differs from Opening_Stock + Receipts − Units_Sold (status: Inconsistent)

These are synthetic test cases, not accidental source-data defects.

## Inventory continuity
For each SKU, the next month's Opening_Stock carries forward the previous month's recorded Closing_Stock. This is preserved even after an injected inconsistent closing value, so the stock-balance exception is localized to the affected row rather than propagating into later months.

## Metric interpretation
Forecast accuracy is calculated against Demand_Units rather than Units_Sold. This distinction matters because a stock-out constrains fulfilled sales; using sales alone as a demand proxy would understate demand during stock-out periods.
