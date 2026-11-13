import sqlite3
from datetime import date, datetime


def purchase_medicine(user_id):

    conn = sqlite3.connect("pharmacy.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        print("\n===== AVAILABLE MEDICINES =====")

        cursor.execute("""
            SELECT medicine_id, medicine_name, unit_price
            FROM medicines
            ORDER BY medicine_id
        """)

        medicines = cursor.fetchall()

        if not medicines:
            print("No medicines available.")
            return

        for medicine in medicines:
            print(
                f"Medicine ID: {medicine[0]} | "
                f"Name: {medicine[1]} | "
                f"Price: Rs. {medicine[2]:.2f}"
            )

        medicine_id = int(input("\nEnter Medicine ID: "))

        cursor.execute("""
            SELECT medicine_name, unit_price
            FROM medicines
            WHERE medicine_id = ?
        """, (medicine_id,))

        medicine = cursor.fetchone()

        if medicine is None:
            print("Invalid Medicine ID.")
            return

        medicine_name = medicine[0]
        unit_price = medicine[1]

        today = date.today().isoformat()

        cursor.execute("""
            SELECT batch_id, batch_number, quantity, expiry_date
            FROM medicine_batches
            WHERE medicine_id = ?
            AND quantity > 0
            AND expiry_date >= ?
            ORDER BY expiry_date
        """, (medicine_id, today))

        batches = cursor.fetchall()

        if not batches:
            print("No eligible stock available.")
            return

        print("\n===== AVAILABLE BATCHES =====")

        for batch in batches:
            print(
                f"Batch ID: {batch[0]} | "
                f"Batch Number: {batch[1]} | "
                f"Quantity: {batch[2]} | "
                f"Expiry Date: {batch[3]}"
            )

        batch_id = int(input("\nEnter Batch ID: "))

        selected_batch = None

        for batch in batches:
            if batch[0] == batch_id:
                selected_batch = batch
                break

        if selected_batch is None:
            print("Invalid Batch ID.")
            return

        quantity_available = selected_batch[2]

        quantity = int(input("Enter Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        if quantity > quantity_available:
            print("Insufficient stock.")
            return

        total_price = quantity * unit_price

        print("\n===== BILL DETAILS =====")
        print("Medicine:", medicine_name)
        print("Quantity:", quantity)
        print(f"Unit Price: Rs. {unit_price:.2f}")
        print(f"Total Bill: Rs. {total_price:.2f}")

        confirm = input("\nConfirm Purchase? (yes/no): ")

        if confirm.lower() != "yes":
            print("Purchase cancelled.")
            return

        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO sales (user_id, sale_date, total_amount)
            VALUES (?, ?, ?)
        """, (user_id, sale_date, total_price))

        sale_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO sale_items (
                sale_id,
                medicine_id,
                batch_id,
                quantity,
                unit_price,
                total_price
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sale_id,
            medicine_id,
            batch_id,
            quantity,
            unit_price,
            total_price
        ))

        cursor.execute("""
            UPDATE medicine_batches
            SET quantity = quantity - ?
            WHERE batch_id = ?
            AND quantity >= ?
        """, (quantity, batch_id, quantity))

        if cursor.rowcount != 1:
            raise ValueError("Stock update failed.")

        conn.commit()

        print("\nPurchase recorded successfully!")
        print("Sale ID:", sale_id)
        print(f"Total Amount: Rs. {total_price:.2f}")

    except ValueError as error:
        conn.rollback()
        print("Error:", error)

    except sqlite3.Error as error:
        conn.rollback()
        print("Database Error:", error)

    finally:
        conn.close()


def view_my_purchases(user_id):

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            sales.sale_id,
            sales.sale_date,
            medicines.medicine_name,
            sale_items.quantity,
            sale_items.total_price
        FROM sales
        JOIN sale_items
            ON sales.sale_id = sale_items.sale_id
        JOIN medicines
            ON sale_items.medicine_id = medicines.medicine_id
        WHERE sales.user_id = ?
        ORDER BY sales.sale_id DESC
    """, (user_id,))

    purchases = cursor.fetchall()

    print("\n===== MY PURCHASE HISTORY =====")

    if not purchases:
        print("No purchases found.")

    else:
        for purchase in purchases:
            print(
                f"Sale ID: {purchase[0]} | "
                f"Date: {purchase[1]} | "
                f"Medicine: {purchase[2]} | "
                f"Quantity: {purchase[3]} | "
                f"Total: Rs. {purchase[4]:.2f}"
            )

    conn.close()


def view_all_sales():

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            sales.sale_id,
            users.username,
            sales.sale_date,
            medicines.medicine_name,
            sale_items.quantity,
            sale_items.total_price
        FROM sales
        JOIN users
            ON sales.user_id = users.user_id
        JOIN sale_items
            ON sales.sale_id = sale_items.sale_id
        JOIN medicines
            ON sale_items.medicine_id = medicines.medicine_id
        ORDER BY sales.sale_id DESC
    """)

    sales_records = cursor.fetchall()

    print("\n===== ALL SALES HISTORY =====")

    if not sales_records:
        print("No sales recorded.")

    else:
        for sale in sales_records:
            print(
                f"Sale ID: {sale[0]} | "
                f"User: {sale[1]} | "
                f"Date: {sale[2]} | "
                f"Medicine: {sale[3]} | "
                f"Quantity: {sale[4]} | "
                f"Total: Rs. {sale[5]:.2f}"
            )

    conn.close()