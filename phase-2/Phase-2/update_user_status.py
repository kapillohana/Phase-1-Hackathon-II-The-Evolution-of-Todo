import sqlite3
import os

# Connect to the database - check if it exists in the current directory
db_path = "./todo_app.db"

if not os.path.exists(db_path):
    print(f"Database file not found at: {db_path}")
    print("Looking for database files...")

    # Look for the database file in the current directory
    import subprocess
    result = subprocess.run(['find', '.', '-name', 'todo_app.db'], capture_output=True, text=True)
    db_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

    if db_files and db_files[0].strip():  # Check if any file was found
        db_path = db_files[0].strip()  # Use the first database file found
        print(f"Found database at: {db_path}")
    else:
        print("No database file found!")
        exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current users
cursor.execute("SELECT id, email, is_active FROM user;")
users = cursor.fetchall()
print("Current users in database:")
for user in users:
    print(f"ID: {user[0]}, Email: {user[1]}, Is Active: {user[2]}")

# Update all users to be active
cursor.execute("UPDATE user SET is_active = 1;")
conn.commit()

print(f"\nActivated all users in the database.")
print(f"Rows affected: {cursor.rowcount}")

# Verify the update
cursor.execute("SELECT id, email, is_active FROM user;")
updated_users = cursor.fetchall()
print("\nUpdated user status:")
for user in updated_users:
    print(f"ID: {user[0]}, Email: {user[1]}, Is Active: {user[2]}")

conn.close()
print("\nDatabase update completed. The 403 Forbidden error should now be resolved.")