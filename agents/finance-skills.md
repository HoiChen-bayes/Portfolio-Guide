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

- **Purpose:** Choose the correct reported amount for the model input.
- **Why:** Using full-year sales instead of quarterly sales would overstate the starting revenue before any forecasting begins.
- **Method:** Read the row, column period and unit together, then preserve the source reference beside the selected value.

<details>
<summary>Example: quarterly revenue, with matching values in red</summary>

**Result:** The agent carries quarterly sales of **$20,889M** into the baseline and leaves full-year sales of **$84,284M** out.

![Input selection: source and result](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/guide_evidence/revenue.png)

[Actual mapping](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/runs/PG_mid_history/finance/output.json)

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
