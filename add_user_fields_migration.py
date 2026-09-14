#!/usr/bin/env python3
"""
Migration script to add gender, area, and city fields to User model
"""
import sqlite3
import os

def add_user_fields():
    """Add gender, area, and city fields to users table"""
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add gender column if it doesn't exist
        if 'gender' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN gender VARCHAR(20)')
            print("Added 'gender' column to users table")
        else:
            print("'gender' column already exists")
        
        # Add area column if it doesn't exist
        if 'area' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN area VARCHAR(100)')
            print("Added 'area' column to users table")
        else:
            print("'area' column already exists")
        
        # Add city column if it doesn't exist
        if 'city' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN city VARCHAR(100) DEFAULT "Ahmedabad"')
            print("Added 'city' column to users table")
            
            # Update existing users to have default city
            cursor.execute('UPDATE users SET city = "Ahmedabad" WHERE city IS NULL')
            print("Updated existing users with default city 'Ahmedabad'")
        else:
            print("'city' column already exists")
        
        conn.commit()
        print("Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    add_user_fields()