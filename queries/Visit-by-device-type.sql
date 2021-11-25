SELECT count(*) AS 'Visits per Device Type'
FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	GROUP BY deviceType
