-- State Volume by Category Report Screen and 
-- Populate the month/year dropdown from:

SELECT
	DISTINCT DATE_FORMAT(StoreSellsProduct.transactionDate,'%m-%Y')
FROM 
	StoreSellsProduct
ORDER BY
	DATE_FORMAT(StoreSellsProduct.transactionDate,'%m-%Y') DESC;


-- Generate Report button clicked: (State Volume by Category Report)

SELECT 
	Category, State, Units
FROM
(
	SELECT 
		unitsCategory AS Category, MAX(units) AS Units
	FROM
	(
		SELECT 
			CAT.categoryName AS unitsCategory, 
			City.state, SUM(quantity) AS units
		FROM 
			StoreSellsProduct SSP
		JOIN Product P ON P.PID = SSP.PID
		JOIN Store S ON SSP.storeNumber = S.storeNumber
		JOIN City ON City.cityName = S.cityName AND City.state = S.state
		JOIN CategorizedBy CB ON CB.PID = SSP.PID
		JOIN Category CAT ON CAT.categoryName = CB.categoryName
		WHERE
			MONTH(SSP.transactionDate) = '$month' AND
			YEAR(SSP.transactionDate) = '$year'
		GROUP BY CAT.categoryName, City.state
	) AS Q1
	
	GROUP BY unitsCategory
) AS Q2
JOIN
(
	SELECT
		CAT.categoryName AS stateCategory,
		City.state AS State,
		SUM(quantity) AS stateUnits
		FROM 
			StoreSellsProduct SSP
		JOIN 
			Product P ON P.PID = SSP.PID
		JOIN 
			Store S ON SSP.storeNumber = S.storeNumber
		JOIN 
			City ON City.cityName = S.cityName AND City.state = S.state
		JOIN 
			CategorizedBy CB ON CB.PID = SSP.PID
		JOIN 
			Category CAT ON CAT.categoryName = CB.categoryName
		WHERE
			MONTH(SSP.transactionDate) = '$month' AND
			YEAR(SSP.transactionDate) = '$year'
		GROUP BY 
			CAT.categoryName, City.state
) AS Q3
	ON Category = stateCategory AND Units = stateUnits
ORDER BY Category




-- drill-down

SELECT
	Store.storeNumber AS `Store Number`,
	streetAddress AS `Address`,
	cityName AS City,
	IFNULL(managerName, '[No manager assigned]') AS Manager,
	Manager.emailAddress AS Email 
FROM
	Store 
LEFT JOIN
	Manages 
	ON Manages.storeNumber = Store.storeNumber 
LEFT JOIN
	Manager 
	ON Manager.emailAddress = Manages.emailAddress 
WHERE 
	Store.state = '$state' 
ORDER BY 
	Store.storeNumber, managerName;