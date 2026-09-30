-- SQLite. Run against F11_Forecast_Backtest.sqlite.
-- One-month-ahead retrospective exercise; assume prior month closed at month-end.
-- Target-month actuals are used only for scoring, never as model features.
CREATE VIEW monthly AS
SELECT month,segment,SUM(units) units,SUM(sales) sales,SUM(cogs) cogs,SUM(profit) profit
FROM source GROUP BY month,segment;
CREATE VIEW features AS
SELECT month,segment,sales actual,
 LAG(month) OVER w training_end,
 LAG(sales) OVER w last_sales,
 LAG(units) OVER w last_units,
 COUNT(*) OVER prior3 n_prior,
 AVG(sales) OVER prior3 avg_sales,
 SUM(sales) OVER prior3 prior_sales,
 SUM(units) OVER prior3 prior_units
FROM monthly
WINDOW w AS (PARTITION BY segment ORDER BY month),
 prior3 AS (PARTITION BY segment ORDER BY month ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING);
CREATE VIEW forecasts AS
SELECT month,segment,training_end,actual,'Last month' method,last_sales forecast
FROM features WHERE month BETWEEN '2014-04' AND '2014-12' AND n_prior=3
UNION ALL
SELECT month,segment,training_end,actual,'Trailing 3 months',avg_sales
FROM features WHERE month BETWEEN '2014-04' AND '2014-12' AND n_prior=3
UNION ALL
SELECT month,segment,training_end,actual,'Recent volume x pooled price',last_units*prior_sales/NULLIF(prior_units,0)
FROM features WHERE month BETWEEN '2014-04' AND '2014-12' AND n_prior=3;
CREATE VIEW forecast_errors AS
SELECT *, CASE WHEN month<='2014-09' THEN 'Development' ELSE 'Holdout' END sample,
 forecast-actual error,ABS(forecast-actual) absolute_error
FROM forecasts;
-- Development scores choose the method; holdout scores do not reselect it.
SELECT sample,method,COUNT(*) observations,
 SUM(absolute_error)/SUM(ABS(actual)) segment_month_wape,
 SUM(error)/SUM(ABS(actual)) signed_bias
FROM forecast_errors GROUP BY sample,method ORDER BY sample,segment_month_wape;
