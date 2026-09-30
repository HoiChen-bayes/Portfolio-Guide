# Finance analysis portfolio

**Focus:** FP&A and commercial finance using public sample data. Prepared with AI assistance. The materials cover variance analysis, forecast updates, working capital, cash planning and an illustrative accounting close.

## IT spend: where should management focus?

Compared actual spend with Plan and latest-estimate versions, traced material cost variances, and constructed an illustrative year-end outlook using actuals for closed months and estimates for remaining months. Infrastructure exceeded Plan in 11 of 12 months, supporting a targeted review rather than a blanket assumption that the overspend would reverse.

The analysis separates in-year net benefit from annualised recurring savings. Missing estimate publication dates prevent a claim of genuine historical forecast accuracy. Contract and invoice evidence would be needed before confirming root causes or implementing a cost action.

**Review:** IT Finance dashboard pages 02, 03 and 07, followed by the assumptions and action schedule.

## Commercial performance: is growth profitable?

Analysed 700 monthly sample records across six products, five countries and five segments. Comparable September–December sales rose **36.9%**. The **9.74M** increase reconciles to **5.06M** from matched-group volume, **0.29M** from realised price and **4.39M** from coverage changes. Realised price includes discounts and within-group mix. Coverage changes are not confirmed customer acquisition or churn.

Enterprise generated approximately **0.615M** of negative sample profit across the full dataset. An illustrative discount proposal shows **0.159M** potential improvement under a 5% volume decline, but a 25% decline produces a loss of benefit versus baseline. No saving has been realised.

**Review:** Commercial dashboard pages 03, 04 and 06, then the decision memo and formula-backed workbook.

## Forecast challenge: does a simple model hold up?

A retrospective SQL exercise compares three one-month-ahead methods at segment-month level. The trailing-three-month baseline wins the April–September selection period. Its October–December holdout WAPE is **41.6%**, with **−22.5%** signed bias. The result supports obtaining commercial inputs rather than claiming a dependable statistical forecast. Only three holdout months are available.

Each target forecast uses earlier months only. All 135 predictions match an independent calculation, and changing target-month data does not change that month's prediction. The retrospective protocol assumes prior-month data are available at month-end and does not reproduce a real historical publication process.

**Review:** F11 forecast methodology and reproducible SQLite analysis.

## Planning, cash and close: what does the forecast imply?

Built an October-close forecast using October actuals and November–December driver assumptions. In the base case, Q4 sales move from a reconstructed September forecast of **20.37M** to **28.80M**. The **8.44M** revision reconciles to October actualisation, remaining-period volume and realised price. Future actuals are excluded from forecast inputs.

Linked sales and cost forecasts to receivables, inventory, payables and cash under three teaching scenarios. The downside case produces a **3.57M** peak funding requirement against a **1.50M** minimum cash target. Receivable and payable caps prevent impossible negative collections or supplier payments. The model excludes tax, interest and financing and observes month-end cash only.

A separate synthetic ledger demonstrates five balanced adjusting journals, moving profit from **200,000** to **180,000**. Trial-balance and net-assets/equity checks reconcile. A local monthly update workflow validates 700 sample rows, freezes versions and rejects invalid amounts, missing months and changes to frozen inputs.

**Review:** F15–F17 workbook and planning dashboard; F18 update instructions and validation evidence.

## Boundaries

These are sample-data projects, not employment experience. There is no claim of a completed financial audit, actual stakeholder approval, production deployment or realised business impact. Sample profit is sales less COGS, not company net income. Excel and Power BI are delivery snapshots; editing Excel does not automatically refresh the report.

## Suggested interview walkthrough

Start with one business question. Show the quantified result and trace one headline number to its source. Explain one modelling choice and one alternative rejected. Finish with the decision the evidence supports, the missing information, and the practical next step. Trace the forecast revision into cash needs and explain the closing adjustments.
