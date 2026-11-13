import sqlite3
from activity_log import log_activity


def add_medicine(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    medicine_name = input("Enter Medicine Name: ")
    category_id = input("Enter Category ID: ")
    supplier_id = input("Enter Supplier ID: ")
    unit_price = input("Enter Unit Price: ")
    description = input("Enter Description: ")

    if not medicine_name or not unit_price:
        print("Medicine Name and Unit Price are required!")
        return

    try:
        unit_price = float(unit_price)

        if unit_price < 0:
            print("Price cannot be negative!")
            return

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO medicines
            (medicine_name, category_id, supplier_id,
             unit_price, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            medicine_name,
            category_id or None,
            supplier_id or None,
            unit_price,
            description
        ))

        conn.commit()

        print("Medicine Added Successfully!")
        log_activity(
            "admin",
            role,
            "ADMIN MEDICINE",
            "Added medicine:" +medicine_name
        )

    except sqlite3.Error as e:
        print("Database Error:", e)

    except ValueError:
        print("Please Enter a Valid Price!")

    finally:
        if 'conn' in locals():
            conn.close()


def view_medicines(role):

    if role not in ("admin", "user"):
        print("Access Denied!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            medicines.medicine_id,
            medicines.medicine_name,
            medicines.category_id,
            categories.category_name,
            medicines.supplier_id,
            medicines.unit_price,
            medicines.description
        FROM medicines
        LEFT JOIN categories
        ON medicines.category_id =
    categories.category_id
 """)

    medicines = cursor.fetchall()

    if medicines:
        print("\n" + "=" * 100)
        print("                              MEDICINE DETAILS")
        print("=" * 100)
        print(
            f"{'ID':<6}"
            f"{'MEDICINE NAME':<25}"
            f"{'CATEGORY ID':<15}"
            f"{'CATEGORY':<15}"
            f"{'SUPPLIER ID':<15}"
            f"{'PRICE':<12}"
            f"{'DESCRIPTION':<25}"
        )

        print("-" * 100)
 
        for medicine in medicines:
            description = str(medicine[6] or "")
            description = description[:25]

            print(
            f"{medicine[0]:<6}"
            f"{str(medicine[1]):<25}"
            f"{str(medicine[2]):<15}"
            f"{str(medicine[3] or ''):<15}"
            f"{str(medicine[4] or ''):<15}"
            f"{medicine[5]:<12.2f}"
            f"{description:<25}"
            )

        print("=" * 55)
    else:
        print("\nNo Medicines Found in the Database!")

    conn.close()


def update_medicine(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    medicine_id = input("Enter Medicine ID to Update: ")

    new_price = input("Enter New Unit Price: ")
    new_description = input("Enter New Description: ")

    try:
        new_price = float(new_price)

        if new_price < 0:
            print("Price cannot be negative!")
            return

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE medicines
            SET unit_price = ?,
                description = ?
            WHERE medicine_id = ?
        """, (new_price, new_description, medicine_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Medicine Updated Successfully!")
        else:
            print("Medicine ID Not Found!")

    except sqlite3.Error as e:
        print("Database Error:", e)

    except ValueError:
        print("Please Enter a Valid Price!")

    finally:
        if 'conn' in locals():
            conn.close()


def delete_medicine(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    medicine_id = input("Enter Medicine ID to Delete: ")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM medicines
        WHERE medicine_id = ?
    """, (medicine_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Medicine Deleted Successfully!")
    else:
        print("Medicine ID Not Found!")

    conn.close()