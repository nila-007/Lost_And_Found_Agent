from app.database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
INSERT INTO found_items
(item_name, category, description, location, found_date_time)
VALUES (?, ?, ?, ?, ?)
""", (
    "Black Wallet",
    "Wallet",
    "Black leather wallet with college ID",
    "Library",
    "2026-09-05 10:30"
))

cursor.execute("""
INSERT INTO found_items
(item_name, category, description, location, found_date_time)
VALUES (?, ?, ?, ?, ?)
""", (
    "Blue Water Bottle",
    "Bottle",
    "Blue steel water bottle",
    "Canteen",
    "2026-09-05 11:15"
))

connection.commit()
connection.close()

print("Test found items added!")