# P&G External Financial Analysis

- **Goal:** Use public information to assess P&G from an investment perspective and an insurance risk-screening perspective.
- **Start here:** [1. Financial statements — revenue and operating profit](investment/01_financial_statements.md).
- **Current sample:** FY2024–FY2026 income statements, two questions, an Excel analysis and original-source evidence.
- **Files:** [Original data](raw_data/README.md) · [Analysis outputs](processed_data/README.md) · [Agents](agents/README.md).

## Two perspectives

| Module | Decision it supports | Current stage |
|---|---|---|
| Investment analysis | Earnings quality, cash generation and valuation for a CIO or investment committee. | Income-statement sample ready for review. |
| Insurance risk screening | Publicly visible exposures, disruption paths and information requests for a CUO or CRO. | Planned after the investment sample is reviewed. |

## Project sequence

```mermaid
flowchart TB
    A[Public company reports] --> B[Extract and check historical financials]
    B --> C[Explain business drivers]
    C --> D[Research markets and competitors]
    D --> E[Build scenarios and valuation]
    E --> F[Investment report and dashboard]
    B --> G[Map exposures and dependencies]
    G --> H[Screen hazards and loss pathways]
    H --> I[Insurance information requests]
```

This first sample analyses reported results. Forecasts, valuation and insurance scenarios are later stages. Insurance work will identify exposures and missing underwriting information; it will not produce a premium quote from public data.
