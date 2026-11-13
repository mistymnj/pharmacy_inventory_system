import sqlite3


def create_activity_table():

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_role TEXT,
            action TEXT,
            details TEXT,
            activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def log_activity(username, role, action, details):

    create_activity_table()

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity_log
        (username, user_role, action, details)
        VALUES (?, ?, ?, ?)
    """, (username, role, action, details))

    conn.commit()
    conn.close()


def view_activity_log(role):

    if role != "admin":
        print("Access Denied! Admin only.")
        return

    create_activity_table()

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT log_id, username, user_role,
               action, details, activity_date
        FROM activity_log
        ORDER BY log_id DESC
    """)

    activities = cursor.fetchall()

    print("\n===== USER ACTIVITY LOG =====")

    if activities:
        for activity in activities:
            print("----------------------------")
            print("Log ID:", activity[0])
            print("Username:", activity[1])
            print("Role:", activity[2])
            print("Action:", activity[3])
            print("Details:", activity[4])
            print("Date:", activity[5])
    else:
        print("No activity recorded.")

    conn.close()