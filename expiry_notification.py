import sqlite3
from datetime import datetime


def show_expiry_notifications(role):

    if role != "admin":
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    print("\n================================")
    print("     MEDICINE EXPIRY ALERTS")
    print("================================")

    # Check expired medicines
    cursor.execute("""
        SELECT medicines.medicine_name,
               medicine_batches.batch_number,
               medicine_batches.quantity,
               medicine_batches.expiry_date
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id =
           medicines.medicine_id
        WHERE date(medicine_batches.expiry_date) < date(?)
        AND medicine_batches.quantity > 0
        ORDER BY medicine_batches.expiry_date
    """, (today,))

    expired = cursor.fetchall()

    print("\n!!! EXPIRED MEDICINES !!!")

    if expired:
        for item in expired:
            print("--------------------------------")
            print("Medicine:", item[0])
            print("Batch:", item[1])
            print("Quantity:", item[2])
            print("Expiry Date:", item[3])
            print("Status: EXPIRED")
    else:
        print("No expired medicines found.")

    # Check medicines expiring within 30 days
    cursor.execute("""
        SELECT medicines.medicine_name,
               medicine_batches.batch_number,
               medicine_batches.quantity,
               medicine_batches.expiry_date
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id =
           medicines.medicine_id
        WHERE date(medicine_batches.expiry_date)
        BETWEEN date(?) AND date(?, '+30 days')
        AND medicine_batches.quantity > 0
        ORDER BY medicine_batches.expiry_date
    """, (today, today))

    expiring = cursor.fetchall()

    print("\n!!! EXPIRING WITHIN 30 DAYS !!!")

    if expiring:
        for item in expiring:
            print("--------------------------------")
            print("Medicine:", item[0])
            print("Batch:", item[1])
            print("Quantity:", item[2])
            print("Expiry Date:", item[3])
            print("Status: EXPIRING SOON")
    else:
        print("No medicines expiring within 30 days.")

    print("\n================================")

    conn.close()