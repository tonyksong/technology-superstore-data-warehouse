SELECT
Product.PID AS `PID`,
productName AS `Name`,
GROUP_CONCAT(DISTINCT categoryName SEPARATOR ', ') AS `Categories`,
ROUND(price, 2)
FROM Product, CategorizedBy
WHERE
      CategorizedBy.PID = Product.PID AND manufacturerName = %s
GROUP BY Product.PID
ORDER BY price DESC;

