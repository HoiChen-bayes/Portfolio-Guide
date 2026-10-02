# Reproduce this sample

1. Download the two official files listed in `raw_data/source_manifest.json` into `raw_data/` using the recorded filenames.
2. Run `python3 src/extract.py` with openpyxl, pdfplumber and pypdf installed. It extracts the company spreadsheet, checks numeric occurrences on the annual-report page and saves a source-page copy, CSV and JSON.
3. Run `python3 src/extend_data.py` to extract the balance sheet and cash flow and prepare original-page evidence. It also contains the reviewed transcription of company business drivers; update these from the specified pages when changing source years. Then run `node src/build.mjs` in an environment providing `@oai/artifact-tool`. It builds the Excel analysis, recalculates it and tests the profit bridge and one input change.
4. Run a fresh Financial review using `agents/financial.md`, followed by an independent review using `agents/qa.md`. Preserve the returned review records and resolve issues before publication.
5. Open the exported workbook in Microsoft Excel, check its display and recapture the complete populated worksheets. Render the annotated source PDF. Screenshots are dated evidence and must be refreshed after changing inputs.

The current scripts reproduce the data and workbook. Agent review is a separately invoked step; this sample does not claim a fully automated five-agent service.
