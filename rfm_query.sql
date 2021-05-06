-- reference: https://lifetimes.readthedocs.io/en/latest/More%20examples%20and%20recipes.html

CREATE TABLE ecomm_oct
(
	event_time DATE,
	event_type VARCHAR(10),
	product_id INTEGER,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT,
	price REAL,
	user_id INTEGER,
	user_session TEXT
);

CREATE TABLE ecomm_nov
(
	event_time DATE,
	event_type VARCHAR(10),
	product_id INTEGER,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT,
	price REAL,
	user_id INTEGER,
	user_session TEXT
);


WITH purchased_ecomm_oct AS
(
	SELECT *
	FROM ecomm_oct
	WHERE event_type = 'purchase'
),
purchased_ecomm_nov AS
(
	SELECT *
	FROM ecomm_nov
	WHERE event_type = 'purchase'
),
avg_monetary AS
(
	SELECT user_id, AVG(price) AS avg_monetary
	FROM
	(
		SELECT 
			user_id, 
			event_time, 
			SUM(price) AS price, 
			ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY event_time ASC) AS rn
		FROM purchased_ecomm_oct
		GROUP BY user_id, event_time
	) AS purchased_ecomm_oct_rown
	WHERE rn != 1
	GROUP BY user_id
)
SELECT
	rfm_oct.*,
	COALESCE(m_oct.avg_monetary, 0) AS monetary,
	COALESCE(f_nov.frequency_holdout, 0) AS frequency_holdout,
	30 AS duration_holdout
FROM
(
	SELECT 
		user_id, 
		MAX(event_time) - MIN(event_time) as recency, 
		COUNT(DISTINCT event_time) -1 AS frequency, 
		'2019-10-31' - MIN(event_time) as T
	FROM purchased_ecomm_oct
	GROUP BY user_id
) AS rfm_oct
LEFT JOIN
(
	SELECT
		user_id,
		COUNT(DISTINCT event_time) AS frequency_holdout
	FROM purchased_ecomm_nov
	GROUP BY user_id
) AS f_nov
ON rfm_oct.user_id = f_nov.user_id
LEFT JOIN
(
	SELECT user_id, avg_monetary
	FROM avg_monetary
) AS m_oct
ON rfm_oct.user_id = m_oct.user_id


-- WITH purchased_ecomm_nov AS
-- (
-- 	SELECT *
-- 	FROM ecomm_nov
-- 	WHERE event_type = 'purchase'
-- )
-- SELECT
-- 	user_id,
-- 	AVG(sum_monetary) AS monetary
-- FROM
-- (
-- 	SELECT 
-- 		user_id,
-- 		event_time,
-- 		SUM(price) AS sum_monetary
-- 	FROM purchased_ecomm_nov
-- 	GROUP BY user_id, event_time
-- ) AS t1
-- GROUP BY user_id

