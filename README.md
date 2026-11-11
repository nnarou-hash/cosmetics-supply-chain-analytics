# Cosmetics Supply Chain Analytics

Portfolio project: Business & Data Analytics applied to the cosmetics supply chain.

## Project scope
This project explores inventory performance, demand forecasting, sales performance and data quality through a three-tab dashboard:

1. **Executive Overview** — revenue, units sold, forecast accuracy, stock-out rate and category performance.
2. **Inventory & Forecast** — inventory levels, forecast, stock coverage, target stock and operational risks.
3. **Data Quality** — missing values, duplicate flags, consistency checks and data-quality monitoring.

## Dataset and transparency
The project contains 3,600 monthly observations covering 100 illustrative SKUs from January 2024 to December 2026.

**Important:** the 36-month time series is simulated for portfolio and demonstration purposes. It is not actual sales or inventory data from a cosmetics company. The product and supply-chain schema was inspired by the public [Supply-Chain-Dataset_Excel](https://github.com/Indu-nb/Supply-Chain-Dataset_Excel) repository. Simulated and injected quality exceptions are identified as such in the project documentation.

## Repository structure

```text
.
├── README.md
├── data/
│   └── cosmetics_supply_chain_36m.csv
├── dashboard/
│   └── cosmetics_supply_chain_dashboard.html
└── workbook/
    └── cosmetics_supply_chain_36m.xlsx
```

## How to use
- Open `dashboard/cosmetics_supply_chain_dashboard.html` in a browser to explore the dashboard.
- Use the CSV in `data/` for analysis in Python, SQL, Power BI or Excel.
- Use the Excel workbook for a multi-sheet view of the fact table, product dimension, monthly KPIs and data-quality summary.

## Analytical topics
- Inventory coverage and stock-out risk
- Forecast versus actual demand
- Overstock and low-coverage flags
- Revenue and units sold by category
- SKU-level data quality and stock-balance reconciliation

## Data lineage and limitations
The current version is a **synthetic analytical case study** based on a cosmetics-oriented supply-chain schema. It is designed to demonstrate data modelling, KPI definition, data validation and dashboarding. It must not be represented as real company performance. The next development step is to strengthen the business rules, validate KPI definitions, and add reproducible analysis and documented recommendations.
