SELECT
    `Product ID`,
    `Product Name`,
    `Retail Price`,
    SUM(quantity) AS 'Total Units Sold',
    SUM(`Sale Quantity`) AS 'Total Units Sold at Discount',
    SUM(`Retail Quantity`) AS 'Total Units Sold at Retail',
    ROUND(SUM(`Transaction Amount`), 2) AS 'Actual Revenue',
    ROUND(SUM(`Predicted Amount`), 2) AS 'Predicted Revenue',
    ROUND(SUM(InnerSelect.Difference), 2) AS 'Difference'
FROM
    (SELECT
        S.PID AS 'Product ID',
        P.productName AS 'Product Name',
        ROUND(P.price, 2) AS 'Retail Price',
        transactionDate,
        IF(ISNULL(G.salePrice), 0, quantity) AS 'Sale Quantity',
        IF(ISNULL(G.salePrice), quantity, 0) AS 'Retail Quantity',
        quantity * IF(ISNULL(G.salePrice), P.price, G.salePrice) AS 'Transaction Amount',
        IF(ISNULL(G.salePrice), quantity * P.price, 0.75 * quantity * P.price) AS 'Predicted Amount',
        quantity * IF(ISNULL(G.salePrice), P.price, G.salePrice) -
            IF(ISNULL(G.salePrice), quantity * P.price, 0.75 * quantity * P.price) AS 'Difference',
        quantity
    FROM StoreSellsProduct S
    JOIN CategorizedBy C
        ON S.PID = C.PID AND C.categoryName = "GPS"
    JOIN Product P
        ON S.PID = P.PID
    LEFT OUTER JOIN GoesOnSale G
        ON S.PID = G.PID AND transactionDate = saleDate
    ) AS InnerSelect
GROUP BY `Product ID`, `Product Name`, `Retail Price`
HAVING ABS(Difference) > 5000
ORDER BY `Difference` DESC, `Product ID`;
