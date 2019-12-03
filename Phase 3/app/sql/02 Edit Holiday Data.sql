SELECT holidayName, holidayDate FROM Holiday ORDER BY holidayDate DESC;
INSERT INTO Holiday (holidayDate, holidayName) VALUES (%s, %s);
UPDATE Holiday SET holidayName = %s WHERE holidayDate = %s;
