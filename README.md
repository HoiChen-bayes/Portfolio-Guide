# Pets & More: Budget, Forecast & Cash

[← Portfolio](https://github.com/hoichengit/Portfolio-Guide) · [Source Data](raw_data/README.md) · [Analysis Outputs](processed_data/README.md)

## Dataset overview

- 55 actual income and expense records, January–May 2022.
- 108 monthly budget records across nine categories, January–December 2022.
- Dates, categories, descriptions and amounts in USD.

[Explore source tables, real data excerpts and field formats →](raw_data/README.md)

## Analysis questions

Click a question to jump to its answer and evidence.

| Analysis area | Questions |
|---|---|
| Prepare a fair comparison | [1 — Can actuals and budget be compared?](#b1) |
| Monthly performance | [2 — Which months generated a surplus?](#b2)<br>[3 — How did May perform against budget?](#b3) |
| Explain the budget gap | [4 — What deserves immediate review?](#b4)<br>[5 — What explains the YTD gap?](#b5) |
| Forecast and recovery | [6 — What is the revised full-year result?](#b6)<br>[7 — Which recovery scenario improves the model most?](#b7) |
| Close and management review | [8 — What should be checked before close?](#b8)<br>[9 — What should the business review focus on?](#b9) |
| Cash and funding | [10 — When could funding be needed?](#b10) |

## Analysis data and outputs

[Explore the processed tables, worksheet contents and calculation evidence →](processed_data/README.md)

The output guide separates Analysis data, calculation workbooks and analytical outputs. Each illustrated file page explains its purpose and fields.

## Visualisation

[Open the interactive Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZDUxM2MxNDYtMzZhMy00ZDhlLTkzZjQtMGRiYTRlNDMxYjUxIiwidCI6IjljNzNiMWYxLWY0ZGYtNDhkYy05ZDg5LWE0M2NjNjQ4YmJhNSJ9&language=en-US) — no sign-in or dataset download required. Select a page and use its filters to explore the analysis.

![Power BI Summary](assets/summary.png)

[Download Power BI file](report.pbix)

## Results and evidence

<a id="b1"></a>

### 1 — Can actuals and budget be compared?

**Yes. These two entries both refer to January Sales in USD.**

<details>
<summary>View evidence — compare January Sales in Excel</summary>

#### 1. Actual: January Sales = $5,000

Look at **January**, **Sales** and **5,000** in the original Excel sheet.

![Actual Excel screenshot: January Sales of 5,000](processed_data/field_guides/images/Actual_January_Sales.png)

#### 2. Budget: January Sales = $6,000

Look at the **January** column and **Sales** row in the original Excel sheet.

![Budget Excel screenshot: January Sales budget of 6,000](processed_data/field_guides/images/Budget_January_Sales.png)

**The month and category match, so we can compare the amounts: $5,000 − $6,000 = −$1,000. Sales is $1,000 below budget.**

For the full analysis, compare **January–May only**, because that is the period covered by the actuals.

[Open the Excel file and full screenshots](processed_data/field_guides/4710152f65.md)

</details>

<a id="b2"></a>

### 2 — Which months generated a surplus?

**Result.** March is the only positive month, at $1,700; YTD income less expenses is ($15,934).

**How and why.** Sum income and expense categories separately for each month, then subtract expenses from income.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/6b09eb26ef.md)

![2 — supporting file excerpt](processed_data/field_guides/images/6b09eb26ef-s0-1.svg)

</details>

<a id="b3"></a>

### 3 — How did May perform against budget?

**Result.** May income was $1,200 below budget and expenses $811 below budget, leaving a $389 unfavourable net variance.

**How and why.** Compare May with May. Reverse expense variances when calculating their contribution to the net result.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/6c9b7e1dbb.md)

![3 — supporting file excerpt](processed_data/field_guides/images/6c9b7e1dbb-s0-1.svg)

</details>

<a id="b4"></a>

### 4 — What deserves immediate review?

**Result.** May Sales is $3,000 below plan, Transport is $900 above plan, and Other Expenses is $1,680 below plan.

**How and why.** Rank material dollar gaps, inspect transaction descriptions and identify evidence needed to distinguish timing from operational changes.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/4e494bbe31.md)

![4 — supporting file excerpt](processed_data/field_guides/images/4e494bbe31-s0-1.svg)

</details>

<a id="b5"></a>

### 5 — What explains the YTD gap?

**Result.** The YTD result is $3,734 worse than budget. Sales and Other Income contribute $4,400 and $4,700 of downside, partly offset by $7,470 lower Other Expenses.

**How and why.** Sum January–May actuals and matching budgets by category; reconcile signed contributions to the total net gap.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/4f1a41b2e5.md)

![5 — supporting file excerpt](processed_data/field_guides/images/4f1a41b2e5-s0-1.svg)

</details>

<a id="b6"></a>

### 6 — What is the revised full-year result?

**Result.** The base forecast is ($11,468.33), an improvement of $2,731.67 versus the original ($14,200) budget.

**How and why.** Keep January–May actuals and add June–December estimates using the documented category assumptions.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/340f921e89.md)

![6 — supporting file excerpt](processed_data/field_guides/images/340f921e89-s0-1.svg)

</details>

<a id="b7"></a>

### 7 — Which recovery scenario improves the model most?

**Result.** Service recovery improves the result by $2,250; the cost-control scenario improves it by $4,389. All three scenarios remain in deficit.

**How and why.** Change only future-period drivers. Compare each evaluated case with the same base; the workbook comparison is a saved scenario snapshot.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/4a0dce2d95.md)

![7 — supporting file excerpt](processed_data/field_guides/images/4a0dce2d95-s1-1.svg)

</details>

<a id="b8"></a>

### 8 — What should be checked before close?

**Result.** Two identical $300 insurance entries and potential timing/completeness issues are flagged; no unsupported correction is posted.

**How and why.** Compare record attributes and request invoices, ledger balances and accrual evidence. A duplicate-looking record is not proof of duplicate accounting.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/bb44cca228.md)

![8 — supporting file excerpt](processed_data/field_guides/images/bb44cca228-s0-1.svg)

</details>

<a id="b9"></a>

### 9 — What should the business review focus on?

**Result.** The review prioritises Sales, Transport and Other Expenses and links them to the full-year forecast.

**How and why.** Combine monthly and YTD evidence with a specific question, proposed owner role and next step; no meeting outcome is invented.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/1a4d21dfdf.md)

![9 — supporting file excerpt](processed_data/field_guides/images/1a4d21dfdf-s0-1.svg)

</details>

<a id="b10"></a>

### 10 — When could funding be needed?

**Result.** The illustrative model needs $1,121.67 in October to maintain a $5,000 cash floor.

**How and why.** Roll opening cash plus modelled collections less payments, tax and capex. This depends on the stated opening cash and collection assumptions.

<details>
<summary>View evidence</summary>

[View the data](processed_data/field_guides/bd66ba59ac.md)

![10 — supporting file excerpt](processed_data/field_guides/images/bd66ba59ac-s0-1.svg)

</details>

## Source and measurement notes


**Period:** January–May 2022 actuals; January–December 2022 budget.  
**Scope:** 55 actual records and 108 monthly category budgets.  
**Source:** [Arnav Chaturvedi — Budget vs Actuals model](https://github.com/arnavchaturvedi17/FinancialAnalysis-Variance-Model-Simple-Budget-vs-Actuals-).

Public practice model; the company identity and operational history are not independently verified. May is treated as complete for the exercise. Forecasts, cash timing and funding assumptions are illustrative. Close checks and review questions are preparation work, not an audit or completed business meeting.

