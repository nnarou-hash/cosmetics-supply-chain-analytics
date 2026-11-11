# Data dictionary

The dataset contains 3,600 monthly SKU observations for 100 illustrative cosmetics products from January 2024 to December 2026. The time series is synthetic, not company-reported data.

| Field | Definition |
|---|---|
| Date | First day of the reporting month |
| SKU | Synthetic product identifier |
| Brand | Illustrative cosmetics brand label |
| Product_Type | Skincare, Makeup or Haircare |
| Subcategory | Product subcategory |
| Price_EUR | Illustrative unit price in euros |
| Demand_Units | Simulated unconstrained demand before stock availability |
| Units_Sold | Fulfilled units; cannot exceed opening stock plus receipts |
| Forecast_Units | Monthly demand forecast |
| Revenue_EUR | Units_Sold × Price_EUR |
| Opening_Stock | Available stock at the start of the month |
| Receipts | Stock received during the month |
| Closing_Stock | Opening_Stock + Receipts − Units_Sold, except injected inconsistent rows |
| Stock_Target | Target stock calculated from forecast and target coverage |
| Lead_Time_Days | Illustrative supplier lead time |
| Order_Quantity | Illustrative replenishment order quantity |
| Stockout_Flag | 1 when simulated demand exceeds available stock |
| Stock_Cover_Months | Closing stock divided by monthly forecast |
| Supplier | Illustrative supplier label; blank on injected missing-value rows |
| Data_Quality_Status | OK, Missing, Duplicate or Inconsistent |
| Forecast_Variance | Demand_Units − Forecast_Units |
| Forecast_Accuracy | 1 − absolute forecast error / demand, floored at 0; blank if demand is zero |
| Overstock_Flag | 1 when closing stock exceeds 125% of target |
| Low_Cover_Flag | 1 when stock coverage is below 0.75 month |
| Stock_Value_EUR | Closing_Stock × Price_EUR |

## Data quality exceptions
The file deliberately includes a small number of exceptions to support validation exercises: missing Supplier values, duplicate SKU + Date keys, and stock-balance inconsistencies. These are synthetic test cases, not accidental source-data defects.

## Metric interpretation
Forecast accuracy is calculated against Demand_Units rather than Units_Sold. This distinction matters when a stock-out constrains fulfilled sales: using sales as the only demand proxy would understate demand during stock-out periods.
