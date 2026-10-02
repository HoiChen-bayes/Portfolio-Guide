# Repeatable model workflow

Four independent, fresh Codex model sessions perform judgment: Finance maps historical reporting, Research maps evidence to drivers, Scenario proposes numeric assumptions, and QA challenges the original evidence plus all earlier outputs. Python performs validation, freezing, arithmetic integration and replay. Calling deterministic functions is never described as an agent run.

## Run contracts

Requires Python 3.11+ and an authenticated `codex` CLI. No API key is required by this implementation. Authentication, subscription availability and limits remain environment-dependent. Model defaults to the user's configured model, with an explicit `--model` override available. No credentials are copied into the project. Failed requests retain a failed run status and never produce a freeze.

```sh
python3 src/workflow.py model-run --input data/packets/example.json --output outputs/runs/example
python3 src/workflow.py role --role scenario --input data/packets/scenario-input.json --output outputs/runs/scenario-only
python3 src/workflow.py replay --run outputs/runs/example --output outputs/replayed-assumptions.json
```

Output folders must be new to avoid silently overwriting prior evidence. A single-role input may be a packet or an envelope `{"packet": ..., "prior_outputs": ...}`. Single-role execution does not create a full workflow freeze.

A packet has `company`, `sector`, `cutoff` (ISO date), `target_period` (`start`, `end`), `history`, `evidence`, and `driver_contract`. Every history/evidence row has `source_id`, `published_at`, and an original `source_excerpt`. Historical rows should also specify `period_end`, metric, value, unit and source URL. Driver contracts contain `driver`, `unit`, optional numeric `min` and `max`, and explanatory meaning/orientation fields. The wrapper forwards additional curated context unchanged, so the packet curator is responsible for excluding future information from free text. History-only packets carry no market evidence and should use a `vintage` beginning `history_only`.

No target actuals belong in the packet. Publication dates are the availability gate; period end is insufficient. Do not place a later-published preceding-quarter release into a pre-quarter packet. Use the same historical rows in the mid-quarter history-only control and market-informed treatment. Dataset truth and source capture are separately audited responsibilities.

## Isolation and evidence

Each role runs `codex exec --ephemeral --sandbox read-only --output-schema ... --output-last-message ...` from a fresh temporary directory. User configuration is excluded except the selected model and reasoning effort. Shell, browser, web search, apps, plugins, hooks, MCP servers, memory and delegation are disabled. Project instruction loading is disabled. No target actuals or repository files are intentionally supplied. Runtime tool events cause rejection as a defense against configuration drift. Read-only by itself would not prevent filesystem reads, which is why shell and other tools are disabled as well. Validate these controls on the installed CLI when upgrading it.

The prompt and serialized input are saved with real UTC execution times and hashes. Source excerpts are data, never instructions. QA receives original excerpts as well as other agents' outputs; it can only claim consistency with those excerpts, not independently authenticated webpage accuracy. Missing excerpts force an insufficient-evidence result. QA failure stops freezing; revise a packet and launch a new run rather than modifying saved outputs.

## Freeze and replay

After all four real calls complete and QA passes, `freeze.json` hashes the packet, prompts, role inputs, outputs and run metadata. Replay verifies those bytes and output schemas, then returns saved assumptions without model calls. `unlock_actuals(run_dir, actuals_path)` only reads held-out actuals after freeze verification; the arithmetic engine should use that boundary. Hashes are tamper-evident within the retained manifest, not a trusted external timestamp or signature. Archive/publish the manifest to make subsequent changes observable.

Forecasts are reconstructed now from dated inputs. They are not forecasts authored in the past; date filtering cannot erase model pretraining. Model reruns are stochastic and can change assumptions. Exact reproducibility comes from frozen-output replay. Analyst scenarios are not official company budgets.

## Skills and design choices

Role instructions are in `agents/*.md`, strict response contracts in `config/schemas/*.json`. These concise role skills separate judgment and challenge while preserving shared evidence. Finance does not generate market signals; Research does not calculate statements; Scenario does not validate itself; QA does not edit the scenario it reviews. Financial arithmetic remains deterministic to keep reconciliations testable. This design offers inspectable handoffs without pretending the roles have independent external source access.

Implementation used official OpenAI documentation for [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode) and [configuration controls](https://learn.chatgpt.com/docs/config-file/config-reference), and checked the installed CLI help. The CLI runtime must be smoke-tested on the execution host; unit tests alone establish no authentication or model-call success.

## Fresh rerun versus replay

A fresh eight-case experiment always creates a new timestamped run directory. It makes 32 new model calls and may change judgments. Existing output directories are rejected; the first experiment remains immutable. Explicit locations are useful for downstream artifact generation:

```sh
python3 src/prepare_packets.py
python3 src/run_case_studies.py --run-root outputs/runs_20261003_experiment
python3 src/workflow.py replay --run outputs/runs_20261003_experiment/PG_pre_history
```

Omit `--run-root` to receive a fresh UTC timestamp automatically. `--packets-dir` accepts another prepared packet directory. Each experiment copies its starting packets under its own `prepared_packets`; the market packets then receive that experiment's frozen, matched history-control assumptions. The selected accepted experiment is published under `outputs/runs`; rejected original market evidence is retained under `outputs/rejected_runs`. The original launch predated the fresh-root default. Frozen file bytes are unchanged.

For public distribution, preserve every path listed in each `freeze.json`, including role inputs, prompts, outputs and run metadata. Raw `events.jsonl` and `runtime.stderr.txt` are not freeze dependencies and may be omitted because they can contain local runtime identifiers or host paths. Retain them privately for troubleshooting. The public execution summary should contain real status, timestamps, usage and QA findings without local paths or session IDs. Hashes establish retained-byte consistency, not independent proof of source truth.

## Evidence completeness and content-vintage review

A publication-date field alone cannot prove that every sentence is available at that date. The first market batch exposed a future revision value embedded in an otherwise eligible record's overlap note; those market outputs were rejected and never frozen. Revised packets require review of the entire record, including annotations and provenance, for later information. The initial review remains in `outputs/rejected_runs/review.json`.

Short quotations may not contain every numerical fact in a multi-claim record. Located factual transcriptions can supply additional original-source data, but they are labeled as transcriptions rather than quotations. The Research curator records a separate source inspection and locator audit. QA distinguishes checking a supplied fact record from independently verifying its transcription or authenticating the external webpage. Missing support and contradictions remain blockers; an explicitly limited model-coherence pass never certifies external source accuracy.

## Source-only QA re-review

A rejected review may receive newly inspected original-source support without changing the forecast assumptions:

```sh
python3 src/workflow.py review-qa --run outputs/runs/PG_pre_market --supplement inputs/prequarter_rounding_review.json
```

This is one additional genuine QA model call. The rejected review moves to `qa_initial`; its bytes, the original three upstream role results and the supplemental evidence remain retained. QA independently decides whether the new source evidence resolves the blockers. A successful freeze hashes both QA reviews and the supplement; a rejection produces no freeze. Accepted runs cannot be modified through this command. Source rounding footnotes explain only justified display residuals and never license ignoring material contradictions or changing reported numbers.

A QA supplement must be a curated JSON object with a nonempty `reviews` list. Each entry must identify an existing packet `source_id` and its original `publication_date`, no later than the packet cutoff, plus the original supporting rows/footnotes and locators. Review timestamps record execution time separately. Do not give a pre-quarter review later-published financial data. The accepted case retains its exact eligible supplement in `qa_supplement.json`.
