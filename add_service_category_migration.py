#!/usr/bin/env python3
"""
Database migration script to add category column to services table
Run this script to update existing database with the new category field
"""
import sqlite3
import os

def migrate_database():
    """Add category column to services table"""
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Please ensure the application has been run at least once.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if category column already exists
        cursor.execute("PRAGMA table_info(services)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'category' in columns:
            print("✅ Category column already exists in services table")
            conn.close()
            return True
        
        # Add category column
        print("🔄 Adding category column to services table...")
        cursor.execute("ALTER TABLE services ADD COLUMN category VARCHAR(100)")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("✅ Successfully added category column to services table")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting database migration...")
    success = migrate_database()
    
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")