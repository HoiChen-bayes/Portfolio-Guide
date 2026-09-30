# F2_月度表现.csv

[Download the complete file](<../outputs/F2_月度表现.csv>) · [Back to data guide](../README.md)

**Purpose:** Measure monthly commercial performance.

**Rows:** 16. **Fields:** 10. CSV files store text; the type rules below describe how to interpret the values during import. The images render the actual first five records, with wide tables split into consecutive column panels. They are data excerpts, not screenshots of the Excel application.

![Actual records — F2_月度表现](images/8bdc1bd1cc-1.png)

![Actual records — F2_月度表现](images/8bdc1bd1cc-2.png)

## Fields and formats

| Field | Meaning / use | Import and display | Example |
|---|---|---|---|
| Period | Grouping, filter or comparison label for period. | Date / period; parse stated order, display YYYY-MM-DD or YYYY-MM | 2013-09 |
| Units Sold | Sample units sold; fractional values are preserved. | Numeric; counts as whole numbers, units/durations retain needed decimals | 50601.0 |
| Gross Sales | Units sold × sale price, before discounts. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 4729736.0 |
| Discounts | Discount amount deducted from gross sales. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 245735.97 |
| Sales | Net sales after discounts. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 4484000.03 |
| COGS | Cost of goods sold from the source sample. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 3720397.0 |
| Profit | Sales less COGS; not full company net profit. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 763603.03 |
| Margin | Aggregate profit divided by aggregate sales. | Decimal ratio; display as 0.0% (0.10 = 10%) | 0.17029505461443986 |
| Discount rate | Total discounts divided by total gross sales. | Decimal ratio; display as 0.0% (0.10 = 10%) | 0.051955536207517715 |
| Net price | Net sales divided by units sold. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 88.61485010177665 |
