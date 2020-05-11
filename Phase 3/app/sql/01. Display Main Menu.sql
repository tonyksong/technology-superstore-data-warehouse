SELECT COUNT(storeNumber) AS 'Number of Stores' FROM Store;
SELECT COUNT(manufacturerName) AS 'Number of Manufacturers' FROM Manufacturer;
SELECT COUNT(PID) AS 'Number of Products' FROM Product;
SELECT COUNT(categoryName) FROM Category;
SELECT COUNT(emailAddress) AS 'Number of Managers' FROM Manager;
SELECT COUNT(DISTINCT emailAddress) AS 'Number of Active Managers' FROM Manages;
SELECT COUNT(*) FROM (SELECT S.storeNumber AS store, M.storeNumber AS managed FROM Store S LEFT OUTER JOIN Manages M ON S.storeNumber = M.storeNumber WHERE ISNULL(M.storeNumber)) C;
SELECT COUNT(*) FROM StoreSellsProduct;
SELECT COUNT(*) FROM GoesOnSale;
SELECT COUNT(*) FROM Holiday;
SELECT DATABASE();
SELECT SYSTEM_USER();