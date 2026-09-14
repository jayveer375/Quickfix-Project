#!/usr/bin/env python3
"""
Test script to verify profile image display after login
"""
import requests
import sys

def test_login_profile_image():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing Profile Image Display After Login")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    try:
        # Test 1: Get login page
        print("1. Getting login page...")
        login_page = session.get(f"{base_url}/login")
        if login_page.status_code == 200:
            print("   ✅ Login page accessible")
        else:
            print(f"   ❌ Login page failed: {login_page.status_code}")
            return
        
        # Test 2: Login with User ID 6 (has profile image)
        print("2. Logging in as User ID 6 (jayveervora48@gmail.com)...")
        login_data = {
            'email': 'jayveervora48@gmail.com',
            'password': 'password123'  # Assuming this is the password
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code in [302, 303]:  # Redirect after successful login
            print("   ✅ Login successful (redirected)")
            redirect_url = login_response.headers.get('Location', '')
            print(f"   📍 Redirected to: {redirect_url}")
        else:
            print(f"   ❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text[:200]}...")
            return
        
        # Test 3: Access provider dashboard
        print("3. Accessing provider dashboard...")
        dashboard_response = session.get(f"{base_url}/provider/dashboard")
        
        if dashboard_response.status_code == 200:
            print("   ✅ Dashboard accessible")
            
            # Check if profile image URL is in the response
            dashboard_html = dashboard_response.text
            if '/static/uploads/user_6_kali-3d-black-1920x1080.png' in dashboard_html:
                print("   ✅ Profile image URL found in dashboard HTML")
                print("   🎉 SUCCESS: Profile image should display correctly!")
            else:
                print("   ❌ Profile image URL NOT found in dashboard HTML")
                if '/static/images/default-avatar.svg' in dashboard_html:
                    print("   ⚠️  Default avatar is being used instead")
                
                # Look for debug information
                if 'DEBUG INFO:' in dashboard_html:
                    debug_start = dashboard_html.find('DEBUG INFO:')
                    debug_end = dashboard_html.find('</div>', debug_start)
                    if debug_end > debug_start:
                        debug_info = dashboard_html[debug_start:debug_end]
                        print("   🔍 Debug info found:")
                        print(f"   {debug_info}")
        else:
            print(f"   ❌ Dashboard access failed: {dashboard_response.status_code}")
        
        # Test 4: Check if image file is accessible
        print("4. Testing direct image access...")
        image_response = session.get(f"{base_url}/static/uploads/user_6_kali-3d-black-1920x1080.png")
        
        if image_response.status_code == 200:
            print("   ✅ Profile image file is directly accessible")
            print(f"   📏 Image size: {len(image_response.content)} bytes")
        else:
            print(f"   ❌ Profile image file not accessible: {image_response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_login_profile_image()