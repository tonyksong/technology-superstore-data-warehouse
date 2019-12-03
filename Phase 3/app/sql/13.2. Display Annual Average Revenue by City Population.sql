-- Display the Annual Average Revenue by City Population Report Screen.

SELECT
	YEARS.`Year`,

	ROUND(IFNULL(smallCategory, 0), 2) AS `Small Category`,
	ROUND(IFNULL(mediumCategory, 0), 2) AS `Medium Category`,
	ROUND(IFNULL(largeCategory, 0), 2) AS `Large Category`,
	ROUND(IFNULL(extraLargeCategory, 0), 2) AS `Extra Large Category`,

	ROUND(IFNULL(smallCategory/smallCount, 0), 2) AS `Small Category Avg`,
	ROUND(IFNULL(mediumCategory/mediumCount, 0), 2) AS `Medium Category Avg`,
	ROUND(IFNULL(largeCategory/largeCount, 0), 2) AS `Large Category Avg`,
	ROUND(IFNULL(extraLargeCategory/extraLargeCount, 0), 2) AS `Extra Large Category Avg`
FROM
	(
		SELECT 
			DISTINCT YEAR(transactionDate) AS `Year`
		FROM 
			StoreSellsProduct SSP
	) AS YEARS
LEFT JOIN
	(
		SELECT
			YEAR(transactionDate) AS `Year`,
			ROUND(
				SUM(quantity * 
				IF(ISNULL(GOS.salePrice), P.price, GOS.salePrice)),
				2) AS `smallCategory`,
			COUNT(C.cityName) AS `smallCount`
		FROM 
			StoreSellsProduct SSP
		JOIN 
			Product P
		ON 	
			P.PID = SSP.PID
		JOIN 
			Store S
		ON 
			S.storeNumber = SSP.storeNumber
		JOIN 
			City C
		ON 
			C.cityName = S.cityName 
			AND C.state = S.state 
			AND C.population < 3700000
		LEFT OUTER JOIN 
			GoesOnSale GOS
		ON 
			SSP.transactionDate = GOS.saleDate 
			AND SSP.PID = GOS.PID
		GROUP BY 
			YEAR(transactionDate)
	) AS SMALL
ON 
	YEARS.`Year` = SMALL.`Year`
LEFT JOIN
	(
		SELECT
			YEAR(transactionDate) AS `Year`,
			ROUND(
				SUM(quantity * IF(ISNULL(GOS.salePrice), 
					P.price, GOS.salePrice)),
				2) AS `mediumCategory`,
			COUNT(C.cityName) AS `mediumCount`
		FROM 
			StoreSellsProduct SSP
		JOIN 
			Product P
		ON 
			P.PID = SSP.PID
		JOIN 
			Store S
		ON 
			S.storeNumber = SSP.storeNumber
		JOIN 
			City C
		ON 
			C.cityName = S.cityName 
			AND C.state = S.state 
			AND C.population < 6700000 
			AND C.population >= 3700000
		LEFT OUTER JOIN 
			GoesOnSale GOS
		ON 
			SSP.transactionDate = GOS.saleDate 
			AND SSP.PID = GOS.PID
		GROUP BY 
			YEAR(transactionDate)
	) AS MEDIUM
ON 
	YEARS.`Year` = MEDIUM.`Year`
LEFT JOIN
	(
		SELECT
			YEAR(transactionDate) AS `Year`,
			ROUND(
				SUM(quantity * 
					IF(ISNULL(GOS.salePrice), P.price, GOS.salePrice)),
				2) AS `largeCategory`,
			COUNT(C.cityName) AS `largeCount`
		FROM 
			StoreSellsProduct SSP
		JOIN 
			Product P
		ON 
			P.PID = SSP.PID
		JOIN 
			Store S
		ON 
			S.storeNumber = SSP.storeNumber
		JOIN 
			City C
		ON 
			C.cityName = S.cityName 
			AND C.state = S.state 
			AND C.population < 9000000 
			AND C.population >= 6700000
		LEFT OUTER JOIN GoesOnSale GOS
		ON 
			SSP.transactionDate = GOS.saleDate 
			AND SSP.PID = GOS.PID
		GROUP BY 
		YEAR(transactionDate)
	) AS LARGE
ON 
	YEARS.`Year` = LARGE.`Year`
LEFT JOIN
	(
		SELECT
			YEAR(transactionDate) AS `Year`,
			ROUND(
				SUM(quantity 
					* IF(ISNULL(GOS.salePrice), P.price, GOS.salePrice)),
				2) AS `extraLargeCategory`,
			COUNT(C.cityName) AS `extraLargeCount`
		FROM 
			StoreSellsProduct SSP
		JOIN 
			Product P
		ON 
			P.PID = SSP.PID
		JOIN 
			Store S
		ON 
			S.storeNumber = SSP.storeNumber
		JOIN City C
		ON 
			C.cityName = S.cityName 
			AND C.state = S.state 
			AND C.population >= 9000000
		LEFT OUTER JOIN 
			GoesOnSale GOS
		ON 
			SSP.transactionDate = GOS.saleDate 
			AND SSP.PID = GOS.PID
		GROUP BY 
			YEAR(transactionDate)
	) AS EXTRALARGE
ON 
	YEARS.`Year` = EXTRALARGE.`Year`
ORDER BY YEARS.`Year`;