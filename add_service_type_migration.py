#!/usr/bin/env python
"""
Database migration script to add service_type column to users table
Run this script to update existing database with the new service_type field
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from sqlalchemy import text

def migrate_database():
    """Add service_type column to users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'service_type' not in columns:
                print("Adding service_type column to users table...")
                db.session.execute(text("ALTER TABLE users ADD COLUMN service_type VARCHAR(100)"))
                db.session.commit()
                print("✅ service_type column added successfully!")
            else:
                print("✅ service_type column already exists!")
                
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database()