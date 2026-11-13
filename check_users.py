import sqlite3

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute("SELECT username, role FROM users")
users = cursor.fetchall()

print("Registered Users:")

for user in users:
    print("Username:", user[0], "| Role:", user[1])

conn.close()