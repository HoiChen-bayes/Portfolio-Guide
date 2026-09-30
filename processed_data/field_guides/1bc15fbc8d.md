# F1_逐行核对.csv

[Download the complete file](../outputs/F1_逐行核对.csv) · [Back to data guide](../README.md)

**Purpose:** Reconcile the revenue and profit chain and retain traceability.

**Rows:** 700. **Fields:** 25. CSV files store text; the type rules below describe how to interpret the values during import. The images render the actual first five records, with wide tables split into consecutive column panels. They are data excerpts, not screenshots of the Excel application.

![Actual records — F1_逐行核对](images/1bc15fbc8d-1.png)

![Actual records — F1_逐行核对](images/1bc15fbc8d-2.png)

![Actual records — F1_逐行核对](images/1bc15fbc8d-3.png)

![Actual records — F1_逐行核对](images/1bc15fbc8d-4.png)

![Actual records — F1_逐行核对](images/1bc15fbc8d-5.png)

## Fields and formats

| Field | Meaning / use | Import and display | Example |
|---|---|---|---|
| SourceRow | Traceability row in this sample, not a business transaction ID. | Identifier; preserve as text, including leading zeros | 1 |
| Segment | Grouping, filter or comparison label for segment. | Text / categorical label; preserve spelling and blanks | Government |
| Country | Grouping, filter or comparison label for country. | Text / categorical label; preserve spelling and blanks | Canada |
| Product | Grouping, filter or comparison label for product. | Text / categorical label; preserve spelling and blanks | Carretera |
| Discount Band | Field retained under its source/output label; interpret with the table purpose and displayed example. | Text / categorical label; preserve spelling and blanks | None |
| Units Sold | Sample units sold; fractional values are preserved. | Numeric; counts as whole numbers, units/durations retain needed decimals | 1618.5 |
| Manufacturing Price | Source manufacturing-price field; not a substitute for unit COGS. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 3 |
| Sale Price | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 20 |
| Gross Sales | Units sold × sale price, before discounts. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 32370.0 |
| Discounts | Discount amount deducted from gross sales. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0.0 |
| Sales | Net sales after discounts. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 32370.0 |
| COGS | Cost of goods sold from the source sample. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 16185.0 |
| Profit | Sales less COGS; not full company net profit. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 16185.0 |
| Date | Field retained under its source/output label; interpret with the table purpose and displayed example. | Date / period; parse stated order, display YYYY-MM-DD or YYYY-MM | 2014-01-01 |
| Month Number | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; counts as whole numbers, units/durations retain needed decimals | 1 |
| Month Name | Field retained under its source/output label; interpret with the table purpose and displayed example. | Text / categorical label; preserve spelling and blanks | January |
| Year | Calendar year. | Numeric; counts as whole numbers, units/durations retain needed decimals | 2014 |
| Period | Grouping, filter or comparison label for period. | Date / period; parse stated order, display YYYY-MM-DD or YYYY-MM | 2014-01 |
| MonthNo | Month number used for chronological sorting. | Numeric; counts as whole numbers, units/durations retain needed decimals | 1 |
| Gross check | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0.0 |
| Sales check | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0.0 |
| Profit check | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0.0 |
| Margin | Aggregate profit divided by aggregate sales. | Decimal ratio; display as 0.0% (0.10 = 10%) | 0.5 |
| Effective discount | Discounts divided by gross sales. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 0.0 |
| COGS per unit | Field retained under its source/output label; interpret with the table purpose and displayed example. | Numeric; preserve full precision, display amount with 2 decimals where applicable | 10.0 |
