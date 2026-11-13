import sqlite3
conn = sqlite3.connect("pharmacy.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    phone TEXT,
    address TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    category_id INTEGER,
    supplier_id INTEGER,
    unit_price REAL NOT NULL,
    description TEXT,

    FOREIGN KEY (category_id)
    REFERENCES categories(category_id),

    FOREIGN KEY (supplier_id)
    REFERENCES suppliers(supplier_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicine_batches (
    batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER NOT NULL,
    batch_number TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    manufacturing_date TEXT,
    expiry_date TEXT NOT NULL,
    purchase_date TEXT,

    FOREIGN KEY (medicine_id)
    REFERENCES medicines(medicine_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
    FOREIGN KEY (batch_id) REFERENCES medicine_batches(batch_id)
)
""")
conn.commit()
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table'
ORDER BY name
""")
tables = cursor.fetchall()
print("Pharmacy Database Created Successfully!")
print("\nTables Created:")
for table in tables:
    print(table[0])
cursor.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Antibiotics','Medicine for bacterial infections')
""")
cursor.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Painkillers','Medicine for pain releif')
""")
cursor.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Vitamins','Vitamin suppliments')
""")
cursor.execute("""
INSERT OR IGNORE INTO users(username,password,role)
VALUES(?,?,?)
""",("admin","Pharma@2026","admin"))
conn.commit()
cursor.execute("SELECT*FROM categories")
print("Category values:")
print(cursor.fetchall())
conn.close()
print("values inserted successfully") 