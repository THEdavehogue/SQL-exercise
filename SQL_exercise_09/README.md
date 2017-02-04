To set up this exercise, navigate to this directory from the command line. Run this command:

```bash
bash setup.sh
```

This will install `pandas` and `sqlalchemy` if they are not already installed. Then, the `setup_db.py` script will create the database from the cran_logs_2015-01-01.csv file.


**NOTE: The installation of pandas and sqlalchemy depends on having Anaconda as your package manager, and the database engine used in this exercise is PostgreSQL**


-- 9.1 give the total number of recordings in this table
```sql
SELECT COUNT(*) AS count_all
FROM cran_logs;
```

-- 9.2 the number of packages listed in this table?
```sql
SELECT COUNT(*) AS count_pkg
FROM (
    SELECT DISTINCT package FROM cran_logs
) unique_pkgs;
```

-- 9.3 How many times the package "Rcpp" was downloaded?
```sql
SELECT COUNT(*) AS count_Rcpp
FROM cran_logs
WHERE package = 'Rcpp';
```

-- 9.4 How many recordings are from China ("CN")?
```sql
SELECT COUNT(*) AS count_CN
FROM cran_logs
WHERE country = 'CN';
```
-- 9.5 Give the package name and how many times they're downloaded. Order by the 2nd column in descending order.
```sql
SELECT package, COUNT(*) AS count_pkg
FROM cran_logs
GROUP BY package
ORDER BY count_pkg DESC;
```
-- 9.6 Give the package ranking (based on how many times it was downloaded) during 9AM to 11AM
```sql
SELECT package, count(*) AS downloads
FROM cran_logs
WHERE time >= '09:00:00'
AND time <= '11:00:00'
GROUP BY package
ORDER BY downloads DESC;
```

-- 9.7 How many recordings are from China ("CN") or Japan("JP") or Singapore ("SG")?
--    Select based on a given list.
```sql
SELECT country, COUNT(*) AS downloads
FROM cran_logs
WHERE country IN ('CN', 'JP', 'SG')
GROUP BY country;
```


-- 9.8 Print the countries whose downloaded are more than the downloads from China ("CN")

```sql
WITH count_country AS (
    SELECT country, COUNT(*) AS cnt
    FROM cran_logs
    GROUP BY country
    ORDER BY cnt desc
)
SELECT country
FROM count_country
WHERE cnt > (
    SELECT cnt from count_country
    WHERE country = 'CN'
);
```

-- 9.9 Print the average length of the package name of all the UNIQUE packages

```sql
WITH pkgs AS (
    SELECT DISTINCT package, LENGTH(package) AS len
    FROM cran_logs
)
SELECT AVG(len)
FROM pkgs;
```


-- 9.10 Get the package whose downloading count ranks 2nd (print package name and it's download count).

```sql
WITH top_two AS (
    SELECT package, COUNT(*) AS downloads
    FROM cran_logs
    GROUP BY package
    ORDER BY downloads DESC
    LIMIT 2
)
SELECT package, downloads
FROM top_two
WHERE downloads = (
    SELECT MIN(downloads)
    FROM top_two
);
```


-- 9.11 Print the name of the package whose download count is bigger than 1000.

```sql
SELECT package, downloads
FROM (
    SELECT package, COUNT(*) AS downloads
    FROM cran_logs
    GROUP BY package
) AS count_downloads
WHERE downloads > 1000;
```

-- 9.12 The field "r_os" is the operating system of the users.
-- 	Here we would like to know what main system we have (ignore version number), the relevant counts, and the proportion (in percentage).
```sql
WITH count_os AS (
    SELECT SUBSTR(r_os, 1, 5) AS os, COUNT(*) as cnt
    FROM cran_logs
    GROUP BY os
)
SELECT os, ROUND(100.0 * cnt / (SELECT SUM(cnt) FROM count_os), 2) || '%'  as download_pct
FROM count_os;
```

-- Here we use INT*1.0 to conver an integer to float so that we can compute compute the percentage (1/5 can be 0.2 instead of 0)
-- || is an alternative of CONCAT() in SQLite.
-- SUBSTR(field, start_position, length) is used to get a part of a character string.
-- [] can help use spaces in the aliases.
