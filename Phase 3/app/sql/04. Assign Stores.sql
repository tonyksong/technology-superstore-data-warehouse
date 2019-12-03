SELECT storeNumber FROM Manages WHERE emailAddress = %s ORDER BY storeNumber;
SELECT emailAddress FROM Manages WHERE storeNumber = %s ORDER BY emailAddress;
INSERT INTO Manages(storeNumber, emailAddress) VALUES(%s, %s);
DELETE FROM Manages WHERE emailAddress = %s AND storeNumber = %s;
SELECT GROUP_CONCAT(S.storeNumber SEPARATOR ', ') FROM Store S WHERE S.storeNumber NOT IN (SELECT M.storeNumber FROM Manages M);
SELECT storeNumber, managerName, Manages.emailAddress FROM Manages JOIN Manager ON Manages.emailAddress = Manager.emailAddress ORDER BY Manages.storeNumber, managerName;
SELECT storeNumber, storeNumber FROM Store ORDER BY storeNumber;
SELECT emailAddress, CONCAT(managerName, ' (', emailAddress, ')') FROM Manager ORDER BY managerName;