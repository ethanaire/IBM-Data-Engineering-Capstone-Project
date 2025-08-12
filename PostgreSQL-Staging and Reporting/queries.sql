-- Create a grouping sets query using the columns country, category, totalsales.
SELECT cou.COUNTRY, cat.CATEGORY, SUM(sa.AMOUNT) AS totalsales
FROM FACTSALES sa
LEFT JOIN DIMCOUNTRY cou ON sa.COUNTRYID = cou.COUNTRYID
LEFT JOIN DIMCATEGORY cat ON sa.CATEGORYID = cat.CATEGORYID
GROUP BY GROUPING SETS (cou.COUNTRY, cat.CATEGORY)
ORDER BY cou.COUNTRY, cat.CATEGORY;

-- Create a rollup query using the columns year, country, and totalsales.
SELECT dat.YEAR, cou.COUNTRY, SUM(sa.AMOUNT) AS totalsales
FROM FACTSALES sa
LEFT JOIN DIMDATE dat ON sa.DATEID = dat.DATEID 
LEFT JOIN DIMCOUNTRY cou ON sa.COUNTRYID = cou.COUNTRYID
GROUP BY ROLLUP (dat.YEAR, cou.COUNTRY)
ORDER BY dat.YEAR, cou.COUNTRY;

-- Create a cube query using the columns year, country, and average sales.
SELECT cou.COUNTRY, dat.YEAR, AVG(sa.AMOUNT) AS totalsales
FROM FACTSALES sa
LEFT JOIN DIMDATE dat ON sa.DATEID = dat.DATEID 
LEFT JOIN DIMCOUNTRY cou ON sa.COUNTRYID = cou.COUNTRYID
GROUP BY CUBE(cou.COUNTRY, dat.YEAR)
ORDER BY cou.COUNTRY, dat.YEAR;

-- Create an MQT named total_sales_per_country that has the columns country and total_sales.
CREATE TABLE total_sales_per_country(country, total_sales) AS
(SELECT 
	cou.COUNTRY,
	SUM(sa.AMOUNT) as total_sales
FROM FACTSALES sa
LEFT JOIN DIMCOUNTRY cou ON sa.COUNTRYID = cou.COUNTRYID
GROUP BY cou.COUNTRY)
DATA INITIALLY DEFERRED REFRESH DEFERRED;

REFRESH TABLE total_sales_per_country;


