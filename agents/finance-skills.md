# Finance Agent — Skills

**Purpose:** Give Finance a repeatable way to select, align and check financial inputs before a forecast is built.

[Finance Agent](https://github.com/hoichengit/Portfolio-Guide/blob/main/agents/finance.md) · [Reusable role instructions](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/agents/finance.md) · [Real execution record](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/agents-execution.md)

## Skill groups

| Group | Why it exists | Problems solved |
|---|---|---|
| [1. Input selection](#input-selection) | Financial reports place several time periods beside each other. | Quarterly revenue · Annual totals · Currency and scale |
| [2. Date alignment](#date-alignment) | A report can be published after the period it describes. | Report cutoff · Fiscal/calendar periods · Late information |
| [3. Ratio checks](#ratio-checks) | An amount is only comparable when its period and accounting meaning match. | Gross margin · Expense ratio · Missing or inconsistent inputs |

<a id="input-selection"></a>
## 1. Input selection

- **Purpose:** Check that reported revenue is recorded in Excel with the correct amount, period and unit.
- **Why:** Confusing quarterly and annual figures would make the historical financial report wrong before analysis begins.
- **Method:** Read the row, column period and unit together, then preserve the source reference beside the selected value.

<details>
<summary>Compare the original report with the full Excel worksheet</summary>

**Follow the red marks:** NET SALES of **$20,889 million** in the report matches **$20,889.0M** in Excel; the extra decimal is display formatting, and M means million.

| Original company report — page 8 | Actual Excel workbook — Historical Financials |
|---|---|
| [![Original P&G earnings statement with net sales outlined in red](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/revenue_original_source.png)](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/revenue_original_source.png) | [![Full Historical Financials worksheet in Microsoft Excel with net sales highlighted in red](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/revenue_excel_full.png)](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/revenue_excel_full.png) |
| Three months ended 30 June 2025, 2025 column; NET SALES. | FY2025Q4 column; Net Sales row; cell I14. |

Click either image to open it at full size.

**Check:** Same amount (**20,889**), period (**April–June 2025 / FY2025 Q4**), currency (**USD**) and scale (**millions**).

[Original report PDF](https://s204.q4cdn.com/332108499/files/doc_financials/2025/q4/FY2425-Q4-AMJ-Press-Release-Final.pdf#page=8) · [Actual Excel workbook](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/PG_Financial_Scenarios.xlsx)

The left image is the original PDF page with red outlines added. The right image is a genuine Microsoft Excel screenshot showing every populated row and period of the historical-financials worksheet, with temporary red emphasis; the workbook's data and formulas are unchanged.

</details>

<a id="date-alignment"></a>
## 2. Date alignment

- **Purpose:** Use only information available by the forecast date.
- **Why:** March results released in April cannot support a forecast supposedly based on March information.
- **Method:** Match the financial period to the report, compare the publication date with the cutoff, and flag late records.

<details>
<summary>Example: one report, two forecast dates</summary>

**Result:** The **24 April 2026** release is excluded at **31 March** and available at **15 May**.

![Date alignment: source dates and cutoff decisions](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/timing.png)

[Report dates](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/data/history/source_manifest.json) · [Actual Finance output](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/runs/PG_mid_history/finance/output.json)

</details>

<a id="ratio-checks"></a>
## 3. Ratio checks

- **Purpose:** Convert matched financial amounts into interpretable model references.
- **Why:** Gross profit and sales from different periods would create a misleading margin even if the arithmetic were correct.
- **Method:** Match the period and unit, divide gross profit by sales, and retain any missing data or reconciliation issues for QA.

<details>
<summary>Example: reported gross profit to historical margin</summary>

**Result:** **$10,258M ÷ $20,889M = 49.11%**, providing a historical reference for the Scenario Agent.

![Ratio checks: matching reported amounts and calculated margin](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/margin.png)

[Actual mapping and issues](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/runs/PG_mid_history/finance/output.json) · [Editable evidence](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/guide_evidence/Finance_Evidence.xlsx)

</details>

These are capabilities implemented through the role instructions and workflow checks; they are not separately installed software plugins.

[Back to skill groups](#skill-groups) · [Finance Agent](https://github.com/hoichengit/Portfolio-Guide/blob/main/agents/finance.md)
