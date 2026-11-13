from register import register_user
from login import login_user
from reset_password import reset_password
from getpass import getpass
from permissions import show_permissions
from medicine_management import(
    add_medicine,
    view_medicines,
    update_medicine,
    delete_medicine
)
from batch_management import batch_menu
from expiry_alerts import view_expiry_alerts
from low_stock_alerts import view_low_stock_alerts
from stock_summary import view_stock_summary
from supplier_management import supplier_menu
from purchase_management import record_purchase
from purchase_history import view_purchase_history
from activity_log import view_activity_log
from billing_management import purchase_medicine, view_my_purchases, view_all_sales
from analytics_dashboard import analytics_dashboard
from inventory_report import export_inventory_report 
from expiry_notification import show_expiry_notifications
def medicine_menu(role, user_id):
    while True:
        print("\n===== MEDICINE MANAGEMENT =====")

        if role == "admin":
            show_expiry_notifications("admin")
            print("\n" +  "=" * 55)
            print("         PHARMACY INVENTORY MANAGEMENT SYSTEM")
            print("=" * 55)

            print("\n       ADMIN DASHBOARD")
            print("         Welcome,Admin!")
            print("-" * 55)

            print("   MEDICINE MANAGEMENT")
            print("   [1] Add Medicine")
            print("   [2] View Medicines")
            print("   [3] Update Medicine")
            print("   [4] Delete Medicine")

            print("\n   BATCH MANAGEMENT")
            print("   [5] Batch Management")

            print("\n   INVENTORY ALERTS")
            print("   [6] Expiry Alerts")
            print("   [7] Low Stock Alerts")

            print("\n   OTHER OPERATIONS")
            print("   [8] Stock Summary")
            print("   [9] Supplier Management")
            print("   [10] Purchase Management")
            print("   [11] Purchase History")
            print("   [12] Activity Log")
            print("   [13] View All Sales History")
            print("   [14] Analytics Dashboard")
            print("   [15] Export Inventory Report")
            print("   [16] Logout")

            print("-" * 55)
        elif role == "user":
            print("\n" + "=" * 55)
            print("           PHARMACY INVENTORY MANAGEMENT SYSTEM")
            print("=" * 55)

            print("\n        USER DASHBOARD")
            print("         Welcome User!")
            print("-" * 55)

            print("   INVENTORY") 
            print("   [1] View Medicines")
            print("   [2] Batch Management")

            print("\n  INVENTORY ALERTS")
            print("    [3] Expiry Alerts")
            print("    [4]Low Stock Alerts")

            print("\n  OTHER INFORMATION") 
            print("    [5] Stock Summary")
            print("    [6] Supplier Management")

            print("\n  PURCHASE")
            print("    [7] Purchase Medicine")
            print("    [8] View My Purchase")

            print("    [9] Logout")

            print("-" * 55)

        choice = input("Enter your choice: ")

        if role == "admin":
            if choice == "1":
                add_medicine(role)

            elif choice == "2":
                view_medicines(role)

            elif choice == "3":
                update_medicine(role)

            elif choice == "4":
                delete_medicine(role)

            elif choice == "5":
                batch_menu(role)

            elif choice == "6":
                view_expiry_alerts(role)

            elif choice == "7":
                view_low_stock_alerts(role)

            elif choice == "8":
                view_stock_summary(role)

            elif choice == "9":
                supplier_menu(role)

            elif choice == "10":
                record_purchase(role)

            elif choice == "11":
                view_purchase_history(role)

            elif choice == "12":
                view_activity_log(role)

            elif choice == "13":
                view_all_sales()

            elif choice == "14":
                analytics_dashboard(role)

            elif choice == "15":
                export_inventory_report(role)

            elif choice == "16":
                break

            else:
                print("Invalid choice!")

        elif role == "user":
            if choice == "1":
                view_medicines(role)

            elif choice == "2":
                batch_menu(role)

            elif choice == "3":
                view_expiry_alerts(role)

            elif choice == "4":
                view_low_stock_alerts(role)

            elif choice == "5":
                view_stock_summary(role)

            elif choice == "6":
                supplier_menu(role)

            elif choice == "7":
                purchase_medicine(user_id)

            elif choice == "8":
                view_my_purchases(user_id)

            elif choice == "9":
                break

            else:
                print("Invalid choice!")
def main():

    while True:

        print("\n")
        print("=" * 60)
        print("            PHARMACY INVENTORY MANAGEMENT SYSTEM")
        print("=" *60)

        print("\n")
        print("=" *60)

        print("   [1]   User Registration")
        print("   [2]   User Login")
        print("   [3]   Reset Password")
        print("   [4]   Exit")
        print("="*60)

        choice = input("     Enter Your Choice: ")

        if choice == "1":

            username = input("Enter Username: ")
            password = getpass("Enter Password: ")
            confirm_password = getpass("Confirm Password: ")


            register_user(
                username,
                password,
                confirm_password
            )

        elif choice == "2":

            username = input("Enter Username: ")
            password = getpass("Enter Password: ")

            login_result = login_user(username,password)
            if login_result:
                role,user_id=login_result

                show_permissions(role)
                medicine_menu(role,user_id)
        elif choice == "3":

            username = input("Enter Username: ")
            new_password = getpass("Enter New Password: ")
            confirm_password = getpass("Confirm New Password: ")

            reset_password(
                username,
                new_password,
                confirm_password
            )

        elif choice == "4":

            print("Exiting Pharmacy System...")
            break

        else:

            print("Invalid Choice! Please Try Again.")


if __name__ == "__main__":
    main()