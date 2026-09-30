# Monthly update and version checks

[Original validation output](../outputs/FP&A_extensions/F18_验证记录.json) · [Frozen database](../outputs/FP&A_extensions/F18_已验证版本/sample_2014_12_v1.sqlite) · [Update script](../outputs/FP&A_extensions/F18_月度更新与版本冻结.py)

This local process checks monthly completeness and sales and profit totals before creating a a dated copy of the data. Re-running identical data does not append duplicate records.

![Recorded update checks](images/F18-validation-1.svg)

Both columns are text: **Check** identifies the test; **Result** is the result. The frozen database contains sample records and the original data references, not a live cloud connection.
