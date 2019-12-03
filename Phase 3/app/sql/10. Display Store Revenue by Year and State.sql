SELECT
	Store.storeNumber,
	Store.streetAddress,
	City.cityName,
	YEAR(StoreSellsProduct.transactionDate) AS Year,
	ROUND(SUM(IF(StoreSellsProduct.transactionDate = GoesOnSale.saleDATE AND
		StoreSellsProduct.PID = GoesOnSale.PID,GoesOnSale.salePrice, Product.price)
		* StoreSellsProduct.quantity),2) AS Revenue
FROM
	StoreSellsProduct
LEFT OUTER JOIN
	GoesOnSale
ON
	StoreSellsProduct.transactionDate = GoesOnSale.saleDATE AND
		StoreSellsProduct.PID = GoesOnSale.PID,
	Product,
	Store,
	City
WHERE 
	City.state = %s
	AND Store.state = %s
	AND Store.cityName = City.cityName
	AND StoreSellsProduct.storeNumber = Store.storeNumber
	AND StoreSellsProduct.PID = Product.PID
GROUP BY
	Store.storeNumber,
	Store.streetAddress,
	City.cityName,
	YEAR(StoreSellsProduct.transactionDate)
ORDER BY 
	Year, 
	Revenue DESC;
