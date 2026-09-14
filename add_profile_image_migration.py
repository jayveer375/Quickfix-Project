#!/usr/bin/env python3
"""
Database migration script to add profile_image column to users table
"""
import sqlite3
import os

def migrate_database():
    """Add profile_image column to users table"""
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("Database not found. Please run the application first to create the database.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_image' not in columns:
            # Add the profile_image column
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN profile_image VARCHAR(255) DEFAULT 'default.png'
            """)
            
            print("✅ Successfully added profile_image column to users table")
        else:
            print("ℹ️  profile_image column already exists in users table")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error migrating database: {e}")

if __name__ == "__main__":
    migrate_database()