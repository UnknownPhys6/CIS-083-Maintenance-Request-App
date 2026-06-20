import mysql.connector

cnx = mysql.connector.connect(
    user="developer",
    password="Group2pass",
    host="192.168.1.144",
    database="maintenance_requests",
    port=3306
)

print("Connected!")

cnx.close()