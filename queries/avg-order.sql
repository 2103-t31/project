SELECT COUNT(*) as 'Number of Orders',SUM(q.value) as 'Total Order Value', Quarter
FROM  (SELECT
	pc.cartID,
	sc.value,
	(STRFTIME('%m', pc.datePurchased) + 2) / 3 as Quarter
FROM
	shoppingCarts sc
INNER JOIN purchasedCart pc 
ON
	sc.cartID = pc.cartID
WHERE
	sc.value <
(
	SELECT
		AVG(sc.value)
	FROM
		shoppingCarts sc
	INNER JOIN purchasedCart pc 
ON
		sc.cartID = pc.cartID)) q
GROUP BY quarter