# Cosmetics Supply Chain Analytics

**Portfolio case study | Business & Data Analyst | Cosmetics | Inventory | Forecast | Data Quality**

## Business objective
Build a decision-support view of inventory and demand performance in a cosmetics portfolio. The project connects product-level data, demand forecasting, stock availability and data-quality controls to identify operational risks and support business decisions.

## Dashboard
The [interactive three-tab dashboard](dashboard/cosmetics_supply_chain_dashboard.html) is provided as a self-contained HTML file. Download it and open it in a web browser.

1. **Executive Overview** — revenue, units sold, forecast accuracy, stock-out rate and category performance.
2. **Inventory & Forecast** — stock cover, target stock, low-cover and overstock indicators, demand versus forecast, and a SKU watchlist.
3. **Data Quality** — missing supplier values, duplicate SKU-month keys, stock-balance inconsistencies and validation rules.

## Dataset
- **3,604 raw records**, including 4 deliberately duplicated rows
- **3,600 expected unique SKU-month combinations** (100 illustrative SKUs × 36 months)
- **36 monthly periods**, January 2024 to December 2026
- **25 fields** covering product attributes, demand, sales, inventory, replenishment, forecast and data quality

CSV: [data/cosmetics_supply_chain_36m.csv](data/cosmetics_supply_chain_36m.csv)  
Data dictionary: [docs/data_dictionary.md](docs/data_dictionary.md)  
Data-quality audit: [docs/data_quality_audit.md](docs/data_quality_audit.md)  
Validation script: [src/validate_data.py](src/validate_data.py)

### Data transparency
The time series is **synthetic and generated for this portfolio project**. It is not actual sales, stock or forecast data from a cosmetics company. Product labels, brand labels, prices, transactions and supply-chain metrics are illustrative. The business schema was informed by the public [Supply-Chain-Dataset_Excel](https://github.com/Indu-nb/Supply-Chain-Dataset_Excel) project, but the 36-month history in this repository is simulated.

The dataset intentionally includes:
- 17 missing supplier values
- 4 additional duplicate SKU-month records
- 25 stock-balance inconsistencies

These are inserted test cases for demonstrating data validation. They are not real source-data defects.

## KPI definitions
- **Revenue:** Units_Sold × Price_EUR.
- **Stock-out:** simulated demand exceeds stock available (Opening_Stock + Receipts).
- **Stock cover:** Closing_Stock divided by Forecast_Units.
- **Forecast accuracy:** 1 − |Demand_Units − Forecast_Units| / Demand_Units, floored at zero. It is measured against simulated unconstrained demand, not fulfilled sales, so stock-outs do not artificially make the forecast look worse. The portfolio headline is the mean of non-null SKU-month accuracy values on the deduplicated dataset.
- **Low cover:** stock cover below 0.75 month.
- **Overstock:** Closing_Stock above 125% of Stock_Target.
- **Stock-balance check:** Opening_Stock + Receipts − Units_Sold must equal Closing_Stock.

## Repository structure
```text
.
├── README.md
├── data/
│   └── cosmetics_supply_chain_36m.csv
├── dashboard/
│   └── cosmetics_supply_chain_dashboard.html
├── docs/
│   ├── data_dictionary.md
│   └── data_quality_audit.md
└── src/
    └── validate_data.py
```

## Next development steps
1. Add reproducible exploratory analysis and SKU/category insights.
2. Refine replenishment and demand-planning scenarios.
3. Turn analytical findings into quantified business recommendations.
4. Optionally add a SQL model and a presentation of the case study.

---
*Educational portfolio project. All business figures are illustrative and synthetic.*
