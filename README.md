# Cosmetics Supply Chain Analytics

**Portfolio case study | Business & Data Analyst | Cosmetics | Inventory | Forecast | Data Quality**

## Business objective
Build a decision-support view of inventory and demand performance in a cosmetics portfolio. The project connects product-level data, demand forecasting, stock availability and data-quality controls to identify operational risks and support business decisions.

## Dashboard
Open the [interactive three-tab dashboard](dashboard/cosmetics_supply_chain_dashboard.html) directly from this repository (or download the HTML file and open it in a browser).

1. **Executive Overview** — revenue, units sold, forecast accuracy, stock-out rate and category performance.
2. **Inventory & Forecast** — stock cover, target stock, low-cover and overstock indicators, plus a SKU watchlist.
3. **Data Quality** — missing values, duplicate SKU-date keys, stock-balance inconsistencies and validation rules.

## Dataset
- **3,600 monthly records**
- **100 illustrative SKUs** across Skincare, Makeup and Haircare
- **36 months**, January 2024 to December 2026
- **25 fields** covering product attributes, demand, sales, inventory, replenishment, forecast and data quality

CSV: [data/cosmetics_supply_chain_36m.csv](data/cosmetics_supply_chain_36m.csv)  
Data dictionary: [docs/data_dictionary.md](docs/data_dictionary.md)

### Data transparency
The time series is **synthetic and generated for this portfolio project**. It is not actual sales, stock or forecast data from a cosmetics company. The business schema was informed by the public [Supply-Chain-Dataset_Excel](https://github.com/Indu-nb/Supply-Chain-Dataset_Excel) project, but the 36-month history in this repository is simulated.

A small number of test exceptions are deliberately injected: missing supplier values, duplicate SKU + Date keys and stock-balance inconsistencies. They are there to demonstrate validation and data-quality monitoring.

## Key analytical definitions
- **Stock-out:** simulated demand exceeds stock available (opening stock + receipts).
- **Stock cover:** closing stock divided by monthly forecast.
- **Forecast accuracy:** 1 − |demand − forecast| / demand, floored at zero. It is measured against simulated unconstrained demand, not fulfilled sales, so stock-outs do not artificially make the forecast look worse.
- **Low cover:** stock cover below 0.75 month.
- **Overstock:** closing stock above 125% of target stock.

## Repository structure
```text
.
├── README.md
├── data/
│   └── cosmetics_supply_chain_36m.csv
├── dashboard/
│   └── cosmetics_supply_chain_dashboard.html
└── docs/
    └── data_dictionary.md
```

## Next development steps
1. Validate and refine the business rules and KPI definitions.
2. Add reproducible Python/SQL analysis and data-quality checks.
3. Develop deeper SKU, category and seasonality insights.
4. Turn analytical findings into quantified business recommendations.

---
*Created as an educational portfolio project. All business figures in the current version are illustrative.*
