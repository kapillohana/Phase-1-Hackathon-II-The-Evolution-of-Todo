import sqlite3

# Connect to the database
db_path = "./todo_app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Database State Check ===")

# Check all users
cursor.execute("SELECT id, email, is_active, created_at, updated_at FROM user;")
users = cursor.fetchall()
print("\nUsers in database:")
for user in users:
    print(f"ID: {user[0]}, Email: {user[1]}, Is Active: {user[2]}, Created: {user[3]}, Updated: {user[4]}")

# Check all tasks
cursor.execute("SELECT id, user_id, title, completed, created_at FROM task LIMIT 10;")
tasks = cursor.fetchall()
print(f"\nSample of tasks in database (first 10):")
for task in tasks:
    print(f"Task ID: {task[0]}, User ID: {task[1]}, Title: {task[2][:30]}..., Completed: {task[3]}, Created: {task[4]}")

# Count tasks per user
cursor.execute("SELECT user_id, COUNT(*) as task_count FROM task GROUP BY user_id ORDER BY user_id;")
task_counts = cursor.fetchall()
print(f"\nTask counts per user:")
for user_id, count in task_counts:
    print(f"User ID: {user_id}, Task Count: {count}")

conn.close()
print("\nDatabase state check completed.")