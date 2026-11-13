import sqlite3
import hashlib
import getpass
from activity_log import log_activity


def verify_password(password, stored_password):

    # Check hashed password
    if ":" in stored_password:

        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            100000
        )

        return new_hash.hex() == hash_hex

    # Check old plain-text Admin password
    return password == stored_password


def login_user(username, password):

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, password, role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user:

        stored_password = user[2]

        if verify_password(password, stored_password):

            # Upgrade old plain-text password to hashed format
            if ":" not in stored_password:

                import os

                salt = os.urandom(16)

                hashed = hashlib.pbkdf2_hmac(
                    "sha256",
                    password.encode(),
                    salt,
                    100000
                )

                new_password = salt.hex() + ":" + hashed.hex()

                cursor.execute("""
                    UPDATE users
                    SET password = ?
                    WHERE username = ?
                """, (new_password, username))

                conn.commit()

            print("Login successful!")
            print("Welcome,",user[1])
            print("Role:",user[3])
            role=user[3]
            log_activity(
                user[1],
                role,
                "LOGIN",
                "User logged in successfully"
            )
            conn.close()
            return role, user[0]

    print("Invalid username or password")

    conn.close()
    return False


if __name__ == "__main__":
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    login_user(username, password)