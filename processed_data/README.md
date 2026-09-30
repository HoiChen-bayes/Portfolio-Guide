# Analysis Outputs — global-electronics

[← Project](../README.md) · [Source Data](../raw_data/README.md)

## What was processed, and why?

| Part | Treatment and business purpose | Tasks |
|---|---|---|
| Join | Match product, customer and store keys without multiplying rows. | E1 |
| Calculate | Use quantity × static product rates for estimated sales and cost. | E2 |
| Compare | Aggregate orders, channels, categories and strict same-store cohorts. | E3–E5 |
| Investigate | Use complete repeat windows, valid deliveries and reconciled annual bridges. | E6–E9 |
| Update | Restore the held-out monthly batch and verify totals. | E10 |

## Worksheets and output tables

The links below open illustrated file guides first, with downloads inside each guide. Each preview shows the data, field names and formats.



Open a table below to see its data and field names.

| File | What the page explains |
|---|---|
| [E10_Update_Check.csv](field_guides/04b98f329e.md) | Check the monthly update and handover totals. |
| [E1_Data_Checks.csv](field_guides/85d1f2d278.md) | Validate joins, source coverage and reconciliation. |
| [E2_Priced_Sales_Lines.csv](field_guides/a1b6297f10.md) | Calculate sales, costs and gross profit from quantity and product rates. |
| [E2_Product_Build.csv](field_guides/70e6712348.md) | Calculate sales, costs and gross profit from quantity and product rates. |
| [E3_Annual.csv](field_guides/8a20bf94e0.md) | Explain order and channel performance over time. |
| [E3_Monthly_Channel.csv](field_guides/637a5a0be2.md) | Explain order and channel performance over time. |
| [E3_Orders.csv](field_guides/a8f891900e.md) | Explain order and channel performance over time. |
| [E4_Brand.csv](field_guides/d83a557718.md) | Compare product, store and market contributions. |
| [E4_Category.csv](field_guides/bd58016c24.md) | Compare product, store and market contributions. |
| [E4_Customer_Country.csv](field_guides/4a116a038b.md) | Compare product, store and market contributions. |
| [E4_Store.csv](field_guides/92f4047007.md) | Compare product, store and market contributions. |
| [E5_Store_Comparability.csv](field_guides/37f4b0f1fe.md) | Identify a consistent same-store comparison group. |
| [E6_Cohorts.csv](field_guides/d7d3dc200c.md) | Measure repeat purchasing with complete observation windows. |
| [E6_Customer_90d.csv](field_guides/6547dc404c.md) | Measure repeat purchasing with complete observation windows. |
| [E6_Demographics.csv](field_guides/82603f6d1b.md) | Measure repeat purchasing with complete observation windows. |
| [E6_New_Existing.csv](field_guides/7110532256.md) | Measure repeat purchasing with complete observation windows. |
| [E6_Retention.csv](field_guides/c34f59f4b2.md) | Measure repeat purchasing with complete observation windows. |
| [E7_Delivery.csv](field_guides/22d6390870.md) | Analyse valid delivery times and illustrate exchange-rate treatment. |
| [E7_FX_Illustration.csv](field_guides/45d2a40909.md) | Analyse valid delivery times and illustrate exchange-rate treatment. |
| [E8_Annual_Bridge.csv](field_guides/e49f3d39f6.md) | Explain the year-on-year revenue decline. |
| [E8_Contributions.csv](field_guides/93f581656f.md) | Explain the year-on-year revenue decline. |
| [E8_SKU_Quantity_Bridge.csv](field_guides/bc55de2142.md) | Explain the year-on-year revenue decline. |
| [E9_Store_Review_Shortlist.csv](field_guides/4a0c26a3d3.md) | Prioritise stores for business review. |
| [Customers_UTF8.csv](field_guides/ddf0026398.md) | View the budget, actual amounts and calculations. |
| [Analysis.xlsx](field_guides/c167c79dbf.md) | View the calculations and assumptions. |

<details>
<summary>Browse all downloadable files</summary>

- [outputs/E10_Update_Check.csv](outputs/E10_Update_Check.csv)
- [outputs/E10_核对查询.sql](outputs/E10_核对查询.sql)
- [outputs/E1_Data_Checks.csv](outputs/E1_Data_Checks.csv)
- [outputs/E2_Priced_Sales_Lines.csv](outputs/E2_Priced_Sales_Lines.csv)
- [outputs/E2_Product_Build.csv](outputs/E2_Product_Build.csv)
- [outputs/E3_Annual.csv](outputs/E3_Annual.csv)
- [outputs/E3_Monthly_Channel.csv](outputs/E3_Monthly_Channel.csv)
- [outputs/E3_Orders.csv](outputs/E3_Orders.csv)
- [outputs/E4_Brand.csv](outputs/E4_Brand.csv)
- [outputs/E4_Category.csv](outputs/E4_Category.csv)
- [outputs/E4_Customer_Country.csv](outputs/E4_Customer_Country.csv)
- [outputs/E4_Store.csv](outputs/E4_Store.csv)
- [outputs/E5_Store_Comparability.csv](outputs/E5_Store_Comparability.csv)
- [outputs/E6_Cohorts.csv](outputs/E6_Cohorts.csv)
- [outputs/E6_Customer_90d.csv](outputs/E6_Customer_90d.csv)
- [outputs/E6_Demographics.csv](outputs/E6_Demographics.csv)
- [outputs/E6_New_Existing.csv](outputs/E6_New_Existing.csv)
- [outputs/E6_Retention.csv](outputs/E6_Retention.csv)
- [outputs/E7_Delivery.csv](outputs/E7_Delivery.csv)
- [outputs/E7_FX_Illustration.csv](outputs/E7_FX_Illustration.csv)
- [outputs/E8_Annual_Bridge.csv](outputs/E8_Annual_Bridge.csv)
- [outputs/E8_Contributions.csv](outputs/E8_Contributions.csv)
- [outputs/E8_SKU_Quantity_Bridge.csv](outputs/E8_SKU_Quantity_Bridge.csv)
- [outputs/E9_Store_Review_Shortlist.csv](outputs/E9_Store_Review_Shortlist.csv)
- [prepared_inputs/Customers_UTF8.csv](prepared_inputs/Customers_UTF8.csv)
- [worksheets/Analysis.xlsx](worksheets/Analysis.xlsx)

</details>
