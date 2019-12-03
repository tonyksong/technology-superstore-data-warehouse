-- Display manuf summ
SELECT
    manufacturerName,
    COUNT(PID),
    ROUND(AVG(price), 2),
    ROUND(MIN(price), 2),
    ROUND(MAX(price), 2)
FROM Product
GROUP BY manufacturerName ORDER BY AVG(price) DESC LIMIT 100;
