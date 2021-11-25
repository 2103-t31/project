select
	t.productID,
	t.productName ,
	SUM(t.quantity) as total_sold
from
	(
	select
		c.cartID,
		c.productID,
		c.quantity,
		p.productName
	from
		contains c
	left join products p on
		p.productID = c.productID
	where
		c.cartID in (
		select
			cartID
		from
			purchasedcart )) t
group by
	t.productID
order by
	SUM(t.quantity) desc;