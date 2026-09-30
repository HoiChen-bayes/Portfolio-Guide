-- Full-period controls; raw amounts are unscaled USD estimates.
SELECT COUNT(*) AS line_count, COUNT(DISTINCT "Order Number") AS orders,
       SUM(Quantity) AS units, SUM(Revenue) AS estimated_sales,
       SUM("Gross Profit") AS estimated_gross_profit
FROM E2_Priced_Sales_Lines;

SELECT Year, Channel, SUM(Revenue) AS estimated_sales,
       COUNT(DISTINCT "Order Number") AS orders,
       SUM(Revenue)/COUNT(DISTINCT "Order Number") AS estimated_aov
FROM E2_Priced_Sales_Lines
GROUP BY Year, Channel ORDER BY Year, Channel;
