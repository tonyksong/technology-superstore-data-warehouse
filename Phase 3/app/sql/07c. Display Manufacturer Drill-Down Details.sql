SELECT
    maximumDiscount,
    COUNT(PID),
    ROUND(AVG(price), 2),
    ROUND(MIN(price), 2),
    ROUND(MAX(price), 2)
FROM Product P, Manufacturer M
WHERE P.manufacturerName = M.manufacturerName AND M.manufacturerName = %s;