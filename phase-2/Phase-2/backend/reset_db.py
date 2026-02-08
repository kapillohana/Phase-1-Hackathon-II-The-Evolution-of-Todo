#!/usr/bin/env python3
"""
Database reset script for the Advanced Todo Application
This script will recreate the database with the correct schema
"""
import os
import sqlite3
from datetime import datetime

def reset_database():
    """Reset the database to ensure correct schema with proper defaults"""
    db_path = "todo_app.db"
    
    # Remove existing database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Connect to create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table with correct schema
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0,
            priority VARCHAR(20) NOT NULL DEFAULT 'medium',
            tags TEXT,
            due_date DATETIME,
            recurring VARCHAR(20) NOT NULL DEFAULT 'none',
            completed_at DATETIME,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database recreated with correct schema!")
    print("The is_active column now has DEFAULT 1 (True)")
    print("Please restart your backend server to pick up the new database.")

if __name__ == "__main__":
    reset_database()