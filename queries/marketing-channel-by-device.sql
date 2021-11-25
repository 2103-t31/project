SELECT
	v.deviceType as 'Device Type',
	v.Mchannel as 'Marketing Channel',
	SUM(sc.value) as 'Total Order Value',
	COUNT(*) as 'Order Count',
	SUM(sc.value)/Count(*) as 'Average Order Value'
FROM
	visits v
INNER JOIN makes m
ON
	v.visitID = m.visitID
INNER JOIN has h
ON
	m.custID = h.custID
INNER JOIN purchasedcart p
ON
	h.cartID = p.cartID
INNER JOIN shoppingCarts sc 
ON
	p.cartID = sc.cartID
GROUP BY
	v.deviceType,
	v.Mchannel
