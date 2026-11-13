import sqlite3


def view_expiry_alerts(role):

    if role not in ["admin", "user"]:
        print("Access Denied!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            medicines.medicine_name,
            medicine_batches.batch_number,
            medicine_batches.quantity,
            medicine_batches.expiry_date,
            CASE
                WHEN medicine_batches.expiry_date < date('now')
                    THEN 'EXPIRED'
                WHEN medicine_batches.expiry_date <= date('now', '+30 days')
                    THEN 'EXPIRING SOON'
                ELSE 'NOT NEAR EXPIRY'
            END AS expiry_status
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id = medicines.medicine_id
        WHERE medicine_batches.expiry_date <= date('now', '+30 days')
        ORDER BY medicine_batches.expiry_date ASC
    """)

    batches = cursor.fetchall()

    print("\n===== MEDICINE EXPIRY ALERTS =====")

    if batches:
        for batch in batches:
            print("--------------------------------")
            print("Medicine Name:", batch[0])
            print("Batch Number:", batch[1])
            print("Quantity:", batch[2])
            print("Expiry Date:", batch[3])
            print("Status:", batch[4])
    else:
        print("No expired or soon-to-expire batches found.")

    conn.close()