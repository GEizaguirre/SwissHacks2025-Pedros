import mysql.connector

# Establish the connection to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='svcr-db'
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Step 1: Show all tables in the database
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# Step 2: Print contents of each table
for table in tables:
    table_name = table[0]
    # Get the number of rows in the table
    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`;")
    row_count = cursor.fetchone()[0]  # Get the row count from the result
    # Print the table name and row count
    print(f"Table: {table_name}, Number of rows: {row_count}")
    
    # Fetch and print the column names
    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 1;")  # Get one row to fetch column names
    column_names = [desc[0] for desc in cursor.description]  # Extract column names
    print(f"Columns: {', '.join(column_names)}")
    
    # Make sure to fetch all results before executing another query
    cursor.fetchall()  # This will clear any pending result set
    
    # Fetch and print the first 10 rows of the table
    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 10;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    
    print("-" * 40)

# Close the cursor and connection
cursor.close()
connection.close()
