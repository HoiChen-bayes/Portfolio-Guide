# Independent calculation review

Eight deterministic tests passed against eligible prior-year financial data and synthetic targets. The tests do not read target company outcomes. A synthetic full run also passed thirty reconciliation checks and preserved the original raw-unit dictionary alongside normalized model metrics.

The review checked historical reconstruction; positive capex treatment; catastrophe and favorable-reserve signs; conversion from percentage-point source ratios to model decimals; written-versus-earned separation; share-denominator effects; cash-versus-profit channels; the all-freezes-before-actuals boundary; signed variance and absolute-percentage-error definitions; and the residual in the sequential actual bridge.

Initial issues were corrected in the implementation: actuals gating, Travelers' unused share driver, spreadsheet units, ambiguous error-percent labeling, incomplete formula parity and cropped render ranges. Travelers now reports a core-income-per-diluted-share proxy, explicitly distinct from reported core EPS.

The workbook code checks every displayed metric for all twelve cases, every editable driver's propagation, numeric finiteness and formula error strings. The generated verification reports were subsequently inspected: both companies have zero differences across all recorded formula-parity rows, and all nine editable drivers propagate to an output. This checks the workbook library calculation results; it is not a claim of opening the files in native Excel. The structured [review record](../../outputs/qa/independent_model_review.json) contains the reviewed file hashes and UTC timestamp. Later changes require checking whether that review still applies.

A fixed accounting-basis offset, independent written/earned assumptions and simplified cash conversion remain model limitations. Sequential bridges are order-dependent numerical explanations, not causal attribution. None of these tests proves statistical predictive accuracy.
