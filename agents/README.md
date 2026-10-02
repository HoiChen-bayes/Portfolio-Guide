# Finance / Research / Scenario / QA agents

A reusable four-agent workflow builds dated financial scenarios for **P&G** and **Travelers**, then evaluates them against reported results. Each role is a real, independent model session; Python performs the arithmetic and validation.

[Explore the complete project](https://github.com/hoichengit/Portfolio-Guide/tree/codex/financial-scenarios) · [P&G case](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/public_cases/PG.md) · [Travelers case](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/public_cases/TRV.md)

| Role and reusable instructions | Responsibility | Why separate it? |
|---|---|---|
| [Finance](finance.md) | Map historical reporting, periods, units and accounting definitions. | Source interpretation stays separate from forecast judgment. |
| [Research](research.md) | Connect dated evidence to financial drivers and identify overlapping signals. | Market claims retain their sources and uncertainty. |
| [Scenario](scenario.md) | Propose structured bear, base and bull assumptions. | Numbers can be reviewed before deterministic calculations. |
| [QA](qa.md) | Challenge the original evidence, assumptions and earlier role outputs. | The forecaster cannot approve its own work. |

The role instructions work with strict response schemas, dated input packets, disabled model tools, independent QA and file-hash freezes. Actual results enter the evaluation only after all eight selected assumption sets are frozen. A new model run may change judgments; deterministic replay verifies the saved assumptions without calling a model.

<details>
<summary>Actual Excel output previews</summary>

These images are generated previews of the delivered Excel workbooks. They show the actual case outputs rather than conceptual mockups.

### P&G

![P&G financial scenario workbook summary](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/screenshots/PG/Summary.png)

### Travelers

![Travelers financial scenario workbook summary](https://raw.githubusercontent.com/hoichengit/Portfolio-Guide/refs/heads/codex/financial-scenarios/outputs/screenshots/TRV/Summary.png)

</details>

## Design and evidence

<details>
<summary>Execution, review decisions and reproducibility</summary>

The completed experiment used **50 genuine production model calls**, plus one separate synthetic runtime smoke test. All eight final case/vintage combinations passed their scoped QA reviews and replay checks. Four original market reviews found insufficient source support, and two later P&G reviews requested source rounding evidence. Those rejected decisions were retained. Two fresh QA-only calls accepted original rounding footnotes without changing any forecast assumptions.

- [Workflow and command contracts](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/agents.md)
- [Actual execution record](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/agents-execution.md)
- [Agent design and skills](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/docs/public_agents/README.md)
- [Financial outputs and downloads](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/outputs/README.md)
- [Source data and date controls](https://github.com/hoichengit/Portfolio-Guide/blob/codex/financial-scenarios/data/README.md)

This is an October 2026 retrospective reconstruction. Date controls restrict supplied information but cannot erase model pretraining. Scenarios are analyst judgments, not official budgets or calibrated probability intervals. QA checks supplied evidence and model coherence; it does not certify external webpages or perform an external accounting audit. The case studies retain forecast improvements, deterioration and limitations.

</details>
