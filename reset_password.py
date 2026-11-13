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


def reset_password(username, new_password, confirm_password):

    if not username or not new_password:
        print("Username and password cannot be empty!")
        return

    if new_password != confirm_password:
        print("Passwords do not match!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user:

        hashed_password = hash_password(new_password)

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE username = ?
        """, (hashed_password, username))

        conn.commit()

        print("Password Reset Successfully!")

    else:
        print("Username Not Found!")

    conn.close()


if __name__ == "__main__":
    username = input("Enter Username: ")
    new_password = getpass("Enter New Password: ")
    confirm_password = getpass("Confirm New Password: ")

    reset_password(username, new_password, confirm_password)