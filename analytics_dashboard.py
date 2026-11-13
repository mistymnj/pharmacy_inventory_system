import sqlite3
from datetime import date, timedelta


def analytics_dashboard(role):

    if role != "admin":
        print("Access denied! Admin only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    print("\n" + "=" * 60)
    print("       PHARMACY ANALYTICS DASHBOARD")
    print("=" * 60)

    # Total Medicines
    cursor.execute("SELECT COUNT(*) FROM medicines")
    total_medicines = cursor.fetchone()[0]

    # Total Stock Quantity
    cursor.execute("SELECT SUM(quantity) FROM medicine_batches")
    total_stock = cursor.fetchone()[0] or 0

    # Total Revenue
    cursor.execute("SELECT SUM(total_amount) FROM sales")
    total_revenue = cursor.fetchone()[0] or 0

    # Total Sales
    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]

    # Expired Medicines
    cursor.execute("""
        SELECT COUNT(*)
        FROM medicine_batches
        WHERE expiry_date < ?
        AND quantity > 0
    """, (date.today().isoformat(),))

    expired_batches = cursor.fetchone()[0]

    # Medicines Expiring Within 30 Days
    future_date = (date.today() + timedelta(days=30)).isoformat()

    cursor.execute("""
        SELECT COUNT(*)
        FROM medicine_batches
        WHERE expiry_date BETWEEN ? AND ?
        AND quantity > 0
    """, (date.today().isoformat(), future_date))

    expiring_batches = cursor.fetchone()[0]

    # Best Selling Medicines
    cursor.execute("""
        SELECT medicines.medicine_name,
               SUM(sale_items.quantity) AS total_sold
        FROM sale_items
        JOIN medicines
        ON sale_items.medicine_id = medicines.medicine_id
        GROUP BY medicines.medicine_id
        ORDER BY total_sold DESC
        LIMIT 5
    """)

    best_selling = cursor.fetchall()

    print("\nTOTAL MEDICINES :", total_medicines)
    print("TOTAL STOCK     :", total_stock)
    print("TOTAL SALES     :", total_sales)
    print("TOTAL REVENUE   : Rs.", round(total_revenue, 2))
    print("EXPIRED BATCHES :", expired_batches)
    print("EXPIRING IN 30 DAYS :", expiring_batches)

    print("\n----- TOP 5 BEST SELLING MEDICINES -----")

    if best_selling:
        for medicine in best_selling:
            print(medicine[0], "-", medicine[1], "units sold")
    else:
        print("No sales records available.")

    print("\n" + "=" * 60)

    conn.close()