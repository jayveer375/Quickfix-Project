#!/usr/bin/env python3
"""
Check user password for testing
"""
import sys
sys.path.append('.')

from app import create_app, db
from app.models import User

def check_user_info():
    app = create_app()
    with app.app_context():
        user = User.query.get(6)
        if user:
            print(f"User ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Name: {user.name}")
            print(f"Role: {user.role}")
            print(f"Profile Image: {user.profile_image}")
            
            # Test common passwords
            test_passwords = ['password', 'password123', '123456', 'admin', 'test']
            for pwd in test_passwords:
                if user.check_password(pwd):
                    print(f"✅ Password found: '{pwd}'")
                    return pwd
            
            print("❌ None of the common passwords work")
            return None
        else:
            print("User ID 6 not found")
            return None

if __name__ == "__main__":
    check_user_info()