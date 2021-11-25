CREATE VIEW androidVisits2 (totalVisits) AS
	SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android";

SELECT ((SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID	
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android" and v.Mchannel = "Direct"
	)
	/
	(SELECT totalVisits FROM androidVisits2)
	)
	AS directAndroid;


SELECT ((SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID	
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android" and v.Mchannel = "Email"
	)
	/
	(SELECT totalVisits FROM androidVisits2)
	)
	AS emailAndroid;

SELECT ((SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID	
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android" and v.Mchannel = "Affiliates"
	)
	/
	(SELECT totalVisits FROM androidVisits2)
	)
	AS affiliatesAndroid;

SELECT ((SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID	
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android" and v.Mchannel = "Paid Search"
	)
	/
	(SELECT totalVisits FROM androidVisits2)
	)
	AS paidAndroid;

SELECT ((SELECT COUNT(*) FROM visits v
	INNER JOIN makes m
	ON v.visitID = m.visitID
	INNER JOIN has h
	ON m.custID = h.custID	
	INNER JOIN purchasedcart p
	ON h.cartID = p.cartID
	WHERE v.deviceType = "Android" and v.Mchannel = "Natural Search"
	)
	/
	(SELECT totalVisits FROM androidVisits2)
	)
	AS naturalAndroid;