-- State Volume by Category Report Screen and
-- Populate the month/year dropdown from:

SELECT DISTINCT tDate
FROM
	(SELECT
		DATE_FORMAT(StoreSellsProduct.transactionDate,'%m-%Y') AS `tDate`
	FROM
		StoreSellsProduct) AS D
ORDER BY
	SUBSTRING(tDate, 4, 4) DESC, SUBSTRING(tDate, 1, 2) DESC;
