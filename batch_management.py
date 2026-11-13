import sqlite3
from activity_log import log_activity


# ADD MEDICINE BATCH
def add_batch(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    print("\n===== ADD MEDICINE BATCH =====")

    medicine_id = input("Enter Medicine ID: ")
    batch_number = input("Enter Batch Number: ")
    quantity = input("Enter Quantity: ")
    manufacturing_date = input("Enter Manufacturing Date (YYYY-MM-DD): ")
    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
    purchase_date = input("Enter Purchase Date (YYYY-MM-DD): ")

    try:
        medicine_id = int(medicine_id)
        quantity = int(quantity)

        if quantity < 0:
            print("Quantity cannot be negative.")
            conn.close()
            return

        cursor.execute(
            "SELECT medicine_id FROM medicines WHERE medicine_id = ?",
            (medicine_id,)
        )

        medicine = cursor.fetchone()

        if medicine is None:
            print("Invalid Medicine ID!")
            conn.close()
            return

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

        print("Medicine Batch Added Successfully!")
        log_activity(
            "admin",
            role,
            "ADD BATCH",
            "Added batch:"+str(batch_number)+" for medicine ID:"+str(medicine_id)
        )

    except ValueError:
        print("Please enter valid numeric values.")

    except sqlite3.Error as error:
        print("Database Error:", error)

    finally:
        conn.close()


# VIEW MEDICINE BATCHES
def view_batches(role):

    if role not in ["admin", "user"]:
        print("Access Denied!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            medicine_batches.batch_id,
            medicines.medicine_name,
            medicine_batches.batch_number,
            medicine_batches.quantity,
            medicine_batches.manufacturing_date,
            medicine_batches.expiry_date,
            medicine_batches.purchase_date
        FROM medicine_batches
        JOIN medicines
        ON medicine_batches.medicine_id = medicines.medicine_id
    """)

    batches = cursor.fetchall()

    print("\n" + "=" * 115)
    print("                 MEDICINE BATCH DETAILS")
    print("=" * 115)
    if batches:
        print(
            f"{'BATCH ID':<10}"
            f"{'MEDICINE NAME':<22}"
            f"{'BATCH NUMBER':<18}"
            f"{'QUANTITY':<12}"
            f"{'MFG DATE':<15}"
            f"{'EXP DATE':<15}"
            f"{'PURCHASE DATE':<15}"
        )

        print("-" * 115)

        for batch in batches:
            print(
                f"{batch[0]:<10}"
                f"{str(batch[1]):<22}"
                f"{str(batch[2]):<18}"
                f"{batch[3]:<12}"
                f"{str(batch[4]):<15}"
                f"{str(batch[5]):<15}"
                f"{str(batch[6]):<15}"
            )
            print("=" * 115)
    else:
        print("No batches found.")
    conn.close()


# UPDATE BATCH QUANTITY
def update_batch_quantity(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    print("\n===== UPDATE BATCH QUANTITY =====")

    batch_id = input("Enter Batch ID: ")
    new_quantity = input("Enter New Quantity: ")

    try:
        batch_id = int(batch_id)
        new_quantity = int(new_quantity)

        if new_quantity < 0:
            print("Quantity cannot be negative.")
            conn.close()
            return

        cursor.execute("""
            UPDATE medicine_batches
            SET quantity = ?
            WHERE batch_id = ?
        """,(new_quantity, batch_id))
        if cursor.rowcount>0:
            conn.commit()
            print("Batch quantity updated sucessfully")
            log_activity(
                "admin",
                role,
                "UPDATE BATCH",
                "Updated batch ID: "+ str(batch_id)+
                "quantity to: "+ str(new_quantity)
    )
        else:
            print("Batch ID Not Found!")

    except ValueError:
        print("Please enter valid numeric values.")

    except sqlite3.Error as error:
        print("Database Error:", error)

    finally:
        conn.close()


# DELETE MEDICINE BATCH
def delete_batch(role):

    if role != "admin":
        print("Access Denied! Admin Only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    print("\n===== DELETE MEDICINE BATCH =====")

    batch_id = input("Enter Batch ID: ")

    try:
        batch_id = int(batch_id)

        cursor.execute("""
            DELETE FROM medicine_batches
            WHERE batch_id = ?
        """, (batch_id,))

        if cursor.rowcount > 0:
            conn.commit()
            print("Batch Deleted Successfully!")
        else:
            print("Batch ID Not Found!")

    except ValueError:
        print("Please enter a valid Batch ID.")

    except sqlite3.Error as error:
        print("Database Error:", error)

    finally:
        conn.close()


# BATCH MANAGEMENT MENU
def batch_menu(role):

    while True:

        print("\n===== BATCH MANAGEMENT =====")

        if role == "admin":
            print("1. Add Batch")
            print("2. View Batches")
            print("3. Update Batch Quantity")
            print("4. Delete Batch")
            print("5. Back")

        elif role == "user":
            print("1. View Batches")
            print("2. Back")

        choice = input("Enter your choice: ")

        if role == "admin":

            if choice == "1":
                add_batch(role)

            elif choice == "2":
                view_batches(role)

            elif choice == "3":
                update_batch_quantity(role)

            elif choice == "4":
                delete_batch(role)

            elif choice == "5":
                break

            else:
                print("Invalid Choice!")

        elif role == "user":

            if choice == "1":
                view_batches(role)

            elif choice == "2":
                break

            else:
                print("Invalid Choice!")