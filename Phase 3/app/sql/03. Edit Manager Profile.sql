SELECT managerName, emailAddress FROM Manager ORDER BY managerName;
INSERT INTO Manager(emailAddress, managerName) VALUES (%s, %s);
UPDATE Manager SET managerName = %s WHERE emailAddress = %s;
DELETE FROM Manages WHERE emailAddress = %s;
SELECT storeNumber, emailAddress FROM Manages WHERE emailAddress = %s;
DELETE FROM Manager WHERE emailAddress = %s;
SELECT COUNT(emailAddress) FROM Manages WHERE emailAddress = %s;
DELETE FROM Manager WHERE emailAddress = %s;
