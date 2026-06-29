"""
This file is just used for testing locally.
I know its bad practice to post login credentials to the internet, I'll change it to use .env files later
"""
import mysql.connector
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

try:
    cnx = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))  # Defaults to 3306 if DB_PORT isn't set
    )

    print("Connected successfully")
    cnx.close()

except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
