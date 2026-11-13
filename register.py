import sqlite3
import hashlib
import os
from getpass import getpass


def hash_password(password):

    salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return salt.hex() + ":" + hashed.hex()


def register_user(username, password, confirm_password):

    if not username or not password:
        print("Username and password cannot be empty!")
        return

    if password != confirm_password:
        print("Passwords do not match!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone():
        print("Username Already Exists!")

    else:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, hashed_password, "user"))

        conn.commit()

        print("User Registered Successfully!")

    conn.close()


if __name__ == "__main__":

    username = input("Enter Username: ")
    password = getpass("Enter Password: ")
    confirm_password = getpass("Confirm Password: ")

    register_user(username, password, confirm_password)