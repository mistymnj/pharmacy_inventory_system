import sqlite3


def add_supplier(role):

    if role != "admin":
        print("Access Denied!")
        return

    supplier_name = input("Enter Supplier Name: ")
    phone = input("Enter Phone Number: ")
    address = input("Enter Address: ")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suppliers (supplier_name, phone, address)
        VALUES (?, ?, ?)
    """, (supplier_name, phone, address))

    conn.commit()
    conn.close()

    print("Supplier added successfully!")


def view_suppliers(role):

    if role not in ["admin", "user"]:
        print("Access Denied!")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT supplier_id, supplier_name, phone, address
        FROM suppliers
    """)

    suppliers = cursor.fetchall()

    print("\n===== SUPPLIER DETAILS =====")

    if suppliers:
        for supplier in suppliers:
            print("---------------------------")
            print("Supplier ID:", supplier[0])
            print("Supplier Name:", supplier[1])
            print("Phone:", supplier[2])
            print("Address:", supplier[3])
    else:
        print("No suppliers found.")

    conn.close()


def update_supplier(role):

    if role != "admin":
        print("Access Denied!")
        return

    supplier_id = input("Enter Supplier ID to update: ")
    supplier_name = input("Enter New Supplier Name: ")
    phone = input("Enter New Phone Number: ")
    address = input("Enter New Address: ")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE suppliers
        SET supplier_name = ?, phone = ?, address = ?
        WHERE supplier_id = ?
    """, (supplier_name, phone, address, supplier_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Supplier updated successfully!")
    else:
        print("Supplier ID not found.")

    conn.close()


def delete_supplier(role):

    if role != "admin":
        print("Access Denied!")
        return

    supplier_id = input("Enter Supplier ID to delete: ")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM suppliers
        WHERE supplier_id = ?
    """, (supplier_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Supplier deleted successfully!")
    else:
        print("Supplier ID not found.")

    conn.close()


def supplier_menu(role):

    while True:

        print("\n===== SUPPLIER MANAGEMENT =====")

        if role == "admin":
            print("1. Add Supplier")
            print("2. View Suppliers")
            print("3. Update Supplier")
            print("4. Delete Supplier")
            print("5. Back")

        elif role == "user":
            print("1. View Suppliers")
            print("2. Back")

        choice = input("Enter your choice: ")

        if role == "admin":

            if choice == "1":
                add_supplier(role)

            elif choice == "2":
                view_suppliers(role)

            elif choice == "3":
                update_supplier(role)

            elif choice == "4":
                delete_supplier(role)

            elif choice == "5":
                break

            else:
                print("Invalid choice!")

        elif role == "user":

            if choice == "1":
                view_suppliers(role)

            elif choice == "2":
                break

            else:
                print("Invalid choice!")