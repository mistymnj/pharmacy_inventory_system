import sqlite3


def view_purchase_history(role):

    if role != "admin":
        print("Access Denied! Admin only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT medicines.medicine_name,
               medicine_batches.batch_number,
               medicine_batches.quantity,
               medicine_batches.purchase_date
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id = medicines.medicine_id
        ORDER BY medicine_batches.purchase_date DESC
    """)

    purchases = cursor.fetchall()

    print("\n===== PURCHASE HISTORY =====")

    if purchases:
        for purchase in purchases:
            print("---------------------------")
            print("Medicine Name:", purchase[0])
            print("Batch Number:", purchase[1])
            print("Quantity Purchased:", purchase[2])
            print("Purchase Date:", purchase[3])
    else:
        print("No purchase history found.")

    conn.close()