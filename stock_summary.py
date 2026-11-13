import sqlite3


def view_stock_summary(role):

    if role != "admin":
        print("Access Denied! Admin only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT medicines.medicine_name,
               COUNT(medicine_batches.batch_id),
               SUM(medicine_batches.quantity)
        FROM medicines
        LEFT JOIN medicine_batches
        ON medicines.medicine_id = medicine_batches.medicine_id
        GROUP BY medicines.medicine_id
    """)

    stocks = cursor.fetchall()

    print("\n===== STOCK SUMMARY =====")

    if stocks:
        for stock in stocks:
            print("-------------------------")
            print("Medicine Name:", stock[0])
            print("Total Batches:", stock[1])
            print("Total Quantity:", stock[2] if stock[2] is not None else 0)
    else:
        print("No medicines found.")

    conn.close()