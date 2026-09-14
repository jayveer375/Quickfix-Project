#!/usr/bin/env python3
"""
Debug script to verify profile image data in database and file system
"""
import os
import sys
sys.path.append('.')

from app import create_app, db
from app.models import User

def debug_profile_images():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("🔍 PROFILE IMAGE DEBUG REPORT")
        print("=" * 60)
        
        # Check upload folder
        upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')
        print(f"\n📁 Upload Folder: {upload_folder}")
        print(f"📁 Upload Folder Exists: {os.path.exists(upload_folder)}")
        
        if os.path.exists(upload_folder):
            files = os.listdir(upload_folder)
            print(f"📁 Files in Upload Folder: {len(files)}")
            for file in files:
                file_path = os.path.join(upload_folder, file)
                file_size = os.path.getsize(file_path)
                print(f"   - {file} ({file_size} bytes)")
        
        print("\n" + "=" * 60)
        print("👥 USER PROFILE IMAGE DATA")
        print("=" * 60)
        
        users = User.query.all()
        for user in users:
            print(f"\n👤 User ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.name}")
            print(f"   Role: {user.role}")
            print(f"   Profile Image (DB): '{user.profile_image}'")
            
            if user.profile_image and user.profile_image != 'default.png':
                file_path = os.path.join(upload_folder, user.profile_image)
                file_exists = os.path.exists(file_path)
                print(f"   File Path: {file_path}")
                print(f"   File Exists: {'✅' if file_exists else '❌'} {file_exists}")
                if file_exists:
                    file_size = os.path.getsize(file_path)
                    print(f"   File Size: {file_size} bytes")
                else:
                    print("   ⚠️  FILE MISSING - This will cause display issues!")
            else:
                print("   Using default avatar")
            
            try:
                profile_url = user.get_profile_image_url()
                print(f"   Profile Image URL: {profile_url}")
            except Exception as e:
                print(f"   ❌ Error getting profile URL: {e}")
            
            print("-" * 50)
        
        print("\n" + "=" * 60)
        print("🔧 RECOMMENDATIONS")
        print("=" * 60)
        
        # Check for common issues
        issues_found = []
        
        if not os.path.exists(upload_folder):
            issues_found.append(f"❌ Upload folder '{upload_folder}' does not exist")
        
        for user in users:
            if user.profile_image and user.profile_image != 'default.png':
                file_path = os.path.join(upload_folder, user.profile_image)
                if not os.path.exists(file_path):
                    issues_found.append(f"❌ User {user.id} ({user.email}) has missing image file: {user.profile_image}")
        
        if issues_found:
            print("\n🚨 ISSUES FOUND:")
            for issue in issues_found:
                print(f"   {issue}")
            
            print("\n🔧 FIXES:")
            if not os.path.exists(upload_folder):
                print(f"   1. Create upload folder: mkdir -p {upload_folder}")
            print("   2. Re-upload missing profile images")
            print("   3. Or reset profile_image to 'default.png' for affected users")
        else:
            print("✅ No issues found! All profile images should display correctly.")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    debug_profile_images()