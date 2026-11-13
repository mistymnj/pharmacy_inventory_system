import sqlite3


def view_low_stock_alerts(role):

    if role not in ["admin", "user"]:
        print("Access Denied!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT medicines.medicine_name,
               medicine_batches.batch_number,
               medicine_batches.quantity
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id = medicines.medicine_id
        WHERE medicine_batches.quantity <= 10
        ORDER BY medicine_batches.quantity ASC
    """)

    batches = cursor.fetchall()

    print("\n===== LOW STOCK ALERTS =====")

    if batches:
        for batch in batches:
            print("----------------------------")
            print("Medicine Name:", batch[0])
            print("Batch Number:", batch[1])
            print("Available Quantity:", batch[2])
            print("Status: LOW STOCK")
    else:
        print("No low-stock medicines found.")

    conn.close()