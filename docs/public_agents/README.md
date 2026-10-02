# Financial scenario agents

Two case studies reconstruct expectations for calendar April–June 2026: P&G fiscal 2026 Q4 and Travelers calendar 2026 Q2. The exercise asks how dated research changes a historical baseline, and how much subsequent error comes from historical refresh, assumptions or unpredictable events. It does not claim these forecasts were authored before the quarter.

## Four roles and their reusable instructions

| Role | Judgment responsibility | Handoff | Instruction file |
|---|---|---|---|
| Finance | Map periods, units and reporting definitions; identify unsupported or inconsistent historical data | Normalized interpretation and issues | `agents/finance.md` |
| Research | Map eligible source evidence to drivers; distinguish observations from interpretation and overlapping signals | Causal signals with source IDs, confidence and limitations | `agents/research.md` |
| Scenario | Propose bear/base/bull assumptions within the company-specific driver contract | Numeric assumptions and rationales | `agents/scenario.md` |
| QA | Challenge the original excerpts and all earlier outputs for dates, units, unsupported precision and double counting | Pass, revise or insufficient-evidence decision | `agents/qa.md` |

These project role instructions are reusable prompts with JSON response contracts; they are not claims that four separate marketplace plugins were installed. Finance does not invent research, Research does not calculate final financial statements, Scenario does not approve itself, and QA does not silently repair a result. Python owns arithmetic, eligibility checks, validation, freezing and replay.

The runtime uses fresh authenticated Codex CLI sessions with tools disabled and a serialized packet as the deliberate information boundary. The completed production exercise made **50 genuine model calls**: Finance 12, Research 12, Scenario 12 and QA 14. Eight selected workflows passed and froze, producing 24 scenarios. Sixteen calls belong to the four rejected initial market workflows; two additional QA reviews accepted original rounding support without changing assumptions. All remain in the audit history. One separate synthetic Finance smoke call is excluded from the 50. See the [execution record](../agents-execution.md) and [authoritative summary](../agents-execution-summary.json).

The implementation separates reusable role instructions from supporting software capabilities. The [workflow](../../src/workflow.py) uses schema-constrained non-interactive model execution, timestamped logs and hash-checked replay. The [spreadsheet builder](../../src/build_workbooks.mjs) uses the artifact workbook library for editable formulas, formatting, charts, recalculation and rendered previews. The [calculator](../../src/calculate.py) owns financial arithmetic; independent [tests](../../tests/calculation_test.py) check its boundaries. These capabilities support the roles but are not additional agents.

## Comparison design

| Run | Historical information | Market evidence | Purpose |
|---|---|---|---|
| Pre history | Published by March 31 | None | Original historical control |
| Pre market | Same pre history | Published by March 31 | Research effect before target quarter |
| Mid history | Published by May 15 | None | Isolate newly available company history |
| Mid market | Same mid history | Published by May 15 | Research effect after history refresh |

A March period-end report released in April is excluded from March's information set. Models receive no target actuals. Actuals may enter evaluation only after assumptions freeze. The model's pretrained knowledge cannot be erased; this is an inspectable reconstruction with deliberate input controls, not a claim of perfect historical blindness.

## Where to inspect actual execution

The [selected-run manifest](../../outputs/runs/selected_runs.json) identifies the accepted company/vintage workflow paths. Original executions remain under `outputs/runs`; corrected market executions and selection records are under `outputs/runs`. Within each public role folder, inspect `input.json`, `prompt.txt`, `output.json` and `run.json`. Raw runtime events and stderr remain private. The existence of a folder is not evidence of success. A successful workflow also requires the QA result and a verified `freeze.json`.

`freeze.json` records hashes of the relevant inputs, prompts, outputs and metadata. Replaying the frozen output reproduces saved assumptions without calling a model. A genuine model rerun creates new executions and may produce different assumptions. Hashes provide a consistency check against the retained manifest, not an externally trusted timestamp.

## Evidence boundaries

The public research register retains twenty dated records; nineteen are admitted to revised model packets and one date-conflicted Marsh record is excluded. Short original quotations are supplemented by clearly labeled factual transcriptions, exact locations and an external source-review record. Initial market runs failed QA because quotation coverage was incomplete. Subsequent source and implementation review also removed a later-vintage revision from pre-quarter free text and identified the need to distinguish Travelers' underlying combined ratio from its headline combined ratio. Corrections preserved the original failures and were tested through fresh market runs; they did not waive the QA gate. The local source archive includes raw official material when downloading succeeded; the manifest records blocked downloads. Raw webpages can contain current navigation, so the full archive is never an agent packet. Only curated, dated evidence is admitted.

The researcher initially encountered incidental later search snippets and navigation headlines; these were excluded from evidence and adjustments. The coordinator separately handles held-out results. Source excerpts support only the narrowly quoted facts; QA cannot claim independent webpage authentication when its tools are disabled.

## Output review

The Excel model and native Power BI file are separate deliverables assembled by the coordinator. Availability, opening, refresh and screenshot verification must be reported from actual checks. The [output evidence index](output_review.md) links generated workbook renders, formula verification and genuine execution records; application-specific opening and refresh checks remain separately labeled.
