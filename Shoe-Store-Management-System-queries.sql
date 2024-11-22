CREATE DATABASE IF NOT EXISTS shoeStore;

CREATE TABLE IF NOT EXISTS Admin (
        id INT PRIMARY KEY,
        username VARCHAR(20),
        password VARCHAR(20)
    );

CREATE TABLE IF NOT EXISTS Customers (
        phone VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255),
        order_id INT
    );
    
INSERT INTO Customers (phone, name, order_id) VALUES
        ('1256789034', 'Alice', 1),
        ('0987654321', 'Bob', 2),
        ('5551234567', 'Charlie', 3),
        ('2223334444', 'David', 4),
        ('6667778888', 'Eva', 5);
        
CREATE TABLE IF NOT EXISTS Shoes (
        numModel INT,
        color VARCHAR(50),
        size INT,
        quantity INT,
        floor INT,
        season VARCHAR(50),
        PRIMARY KEY (numModel, color, size, season)
    );

INSERT INTO Shoes (numModel, color, size, quantity, floor, season) VALUES
        (101, 'Red', 42, 10, 1, 'Summer'),
        (102, 'Blue', 40, 5, 2, 'Winter'),
        (103, 'Black', 38, 8, 1, 'Spring'),
        (104, 'White', 44, 12, 3, 'Fall'),
        (105, 'Green', 39, 6, 2, 'Summer');

CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        numModel INT,
        price DECIMAL(10, 2),
        size INT,
        floor INT,
        name VARCHAR(20),
        phone VARCHAR(20),
        color VARCHAR(20),
        order_date DATE
    );

INSERT INTO Orders (numModel, price, size, floor, name, phone, color, order_date) VALUES
        (101, 1059.99, 42, 1, 'Alice', '1256789034', 'Red', '2024-11-01'),
        (102, 1089.50, 40, 2, 'Bob', '0987654321', 'Blue', '2024-11-02'),
        (103, 2245.75, 38, 1, 'Charlie', '5551234567', 'Black', '2024-11-03'),
        (104, 1220.00, 44, 3, 'David', '2223334444', 'White', '2024-11-04'),
        (105, 1605.25, 39, 2, 'Eva', '6667778888', 'Green', '2024-11-05');

-- quantityInStockQUERY
SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s;

-- inserting_to_stock
INSERT INTO shoes (numModel, color, size, quantity ,floor, season) VALUES (%s, %s, %s, %s, %s, %s);

-- updateQuery
UPDATE shoes SET quantity = %s WHERE numModel = %s AND color = %s AND size = %s season = %s;

-- checkIfmodelExist
SELECT * FROM SHOES WHERE numModel = %s AND size = %s AND color = %s;

-- add purchase
INSERT INTO Orders (numModel, price, size, floor, name, phone, color,order_date) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);
INSERT INTO Customers (phone, name, order_id) VALUES (%s, %s, %s);
SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s;
UPDATE shoes SET quantity = %s Where numModel = %s AND size = %s AND color = %s AND season = %s AND floor = %s;

-- elevated privileges
SELECT * FROM Admin WHERE username = %s AND password = %s;

-- summary page
SELECT Orders.order_id, Orders.numModel, Orders.price, Orders.size, Orders.color, Orders.order_date, Customers.name AS customer_name, Customers.phone FROM Orders JOIN Customers ON Orders.phone = Customers.phone;

-- query to calculate the sum of orders for the current day
SELECT SUM(price) FROM Orders WHERE order_date = %s;

-- nested query to calculate the sum of orders for the current month
SELECT SUM(profit) AS monthly_profit FROM (SELECT price AS profit FROM Orders WHERE MONTH(order_date) = MONTH(CURRENT_DATE()) AND YEAR(order_date) = YEAR(CURRENT_DATE())) AS MonthlyProfits;