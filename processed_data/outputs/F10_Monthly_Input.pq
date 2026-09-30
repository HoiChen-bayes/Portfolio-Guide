let
    Files = Folder.Files(InputFolder),
    CsvFiles = Table.SelectRows(Files, each Text.Lower([Extension]) = ".csv"),
    Batches = Table.AddColumn(CsvFiles, "Period", each Text.BeforeDelimiter([Name], "."), type text),
    DuplicateMonths = Table.SelectRows(Table.Group(Batches, {"Period"}, {{"Count", each Table.RowCount(_), Int64.Type}}), each [Count] <> 1),
    CheckedFiles = if Table.RowCount(DuplicateMonths) > 0 then error "Keep exactly one complete file per month." else Batches,
    Parsed = Table.AddColumn(CheckedFiles, "Data", (r) => let
        T = Table.PromoteHeaders(Csv.Document(r[Content], [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]), [PromoteAllScalars=true]),
        Trimmed = Table.TransformColumnNames(T, Text.Trim),
        Typed = Table.TransformColumnTypes(Trimmed, {{"SourceRow", Int64.Type}, {"Segment", type text}, {"Country", type text}, {"Product", type text}, {"Discount Band", type text}, {"Manufacturing Price", type number}, {"Sale Price", type number}, {"Month Number", Int64.Type}, {"Month Name", type text}, {"Year", Int64.Type}, {"Date", type date}, {"Units Sold", type number}, {"Gross Sales", type number}, {"Discounts", type number}, {"Sales", type number}, {"COGS", type number}, {"Profit", type number}}, "en-US"),
        WrongPeriod = Table.SelectRows(Typed, each Date.ToText([Date], "yyyy-MM") <> r[Period] or Date.Day([Date]) <> 1),
        Result = if Table.RowCount(WrongPeriod) > 0 then error "File month and row Date do not agree." else Typed
        in Result),
    Combined = Table.Combine(Parsed[Data])
in Combined
