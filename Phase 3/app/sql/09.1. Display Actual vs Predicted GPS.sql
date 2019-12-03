

-- my original method ... * WRONG *
SELECT
		ActualAndPredictedRevTable.PID,
		ActualAndPredictedRevTable.price,
		ActualAndPredictedRevTable.productName,
		ActualAndPredictedRevTable.allUnitsSold,
		ActualAndPredictedRevTable.discountUnitsSold,
		ActualAndPredictedRevTable.retailUnitsSold,
		ActualAndPredictedRevTable.actualRevenue,
		ActualAndPredictedRevTable.predictedRevenue,
		ABS(ActualAndPredictedRevTable.actualRevenue - ActualAndPredictedRevTable.predictedRevenue) as difference
FROM
(SELECT
		RetailAndDiscountsTable.PID,
		RetailAndDiscountsTable.price,
		RetailAndDiscountsTable.productName,
		RetailAndDiscountsTable.allUnitsSold,
		RetailAndDiscountsTable.discountUnitsSold,
		RetailAndDiscountsTable.retailUnitsSold,
		(RetailAndDiscountsTable.discountUnitsSold * RetailAndDiscountsTable.salePrice + (RetailAndDiscountsTable.allUnitsSold - RetailAndDiscountsTable.discountUnitsSold) * RetailAndDiscountsTable.price) as actualRevenue,
		((RetailAndDiscountsTable.allUnitsSold - RetailAndDiscountsTable.discountUnitsSold) * RetailAndDiscountsTable.price + (RetailAndDiscountsTable.discountUnitsSold * RetailAndDiscountsTable.price * 0.75)) as predictedRevenue
FROM

-- on X1, find retail sales. (using allunits table and discount table)
(SELECT	
		AllUnitsTable.PID, 
		AllUnitsTable.productName,
		AllUnitsTable.price,
		IFNULL(DiscountsUnitsTable.salePrice, 0) as salePrice,
		AllUnitsTable.allUnitsSold, 
		IFNULL(DiscountsUnitsTable.discountUnitsSold, 0) as discountUnitsSold, 
		(AllUnitsTable.allUnitsSold - IFNULL(DiscountsUnitsTable.discountUnitsSold, 0)) as retailUnitsSold
FROM 

-- change this to all units table again, and left join with discount table to form X1
(SELECT
		product.PID as PID, 
		product.productName as productName, 
		SUM(storesellsproduct.quantity) as allUnitsSold
		#SUM(product.price*storesellsproduct.quantity) as RetailSale
FROM product, storesellsproduct, categorizedby, goesonsale
WHERE 	categorizedby.categoryName = 'GPS' AND
		categorizedby.PID = product.PID AND
		product.PID = storesellsproduct.PID
		#goesonsale.PID = product.PID AND
		#storesellsproduct.transactionDate <> goesonsale.saleDate
GROUP BY product.PID) as AllUnitsTable

LEFT OUTER JOIN 

-- below is pristine..
(SELECT 
		product.PID as PID, 
		product.productName as productName, 
		SUM(storesellsproduct.quantity) as discountUnitsSold, 
		SUM(goesonsale.salePrice*storesellsproduct.quantity)) as discountSale
		SUM(product.price*storesellsproduct.quantity*0.75) as predictedRetailSale
FROM product, storesellsproduct, categorizedby, goesonsale
WHERE 	categorizedby.categoryName = 'GPS' AND
		categorizedby.PID = product.PID AND
		product.PID = storesellsproduct.PID AND
        storesellsproduct.transactionDate = goesonsale.saleDate AND
        goesonsale.PID = product.PID
GROUP BY product.PID, goesonsale.salePrice) as DiscountTable 

ON AllUnitsTable.PID = DiscountsUnitsTable.PID
GROUP BY AllUnitsTable.PID, DiscountsUnitsTable.discountUnitsSold, DiscountsUnitsTable.salePrice) as RetailAndDiscountsTable) as ActualAndPredictedRevTable
#WHERE ABS(ActualAndPredictedRevTable.actualRevenue - ActualAndPredictedRevTable.predictedRevenue) > 5000
ORDER BY difference DESC;