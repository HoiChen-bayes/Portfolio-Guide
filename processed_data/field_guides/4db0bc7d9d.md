# Financial_Sample.csv

[Download the complete file](../prepared_inputs/Financial_Sample.csv) · [Back to data guide](../README.md)

**Purpose:** Provide a prepared table for consistent joins, filtering and analysis.

**Rows:** 700. **Fields:** 16. CSV files store text; the type rules below describe how to interpret the values during import. The images render the actual first five records, with wide tables split into consecutive column panels. They are data excerpts, not screenshots of the Excel application.

![Actual records — Financial_Sample](images/4db0bc7d9d-1.png)

![Actual records — Financial_Sample](images/4db0bc7d9d-2.png)

![Actual records — Financial_Sample](images/4db0bc7d9d-3.png)

![Actual records — Financial_Sample](images/4db0bc7d9d-4.png)

## Fields and formats

| Field | Meaning / use | Import and display | Example |
|---|---|---|---|
| Segment | Grouping, filter or comparison label for segment. | Text / categorical label; preserve spelling and blanks | Government |
| Country | Grouping, filter or comparison label for country. | Text / categorical label; preserve spelling and blanks | Canada |
| Product | Grouping, filter or comparison label for product. | Text / categorical label; preserve spelling and blanks | Carretera |
| Discount Band | Field retained under its source/output label; interpret with the table purpose and displayed example. | Text / categorical label; preserve spelling and blanks | None |
| Units Sold | Sample units sold; fractional values are preserved. | Numeric; counts as whole numbers, units/durations retain needed decimals | 1618.5 |
| Manufacturing Price | Source manufacturing-price field; not a substitute for unit COGS. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 3 |
| Sale Price | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 20 |
| Gross Sales | Units sold × sale price, before discounts. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 32370 |
| Discounts | Discount amount deducted from gross sales. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0 |
|  Sales | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 32370 |
| COGS | Cost of goods sold from the source sample. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 16185 |
| Profit | Sales less COGS; not full company net profit. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 16185 |
| Date | Field retained under its source/output label; interpret with the table purpose and displayed example. | Date / period; parse stated order, display YYYY-MM-DD or YYYY-MM | 2014-01-01 |
| Month Number | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; counts as whole numbers, units/durations retain needed decimals | 1 |
| Month Name | Field retained under its source/output label; interpret with the table purpose and displayed example. | Text / categorical label; preserve spelling and blanks | January |
| Year | Calendar year. | Numeric; counts as whole numbers, units/durations retain needed decimals | 2014 |
