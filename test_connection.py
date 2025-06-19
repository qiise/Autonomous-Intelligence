import mysql.connector

try:
    connection = mysql.connector.connect(
        user='root',
        unix_socket='/var/run/mysqld/mysqld.sock',
        database='agents'  # Make sure this database exists
    )
    print("Connection successful!")
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
