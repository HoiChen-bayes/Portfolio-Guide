# Public run paths

The accepted local run set named `outputs/runs_reviewed` is published as `outputs/runs`. All files listed in every freeze manifest preserve their exact original bytes, so replay verifies normally. Original path names inside JSON provenance are retained and refer to this mapping; they are not external links.

The four rejected original market packets and QA decisions are in `outputs/rejected_runs`. P&G source-only QA re-reviews retain `qa_initial` and their exact source supplements inside the accepted case folders. Raw runtime events and stderr are omitted; freeze verification does not depend on them.
