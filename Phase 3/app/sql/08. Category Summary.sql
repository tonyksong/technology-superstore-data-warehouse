SELECT C.categoryName AS Category, COUNT(CB.PID) AS `Number of Products`,
COUNT(DISTINCT P.manufacturerName) AS `Number of Manufacturers`, ROUND(AVG(P.price), 2) AS `Average Price`
FROM Category C JOIN CategorizedBy CB ON C.categoryName = CB.categoryName JOIN Product P ON CB.PID = P.PID
GROUP BY C.categoryName ORDER BY C.categoryName;
