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
	Store.state= %s
ORDER BY 
	Store.storeNumber, managerName;