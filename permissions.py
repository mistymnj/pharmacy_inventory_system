def check_permission(role, action):

    admin_permissions = [
        "add_medicine",
        "view_medicines",
        "update_medicine",
        "delete_medicine",
        "manage_suppliers",
        "manage_categories",
        "view_expiry_alerts",
        "view_low_stock_alerts"
    ]

    user_permissions = [
        "view_medicines",
        "view_expiry_alerts",
        "view_low_stock_alerts"
    ]

    if role == "admin":

        if action in admin_permissions:
            return True

    elif role == "user":

        if action in user_permissions:
            return True

    return False


def show_permissions(role):

    print("\n===== USER PERMISSIONS =====")

    if role == "admin":

        print("Role: Admin")
        print("Can Add Medicines")
        print("Can View Medicines")
        print("Can Update Medicines")
        print("Can Delete Medicines")
        print("Can Manage Suppliers")
        print("Can Manage Categories")
        print("Can View Expiry Alerts")
        print("Can View Low Stock Alerts")

    elif role == "user":

        print("Role: User")
        print("Can View Medicines")
        print("Can View Expiry Alerts")
        print("Can View Low Stock Alerts")