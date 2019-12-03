SELECT cityName, state, population FROM City ORDER BY state, cityName;
SELECT CONCAT(cityName, '|', state) as `cityValue`, CONCAT(cityName, ', ', state) as `city` FROM City ORDER BY state, cityName;
UPDATE City SET Population = %s WHERE cityName = %s AND State = %s;