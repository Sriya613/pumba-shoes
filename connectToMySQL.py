import mysql.connector as cn
password = 'enter_your_password_here'

try:
    # Connect to the MySQL server without specifying a database
    mydb = cn.connect(
        host='127.0.0.1',
        user='root',
        port=3306,  # Sets port to 3306 if DB_PORT is not defined
        password=password,
        database='shoeStore',
        use_pure=True,
        unix_socket=None
    )
    if mydb.is_connected():
        print("Connected to MySQL!")

    # Create the database if it doesn't exist
    create_database_query = f"CREATE DATABASE IF NOT EXISTS shoeStore"
    mycursor = mydb.cursor()
    mycursor.execute(create_database_query)
    print("Database created or already exists")

    # Connect to the specific database
    mydb = cn.connect(
        host='127.0.0.1',
        user='root',
        password=password,
        database='shoeStore',
    )
    if mydb.is_connected():
        print(f"Connected to 'shoeStore'")

except cn.Error as e:
    print(f'Error connecting to MySQL: {e}')


# Define table creation queries
table_queries = [
    '''
    CREATE TABLE IF NOT EXISTS Admin (
        id INT PRIMARY KEY,
        username VARCHAR(20),
        password VARCHAR(20)
    )
    ''',
    '''
    DROP TABLE IF EXISTS Customers
    ''',
    '''
    DROP TABLE IF EXISTS Shoes
    ''',
    '''
    DROP TABLE IF EXISTS Orders
    ''',
    # Create Customers Table
    '''
    CREATE TABLE IF NOT EXISTS Customers (
        phone VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255),
        order_id INT
    )
    ''',

    # Insert Sample Data into Customers Table
    '''
    INSERT INTO Customers (phone, name, order_id) VALUES
        ('1256789034', 'Alice', 1),
        ('0987654321', 'Bob', 2),
        ('5551234567', 'Charlie', 3),
        ('2223334444', 'David', 4),
        ('6667778888', 'Eva', 5)
    ''',

    # Create Shoes Table
    '''
    CREATE TABLE IF NOT EXISTS Shoes (
        numModel INT,
        color VARCHAR(50),
        size INT,
        quantity INT,
        floor INT,
        season VARCHAR(50),
        PRIMARY KEY (numModel, color, size, season)
    )
    ''',

    # Insert Sample Data into Shoes Table
    '''
    INSERT INTO Shoes (numModel, color, size, quantity, floor, season) VALUES
        (101, 'Red', 42, 10, 1, 'Summer'),
        (102, 'Blue', 40, 5, 2, 'Winter'),
        (103, 'Black', 38, 8, 1, 'Spring'),
        (104, 'White', 44, 12, 3, 'Fall'),
        (105, 'Green', 39, 6, 2, 'Summer')
    ''',

    # Create Orders Table
    '''
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
    )
    ''',

    # Insert Sample Data into Orders Table
    '''
    INSERT INTO Orders (numModel, price, size, floor, name, phone, color, order_date) VALUES
        (101, 1059.99, 42, 1, 'Alice', '1256789034', 'Red', '2024-11-01'),
        (102, 1089.50, 40, 2, 'Bob', '0987654321', 'Blue', '2024-11-02'),
        (103, 2245.75, 38, 1, 'Charlie', '5551234567', 'Black', '2024-11-03'),
        (104, 1220.00, 44, 3, 'David', '2223334444', 'White', '2024-11-04'),
        (105, 1605.25, 39, 2, 'Eva', '6667778888', 'Green', '2024-11-05')
    '''
]


try:
    # Get the cursor before executing the queries
    mycursor = mydb.cursor()

    for query in table_queries:
        mycursor.execute(query)
    print("Tables created successfully")

except cn.Error as e:
    print(f'Error creating tables: {e}')
