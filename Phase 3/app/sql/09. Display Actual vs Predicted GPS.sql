-- Display the GPS Report Screen.
SELECT
	`Product ID`,
	`Product Name`,
	`Retail Price`,
	SUM(`Total Quantity`) AS 'Total Units Sold',
	SUM(`Sale Quantity`) AS 'Total Units Sold at Discount',
	SUM(`Retail Quantity`) AS 'Total Units Sold at Retail',
	SUM(`Transaction Amount`) AS 'Actual Revenue',
	ROUND(SUM(`Predicted Amount`), 2) AS 'Predicted Revenue',
	ROUND(SUM(Difference), 2) AS 'Difference'
FROM 
(
	SELECT
		S.PID AS 'Product ID',
		P.productName AS 'Product Name',
		P.price AS 'Retail Price',
		IFNULL(G.salePrice, 0) AS 'Sale Price',
		C.categoryName,
		storeNumber,
		transactionDate,
		SUM(IF(ISNULL(G.salePrice), 0, quantity)) AS 'Sale Quantity',
		SUM(IF(ISNULL(G.salePrice), quantity, 0)) AS 'Retail Quantity',
		SUM(quantity * IF(ISNULL(G.salePrice), P.price, G.salePrice)) AS 'Transaction Amount',
		SUM(IF(ISNULL(G.salePrice), quantity * P.price, 0.75 * quantity * P.price)) AS 'Predicted Amount', 
		quantity * IF(ISNULL(G.salePrice), P.price, G.salePrice) -
			SUM(IF(ISNULL(G.salePrice), quantity * P.price, 0.75 * quantity * P.price)) AS 'Difference',
		SUM(quantity) AS `Total Quantity`
	FROM 
		StoreSellsProduct S
	JOIN 
		CategorizedBy C
	ON 
		S.PID = C.PID 
		AND C.categoryName = "GPS"
	JOIN 
		Product P
	ON 
		S.PID = P.PID
	LEFT OUTER JOIN 
		GoesOnSale G
	ON 
		S.PID = G.PID 
		AND transactionDate = saleDate
	GROUP BY 
		S.PID, 
		P.productName, 
		P.price, 
		salePrice, 
		C.categoryName,
		storeNumber, 
		transactionDate
) AS InnerSelect
GROUP BY 
	`Product ID`, 
	`Product Name`, 
	`Retail Price`
HAVING ABS(Difference) > 5000
ORDER BY 
	`Difference` DESC, 
	`Product ID`;