import mysql.connector
from config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)

    if connection.is_connected():
        print("MySQL connected successfully!")

    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)