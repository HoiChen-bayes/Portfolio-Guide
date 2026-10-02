# Actual model execution record

The accepted eight-case experiment is in `outputs/runs`. All eight final QA decisions passed and every freeze was verified by deterministic replay. The work used **50 genuine production model calls** plus one separate synthetic runtime smoke call. Reused history-control copies are counted only once.

Execution: 2026-10-02T12:45:57.473771+00:00 to 2026-10-02T13:23:48.134908+00:00; elapsed 37.8 minutes, including source repair and review waits. At most two pipelines ran concurrently. Requested model inherited the user configuration: gpt-6.1-sol.

| Role | Actual calls |
|---|---:|
| Research | 12 |
| Qa | 14 |
| Scenario | 12 |
| Finance | 12 |

Across all 14 independent QA calls: 8 pass, 4 insufficient evidence, and 2 revise. These are review decisions; all 50 runtime calls completed successfully. The rejected reviews were preserved, not relabeled as successful.

The first market batch failed because short excerpts omitted material facts. A pre-quarter PPI note also contained a later revision value. Revised evidence received separate primary-source inspection and a complete text-vintage check; one ambiguously dated Marsh item was excluded. None of the failed market assumptions were selected.

The revised P&G market reviews requested original support for USD1m historical residuals. Independent inspection located the original rounding footnotes and exact reported rows. Two fresh QA-only calls accepted that supplementary evidence; Finance, Research, Scenario outputs and every forecast number remained unchanged. Both rejected reviews and their supplements are included in the final freeze hashes.

Final warnings remain: transcription-dependent source support, limited cash/debt/exposure detail, approximate P&G share denominators, reported rounding residuals, and model classification conventions. A QA pass is a scoped model/evidence review, not an external accounting audit or certification of webpage accuracy.

The complete per-case warnings, UTC times and aggregate runtime usage are in `agents-execution-summary.json`. `outputs/runs/selected_runs.json` identifies the eight accepted artifacts and freeze hashes. Raw events and runtime stderr can be excluded from public distribution without affecting replay; retain all paths listed in each freeze manifest.
