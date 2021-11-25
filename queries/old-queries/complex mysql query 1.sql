CREATE TABLE quarterlyPerformance (
	Quarter char(10) NOT NULL,
	OrdersAboveAverage int,
	PRIMARY KEY (Quarter)
	);


INSERT INTO quarterlyPerformance (Quarter)
	VALUES
	("Quarter 1"),
	("Quarter 2"),
	("Quarter 3"),
	("Quarter 4");

UPDATE quarterlyPerformance
	SET OrdersAboveAverage = (
	SELECT COUNT(*) FROM (
	SELECT * FROM shoppingcarts
	WHERE dateCreated LIKE '2021-01%'
	OR
	dateCreated LIKE '2021-02%'
	OR
	dateCreated LIKE '2021-03%'
	) sub
	WHERE sub.value > (SELECT AVG(value) FROM shoppingcarts)
	)
	WHERE Quarter = "Quarter 1";

UPDATE quarterlyPerformance
	SET OrdersAboveAverage = (
	SELECT COUNT(*) FROM (
	SELECT * FROM shoppingcarts
	WHERE dateCreated LIKE '2021-04%'
	OR
	dateCreated LIKE '2021-05%'
	OR
	dateCreated LIKE '2021-06%'
	) sub
	WHERE sub.value > (SELECT AVG(value) FROM shoppingcarts)
	)
	WHERE Quarter = "Quarter 2";

UPDATE quarterlyPerformance
	SET OrdersAboveAverage = (
	SELECT COUNT(*) FROM (
	SELECT * FROM shoppingcarts
	WHERE dateCreated LIKE '2021-07%'
	OR
	dateCreated LIKE '2021-08%'
	OR
	dateCreated LIKE '2021-09%'
	) sub
	WHERE sub.value > (SELECT AVG(value) FROM shoppingcarts)
	)
	WHERE Quarter = "Quarter 3";

UPDATE quarterlyPerformance
	SET OrdersAboveAverage = (
	SELECT COUNT(*) FROM (
	SELECT * FROM shoppingcarts
	WHERE dateCreated LIKE '2021-10%'
	OR
	dateCreated LIKE '2021-11%'
	OR
	dateCreated LIKE '2021-12%'
	) sub
	WHERE sub.value > (SELECT AVG(value) FROM shoppingcarts)
	)
	WHERE Quarter = "Quarter 4";