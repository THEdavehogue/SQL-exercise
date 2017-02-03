-- Used pSQL for this example

-- 10.1 Join table PEOPLE and ADDRESS, but keep only one address information for each person (we don't mind which record we take for each person).
-- i.e., the joined table should have the same number of rows as table PEOPLE

`Not sure how to keep a random address record except keeping max/min which doesn't make much sense. Kept most recent address, which is answer to 10.2`


```sql
WITH max_date as (
SELECT p.id, MAX(a.updatedate) as latest
FROM people p
LEFT JOIN address a ON p.id = a.id
GROUP BY p.id
)

SELECT md.id, a.address, md.latest
from max_date md
LEFT JOIN address a ON md.id = a.id AND md.latest = a.updatedate;
```

-- 10.2 Join table PEOPLE and ADDRESS, but ONLY keep the LATEST address information for each person.
-- i.e., the joined table should have the same number of rows as table PEOPLE

id |   address   |   latest   
|----|-------------|------------
 1 | address-1-2 | 2016-09-02
 2 | address-2-1 | 2015-11-01
 3 | address-3-1 | 2016-12-01
 4 | address-4-3 | 2015-04-27
(4 rows)
