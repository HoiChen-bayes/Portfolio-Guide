# Dashboard design references and restyle

## Reference boundary

The official [China Power BI competition gallery](https://www.chinapowerbi.com/Works.html?activityId=18) identifies **Toboyoo Sales Dashboard**, by Zhang Hang, as a fictional electronics-retail analysis, and **Financial Enterprise Smart Operating Dashboard**, by Lu Junfeng, as a fictional financial-enterprise analysis. The [official winner list](https://www.chinapowerbi.com/Winning.html) lists Toboyoo as first prize / best visualization and the financial-enterprise entry as second prize / best presentation creativity.

These published entries are design references for coherent identity, analytical hierarchy, and business-specific presentation. The original Toboyoo interactive report was unavailable during the reference review. We do not claim to have inspected its live interactions. The coordinating reviewer inspected the [financial-enterprise report](https://app.powerbi.com/view?r=eyJrIjoiZTEwZmU5NmMtYmVmZC00ZjkyLTlhMzktMGUyZTM5YWVjYWE5IiwidCI6IjdlMTczODMxLThkZDYtNDlkZC1hY2Q1LTljZTY3ZmQ1ODM5MCIsImMiOjZ9&pageName=ReportSection1f9122da2a5df5047d82), specifically its introduction, cockpit and customer-profile pages: its 16-page report uses strong brand/navigation hierarchy, KPI tiles with prior-year context, risk badges, trend/ranking views, and in-cell comparative cues. The redesign adopts hierarchy and disciplined business context, without inventing irrelevant maps or claiming to copy either report. The concrete visual direction below was supplied in the redesign brief.

## Before and after

The original dashboards had working calculations and charts, but relied on repeated white panels and long explanatory footers. The redesign preserves the same financial snapshot, cases, information vintages, existing measures, relationships and six-page analytical scope. Three added display-only columns provide compact calendar-quarter and forecast-version labels; a formatting-only measure controls profit variance color.

P&G now uses a premium consumer-brand finance studio: navy brand rail, powder-blue canvas, cobalt and teal accents, large forecast figures, a wide historical-sales hero, and compact comparison panels. Each page has a distinct analytical composition within the same brand system.

Travelers uses an annual-report editorial treatment: warm white, charcoal type, crimson emphasis, thin horizontal rules, an oversized earnings story, and asymmetric insurance-risk panels. Its page compositions differ from P&G throughout the report.

Native Power BI page tabs provide navigation. The brand rail and editorial masthead are identity elements, not simulated buttons. Native slicers, scatterplots, treemaps, waterfalls, line and bar charts remain interactive. Tables retain scrolling for full source and QA text. Definitions are condensed into short insight lines and precise visual labels.

## Numerical safeguards

Currency formatting includes both `$` and `M`; percentages retain percent formatting. Forecast and actual values are explicitly labeled. Profit deviations use a formatting-only color measure: positive actual-minus-forecast green, negative red. Cost/revenue variance ledgers remain neutral to avoid false favorability signals.

`outputs/powerbi/restyle_model_invariance.json` verifies that every pre-existing table partition, measure expression and relationship is unchanged. `outputs/analysis.json` remains SHA-256 `cd58954f29e8e43f65d88859f4283a4f63162c31462b2f7f3294f8626128f67d`. Final native validation checks all 142 numeric results, six pages per company, and embedded PBIX models. Final screenshots are actual report-canvas captures from Power BI Desktop.

The local before-restyle archive is private and excluded from publication. No Excel workbook was changed by this restyle.
