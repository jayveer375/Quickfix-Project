#!/usr/bin/env python3
"""
Replace corrupted database with a fresh one and recreate admin account.
"""
import sys, os, shutil

src = 'instance/database.db'
bak = 'instance/database_corrupted_backup.db'
if os.path.exists(src):
    shutil.copy2(src, bak)
    os.remove(src)
    print(f"Corrupted DB backed up to {bak} and removed.")

sys.path.insert(0, '.')
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    from app.models import User
    admin = User.query.filter_by(email='admin@gmail.com').first()
    if admin:
        print("\n✅ Fresh database created successfully!")
        print("   Admin email   : admin@gmail.com")
        print("   Admin password: admin@123")
    else:
        print("Something went wrong - admin not created.")
