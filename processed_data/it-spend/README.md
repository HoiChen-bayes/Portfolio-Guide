# Analysis Outputs — it-spend

[← Project](../../projects/it-spend/README.md) · [Source Data](../../raw_data/it-spend/README.md)

## What was processed, and why?

| Part | Treatment and business purpose | Tasks |
|---|---|---|
| Extract | Read the embedded model and retain source keys and scenario values. | I1 |
| Reconcile | Validate joins and compare monthly Actual with Plan. | I1–I3 |
| Diagnose | Trace drivers, estimate overlap and monthly persistence. | I4–I7 |
| Plan | Prepare evidence requests and model a remaining-year cost proposal. | I8–I10 |

## Worksheets and output tables

The links below open illustrated file guides first, with downloads inside each guide. Previews contain actual saved values; ratios, identifiers and dates are explained beside the column definitions.



Open a table or workbook below to inspect real rows, column meanings and format rules.

| File | What the page explains |
|---|---|
| [I10_Rolling_Forecast_Illustration.csv](<field_guides/801098a6d9.md>) | Combine closed actuals with remaining estimates and scenario actions. |
| [I1_Data_Dictionary.csv](<field_guides/d2179e190e.md>) | Validate source extraction and data consistency. |
| [I1_Reconciliation_Checks.csv](<field_guides/a9c25443d1.md>) | Validate source extraction and data consistency. |
| [I2_Monthly_Spend.csv](<field_guides/50d6143c52.md>) | Measure spend against plan by month. |
| [I4_Driver_Detail.csv](<field_guides/061ba80852.md>) | Trace material cost variances to reviewable drivers. |
| [I4_Trace_1.csv](<field_guides/d5062ff323.md>) | Trace material cost variances to reviewable drivers. |
| [I4_Trace_2.csv](<field_guides/3d2a23e484.md>) | Trace material cost variances to reviewable drivers. |
| [I4_Trace_3.csv](<field_guides/edfa74d047.md>) | Trace material cost variances to reviewable drivers. |
| [I5-I6_Version_Diagnostics.csv](<field_guides/8bcf1c0244.md>) | Compare estimate versions and diagnose overlap with actuals. |
| [I7_Monthly_Patterns.csv](<field_guides/f8a92ddc76.md>) | Distinguish recurring variance patterns from monthly offsets. |
| [I8_Review_Actions.csv](<field_guides/72a5b13ff4.md>) | Prepare specific evidence requests for budget-owner review. |
| [Business_Area.csv](<field_guides/4b3d8dc24c.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Cost_Element.csv](<field_guides/109ceb78e7.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Country_Region.csv](<field_guides/73ff7187d3.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Date.csv](<field_guides/5b1a129efe.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Department.csv](<field_guides/b35d7f8b04.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Fact.csv](<field_guides/51feea3373.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [IT_Area.csv](<field_guides/7b6cef3132.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Original_Measures.csv](<field_guides/e6d25bb0a4.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Original_Relationships.csv](<field_guides/8e74b81160.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Range.csv](<field_guides/c65be4eb8d.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Scenario.csv](<field_guides/fb7bcc4efb.md>) | Provide a prepared table for consistent joins, filtering and analysis. |
| [Analysis.xlsx](<field_guides/c167c79dbf.md>) | Inspect calculations, assumptions and saved worksheet results. |

<details>
<summary>Browse all downloadable files</summary>

- [outputs/I10_Rolling_Forecast_Illustration.csv](<outputs/I10_Rolling_Forecast_Illustration.csv>)
- [outputs/I1_Data_Dictionary.csv](<outputs/I1_Data_Dictionary.csv>)
- [outputs/I1_Reconciliation_Checks.csv](<outputs/I1_Reconciliation_Checks.csv>)
- [outputs/I2_Monthly_Spend.csv](<outputs/I2_Monthly_Spend.csv>)
- [outputs/I4_Driver_Detail.csv](<outputs/I4_Driver_Detail.csv>)
- [outputs/I4_Trace_1.csv](<outputs/I4_Trace_1.csv>)
- [outputs/I4_Trace_2.csv](<outputs/I4_Trace_2.csv>)
- [outputs/I4_Trace_3.csv](<outputs/I4_Trace_3.csv>)
- [outputs/I5-I6_Version_Diagnostics.csv](<outputs/I5-I6_Version_Diagnostics.csv>)
- [outputs/I7_Monthly_Patterns.csv](<outputs/I7_Monthly_Patterns.csv>)
- [outputs/I8_Review_Actions.csv](<outputs/I8_Review_Actions.csv>)
- [prepared_inputs/I1_Extracted_Data/Business_Area.csv](<prepared_inputs/I1_Extracted_Data/Business_Area.csv>)
- [prepared_inputs/I1_Extracted_Data/Cost_Element.csv](<prepared_inputs/I1_Extracted_Data/Cost_Element.csv>)
- [prepared_inputs/I1_Extracted_Data/Country_Region.csv](<prepared_inputs/I1_Extracted_Data/Country_Region.csv>)
- [prepared_inputs/I1_Extracted_Data/Date.csv](<prepared_inputs/I1_Extracted_Data/Date.csv>)
- [prepared_inputs/I1_Extracted_Data/DateTableTemplate_5db4a9d0-37ae-4eb8-b985-081b6a9bccc6.csv](<prepared_inputs/I1_Extracted_Data/DateTableTemplate_5db4a9d0-37ae-4eb8-b985-081b6a9bccc6.csv>)
- [prepared_inputs/I1_Extracted_Data/Department.csv](<prepared_inputs/I1_Extracted_Data/Department.csv>)
- [prepared_inputs/I1_Extracted_Data/Fact.csv](<prepared_inputs/I1_Extracted_Data/Fact.csv>)
- [prepared_inputs/I1_Extracted_Data/IT_Area.csv](<prepared_inputs/I1_Extracted_Data/IT_Area.csv>)
- [prepared_inputs/I1_Extracted_Data/LocalDateTable_c659a3fc-ad91-4f80-b458-6b22a6d14a66.csv](<prepared_inputs/I1_Extracted_Data/LocalDateTable_c659a3fc-ad91-4f80-b458-6b22a6d14a66.csv>)
- [prepared_inputs/I1_Extracted_Data/Original_Measures.csv](<prepared_inputs/I1_Extracted_Data/Original_Measures.csv>)
- [prepared_inputs/I1_Extracted_Data/Original_Relationships.csv](<prepared_inputs/I1_Extracted_Data/Original_Relationships.csv>)
- [prepared_inputs/I1_Extracted_Data/Range.csv](<prepared_inputs/I1_Extracted_Data/Range.csv>)
- [prepared_inputs/I1_Extracted_Data/Scenario.csv](<prepared_inputs/I1_Extracted_Data/Scenario.csv>)
- [worksheets/Analysis.xlsx](<worksheets/Analysis.xlsx>)

</details>
