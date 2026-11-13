import sqlite3


def record_purchase(role):

    if role != "admin":
        print("Access Denied! Admin only.")
        return

    medicine_id = input("Enter Medicine ID: ")
    batch_number = input("Enter Batch Number: ")
    quantity = input("Enter Purchased Quantity: ")
    manufacturing_date = input("Enter Manufacturing Date (YYYY-MM-DD): ")
    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
    purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

    try:
        quantity = int(quantity)

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

    except ValueError:
        print("Invalid quantity!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medicine_batches
        (medicine_id, batch_number, quantity,
         manufacturing_date, expiry_date, purchase_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        medicine_id,
        batch_number,
        quantity,
        manufacturing_date,
        expiry_date,
        purchase_date
    ))

    conn.commit()
    conn.close()

    print("Purchase recorded successfully!")