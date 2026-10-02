# Native Power BI projects

Each company folder contains a standard PBIP report and semantic model built from `outputs/analysis.json`. Tables use embedded calculated `DATATABLE` partitions, so the report does not depend on a local spreadsheet path or live credentials. Refresh recalculates this saved snapshot; it does not fetch new financial reports.

P&G uses a clean blue and white card layout. Travelers uses a charcoal underwriting-risk panel with red accents and a different overview arrangement. Both reports have six pages: Summary, History & Segments, Scenarios, Market Revisions, Forecast vs Actual, and Method & QA.

The four-vintage comparison uses a disconnected comparison axis; it retains all four bars when a vintage is selected elsewhere. Case selection still applies. Percent deviations are signed `(actual - forecast) / |forecast|`, not a generic accuracy score. Cost and revenue differences use neutral colors. The market-research waterfall compares forecasts using the same financial-history vintage. Its sequential driver ordering is retained.

Published data are retrospective snapshots. Historical and target financial values remain separately sourced in the repository. The reports are analyst scenarios, not company guidance or official budgets. Native verification outputs and actual screenshots are retained in each company folder after Power BI Desktop validation. Final deliverables are `outputs/PG_Financial_Scenarios.pbix` and `outputs/TRV_Financial_Scenarios.pbix`; these must be saved by Desktop and are never simulated by renaming project archives.
