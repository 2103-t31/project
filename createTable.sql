CREATE TABLE Customer(
	custID char(20) NOT NULL,
	firstName char(20),
	lastName char(20),
	userName char(20),
	email char(50),
	PRIMARY KEY (custID)
);

CREATE TABLE Visits(
	visitID char(20) NOT NULL,
	deviceType char(20),
	startDatetime char(20),
	exitDatetime char(20),
	Mchannel char(20),
	PRIMARY KEY (visitID)
);

CREATE TABLE makes(
	custID char(20),
	visitID char(20),
	PRIMARY KEY (visitID),
	FOREIGN KEY (custID) REFERENCES Customer(custID),
	FOREIGN KEY (visitID) REFERENCES Visits(visitID)
);

CREATE TABLE shoppingCarts(
	cartID char(20) NOT NULL,
	value DECIMAL(5, 2),
	dateCreated DATETIME,
	PRIMARY KEY (cartID)
);

CREATE TABLE has(
	custID char(20) NOT NULL,
	cartID char(20) NOT NULL,
	PRIMARY KEY (custID, cartID),
	FOREIGN KEY (custID) REFERENCES Customer(custID),
	FOREIGN KEY (cartID) REFERENCES shoppingCarts(cartID)
);

CREATE TABLE purchasedCart(
	cartID char(20) NOT NULL,
	datePurchased DATETIME,
	discountValue DECIMAL(5, 2),
	PRIMARY KEY (cartID),
	FOREIGN KEY (cartID) REFERENCES shoppingCarts(cartID) ON DELETE CASCADE
);

CREATE TABLE abandonedCart(
	discountValue DECIMAL(5, 2),
	cartID char(20) NOT NULL,
	PRIMARY KEY (cartID),
	FOREIGN KEY (cartID) REFERENCES shoppingCarts(cartID) ON DELETE CASCADE
);

CREATE TABLE Products(
	productID char(20) NOT NULL,
	productName char(60),
	unitPrice DECIMAL(5,2),
	stockCount INT,
	PRIMARY KEY (productID)
);

CREATE TABLE contains(
	cartID char(20) NOT NULL,
	productID char(20) NOT NULL,
	quantity INT,
	PRIMARY KEY (productID, cartID),
	FOREIGN KEY (cartID) REFERENCES shoppingCarts(cartID),
	FOREIGN KEY (productID) REFERENCES Products(productID)
);

CREATE TABLE Category(
	categoryID char(20) NOT NULL PRIMARY KEY,
	description char(200),
	categoryName char(50)
);

CREATE TABLE BelongsTo(
	categoryID char(20),
	productID char(20),
	PRIMARY KEY (categoryID, productID),
	FOREIGN KEY (categoryID) REFERENCES Category(categoryID),
	FOREIGN KEY (productID) REFERENCES Products(productID)
);
