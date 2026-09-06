from app.database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("DELETE FROM lost_items")
cursor.execute("DELETE FROM found_items")
cursor.execute("DELETE FROM investigation_cases")

connection.commit()
connection.close()

print("========================================")
print("LOSTIQ DEMO DATABASE RESET")
print("========================================")
print("Old test data removed.")
print("Database is ready for final demo.")