#!/usr/bin/env python3
"""Validate the synthetic cosmetics supply-chain dataset.

Run from the repository root:
    python src/validate_data.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cosmetics_supply_chain_36m.csv"


def as_int(row: dict[str, str], field: str) -> int:
    return int(float(row[field]))


def as_float(row: dict[str, str], field: str) -> float:
    return float(row[field])


def main() -> int:
    with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    required = {
        "Date", "SKU", "Price_EUR", "Demand_Units", "Units_Sold",
        "Forecast_Units", "Revenue_EUR", "Opening_Stock", "Receipts",
        "Closing_Stock", "Stockout_Flag", "Stock_Cover_Months",
        "Supplier", "Data_Quality_Status", "Forecast_Variance",
        "Forecast_Accuracy",
    }
    missing_columns = required.difference(rows[0].keys() if rows else set())
    if missing_columns:
        raise AssertionError(f"Missing columns: {sorted(missing_columns)}")

    seen: set[tuple[str, str]] = set()
    canonical: list[dict[str, str]] = []
    duplicate_rows = 0
    for row in rows:
        key = (row["SKU"], row["Date"])
        if key in seen:
            duplicate_rows += 1
        else:
            seen.add(key)
            canonical.append(row)

    checks: list[tuple[str, int, int]] = []
    checks.append(("raw row count", len(rows), 3604))
    checks.append(("canonical SKU-month count", len(canonical), 3600))
    checks.append(("distinct SKU count", len({r["SKU"] for r in rows}), 100))
    checks.append(("monthly period count", len({r["Date"] for r in rows}), 36))
    checks.append(("duplicate rows beyond first occurrence", duplicate_rows, 4))
    checks.append(("missing Supplier values", sum(not r["Supplier"].strip() for r in rows), 17))

    balance_errors = 0
    revenue_errors = 0
    sold_cap_errors = 0
    stockout_flag_errors = 0
    variance_errors = 0
    accuracy_errors = 0
    cover_errors = 0
    negative_quantity_errors = 0

    for row in rows:
        opening = as_int(row, "Opening_Stock")
        receipts = as_int(row, "Receipts")
        sold = as_int(row, "Units_Sold")
        closing = as_int(row, "Closing_Stock")
        demand = as_int(row, "Demand_Units")
        forecast = as_int(row, "Forecast_Units")
        price = as_float(row, "Price_EUR")
        revenue = as_float(row, "Revenue_EUR")
        available = opening + receipts

        balance_errors += int(opening + receipts - sold != closing)
        revenue_errors += int(abs(revenue - sold * price) > 0.011)
        sold_cap_errors += int(sold > available)
        stockout_flag_errors += int(as_int(row, "Stockout_Flag") != int(demand > available))
        variance = demand - forecast
        variance_errors += int(as_int(row, "Forecast_Variance") != variance)

        actual_accuracy = row["Forecast_Accuracy"].strip()
        if demand == 0:
            accuracy_errors += int(bool(actual_accuracy))
        else:
            expected_accuracy = max(0.0, 1.0 - abs(variance) / demand)
            accuracy_errors += int(
                not actual_accuracy
                or abs(float(actual_accuracy) - expected_accuracy) > 1e-6
            )

        expected_cover = round(closing / max(forecast, 1), 2)
        cover_errors += int(abs(as_float(row, "Stock_Cover_Months") - expected_cover) > 0.011)

        for field in ("Price_EUR", "Demand_Units", "Units_Sold", "Forecast_Units",
                      "Opening_Stock", "Receipts", "Closing_Stock", "Revenue_EUR"):
            negative_quantity_errors += int(as_float(row, field) < 0)

    checks.extend([
        ("stock-balance exceptions", balance_errors, 25),
        ("revenue calculation exceptions", revenue_errors, 0),
        ("sales above available stock", sold_cap_errors, 0),
        ("stock-out flag exceptions", stockout_flag_errors, 0),
        ("forecast variance exceptions", variance_errors, 0),
        ("forecast accuracy exceptions", accuracy_errors, 0),
        ("stock cover calculation exceptions", cover_errors, 0),
        ("negative values in core numeric fields", negative_quantity_errors, 0),
    ])

    by_sku: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in canonical:
        by_sku[row["SKU"]].append(row)
    continuity_errors = 0
    for sku_rows in by_sku.values():
        sku_rows.sort(key=lambda item: datetime.strptime(item["Date"], "%Y-%m-%d"))
        for previous, current in zip(sku_rows, sku_rows[1:]):
            continuity_errors += int(
                as_int(current, "Opening_Stock") != as_int(previous, "Closing_Stock")
            )
    checks.append(("inventory continuity exceptions", continuity_errors, 0))

    status_counts = Counter(row["Data_Quality_Status"] for row in rows)
    expected_status = {"OK": 3558, "Missing": 17, "Duplicate": 4, "Inconsistent": 25}
    for status, expected in expected_status.items():
        checks.append((f"status count: {status}", status_counts.get(status, 0), expected))

    print("COSMETICS SUPPLY CHAIN — DATA VALIDATION")
    print("-" * 58)
    failed = False
    for name, actual, expected in checks:
        passed = actual == expected
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {actual} (expected {expected})")
        failed |= not passed

    if failed:
        print("\nValidation failed. Review the exceptions above.", file=sys.stderr)
        return 1
    print("\nAll validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
