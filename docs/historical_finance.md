# Historical finance dataset

## Scope and availability

`data/history/history_tidy.csv` and `.json` contain 1,083 source-traceable observations. Consolidated quarterly P&L and insurance drivers cover calendar 2024Q1–2026Q1 (nine quarters) for PG and TRV. P&G fiscal 2026Q3 is calendar 2026Q1. All source publications are on or before May 15, 2026; all financial periods end on or before March 31, 2026. No forecast or target-quarter actual is included.

The latest PG release was published April 24, 2026; the latest TRV release April 16, 2026. These observations are not eligible at March 31, 2026. `eligible_prequarter` and `eligible_midquarter` implement publication-date gates. Historical comparative columns carry the publication date of the release actually preserved, not an assumed original reporting date. This conservative dating is sufficient for the requested two vintages but should not be used to reconstruct earlier vintages without collecting earlier releases.

## Files and reproducibility

- `source_manifest.json`: ten official company earnings releases, publication dates, URLs, source paths, HTML SHA256.
- `supplement_source_manifest.json`: two SEC-furnished Travelers financial supplements with saved web-extract hashes.
- `sources/`: original release HTML, text, line-numbered text, and exact table cells. SEC direct download returned HTTP403, so cash-flow supplement text was captured using the web tool.
- `observations.csv/json`: all 1,257 extracted source observations, including comparative repeats.
- `history_tidy.csv/json`: earliest publication available in this collection for each company/period/basis/segment/metric key.
- `build_history.py`: deterministic offline parser of saved source tables and SEC extracts. No live fetch or forecast.
- `validate_history.py` and `validation.json`: date/excerpt checks and 72 accounting/ratio reconciliations.

Every row carries dates, fiscal/calendar period, period basis, segment, metric, value, unit, reported/derived status, publication eligibility, source URL, source path, table/row locator or SEC printed page/line, and `source_excerpt` with the exact original table row. Table/row indices are zero based and refer to saved `*_tables.json` arrays, not browser visual numbering. `source_excerpt` retains comparison-year cells; the reported value and period identify the selected column. The sources retain relevant column headers.

## Definitions and modelling cautions

Dollar values are USD millions. `percent` is percentage units (e.g. 84.7), not a fraction (0.847). PG price, mix, FX and volume growth are approximate disclosed growth contributions; they are not unit prices, unit counts, production volumes, SKU observations, or additive precise decompositions.

PG quarterly metrics include net sales, cost of products sold, gross profit, SG&A, operating income, signed interest expense, interest income, other income, pretax income, income taxes, net income and income attributable to PG. `net_income` includes noncontrolling interests; `net_income_attributable` excludes them. Diluted EPS is USD/share. Effective tax rate is the reported percent. Segment sales/pretax/net income and growth contributions cover calendar 2025Q1–2026Q1. PG balance-sheet cash excludes restricted cash; `current_debt` and `long_term_debt` are separate reported lines, never silently netted against cash.

TRV uses earned and written premiums, claims, acquisition amortization, G&A, underwriting, catastrophes, prior-year reserve development, investments, core income and capital. `catastrophe_losses_signed` is negative. `favorable_prior_year_development` is positive. Core pretax income = underwriting gain + pretax investment income + other income including interest. Core income = core pretax less core income tax. GAAP net income = core income + realized gains after tax. Segment core tax is labelled `segment_income_tax` and income before tax `segment_pretax_income`. The reported combined ratio follows reported allocations, not the simple GAAP revenue-minus-expense identity: policyholder dividends, fee allocations, billing fees and noninsurance G&A matter. Do not set reported underwriting gain equal to earned premiums times one minus reported combined ratio without a bridge. Underlying underwriting income can be derived as underwriting gain minus signed catastrophes minus favorable prior-year development.

TRV `loss_ratio_numerator` and `expense_ratio_numerator` are source-defined adjusted numerators; `loss_allocated_fee_income` and `expense_allocated_fee_income` distinguish the two fee allocations. Combined, loss, expense and underlying combined ratios are reported percentages. Net investment income in the operating bridge is pretax, not the after-tax headline amount. TRV `cash_and_restricted_cash` includes restricted cash and is not directly comparable to PG cash and cash equivalents. Its 2025Q4 cash reflects the source's held-for-sale classification. Canadian business divestiture affects 2026Q1 comparability.

## Cash coverage and derived values

TRV quarterly operating cash flow and end-period cash including restricted cash cover all nine quarters using the January 21 and April 16 supplements. PG direct discrete-quarter cash flow covers 2024Q3 and 2025Q1–2026Q1. PG 2024Q2 and 2024Q4 cash flow/capex are explicitly `derived_quarter`, calculated from fiscal YTD differences with both source rows retained. PG 2024Q1 discrete cash flow is unavailable in this collection; do not impute it as an actual. Fiscal-YTD records remain separately labelled and must not be summed with discrete quarters. Cash/debt snapshots have `period_basis=instant`; quarterly flow analysis must filter `period_basis=quarter`.

Balance-sheet PG snapshots are narrower than P&L history: June 2024, March/June/September/December 2025 and March 2026. TRV debt/equity snapshots start December 2024; quarter-end cash has the wider nine-quarter coverage. No fictional unit economics, employee figures, granular policy-level losses or official budget has been created.

## Validation and limitations

72 accounting/ratio checks passed. PG gross profit, operating profit, pretax and net-income bridges have at most USD1m source-rounding residuals; the source explicitly states columns/rows may not add due to rounding, and validation allows USD2m. TRV core-dollar bridges reconcile exactly, and reported ratio sums reconcile within 0.11 percentage points. Dates are bounded and every selected row has a source excerpt. This is source extraction validation, not a financial audit.

The dataset captures as-reported values from the archived release, including comparative figures. It does not guarantee historical-original versus subsequently reclassified line-item presentation. PG cash-flow releases disclose certain comparative reclassifications with no effect on total operating cash flow. Core and underlying measures are non-GAAP and must remain labelled.

Retrieval is retrospective. Broad search unexpectedly exposed the data-collection agent to later target-release snippets, despite historical query terms. Those snippets were not opened, saved in the source directory, used in parsing, or passed as values to the forecasting roles. The collector therefore cannot claim blindness; forecasting roles must receive only the allowlisted data/evidence packets. This is in addition to the coordinator exposure documented in the project brief.
