-- Display the Air Conditioners on Groundhog Day Report Screen.

SELECT
	YEAR(StoreSellsProduct.transactionDate) AS Year,
	SUM(StoreSellsProduct.quantity) AS `Total AC Items Sold`,
	ROUND(SUM(StoreSellsProduct.quantity)/365, 0) AS
		`Average (Rounded) Number of Units Sold/Day`,
	GH.Total AS `Total Units Sold on GroundHog Day`
FROM
	StoreSellsProduct,
	CategorizedBy,
	(
		SELECT
			SUM(StoreSellsProduct.quantity) AS Total,
			YEAR(StoreSellsProduct.transactionDate) AS Year
		FROM
			StoreSellsProduct,
			CategorizedBy
		WHERE
			Categorizedby.categoryName = 'Air Conditioner' AND
			StoreSellsProduct.PID = Categorizedby.PID AND
			DATE_FORMAT(StoreSellsProduct.transactionDate,'%m-%d') = '02-02'
		GROUP BY 
		YEAR(StoreSellsProduct.transactionDate)
	) AS GH
WHERE
	Categorizedby.categoryName = 'Air Conditioner' AND
	StoreSellsProduct.PID = Categorizedby.PID AND
	GH.Year = YEAR(StoreSellsProduct.transactionDate)
GROUP BY
	YEAR(StoreSellsProduct.transactionDate),
	GH.Total
ORDER BY 
	YEAR ASC;
