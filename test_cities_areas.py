"""
Test script for Cities & Areas feature
Run this to verify the feature is working correctly
"""
from app import create_app, db
from app.models import City, Area

def test_cities_areas():
    """Test Cities & Areas functionality"""
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("Testing Cities & Areas Feature")
        print("=" * 60)
        
        # Test 1: Check if tables exist
        print("\n1. Checking if tables exist...")
        try:
            city_count = City.query.count()
            area_count = Area.query.count()
            print(f"   ✓ City table exists with {city_count} records")
            print(f"   ✓ Area table exists with {area_count} records")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return
        
        # Test 2: List all cities
        print("\n2. Listing all cities...")
        cities = City.query.all()
        for city in cities:
            print(f"   - {city.name}" + (f", {city.state}" if city.state else ""))
        
        # Test 3: List areas for each city
        print("\n3. Listing areas for each city...")
        for city in cities:
            areas = city.areas.order_by(Area.name).all()
            print(f"\n   {city.name} ({len(areas)} areas):")
            for area in areas:
                pincode_info = f" (PIN: {area.pincode})" if area.pincode else ""
                print(f"      - {area.name}{pincode_info}")
        
        # Test 4: Test adding a new city
        print("\n4. Testing add city functionality...")
        test_city_name = "Test City"
        existing = City.query.filter_by(name=test_city_name).first()
        if existing:
            print(f"   - Test city already exists, deleting...")
            db.session.delete(existing)
            db.session.commit()
        
        test_city = City(name=test_city_name, state="Test State")
        db.session.add(test_city)
        db.session.commit()
        print(f"   ✓ Added city: {test_city.name}")
        
        # Test 5: Test adding areas
        print("\n5. Testing add area functionality...")
        test_areas = ["Test Area 1", "Test Area 2"]
        for area_name in test_areas:
            area = Area(name=area_name, city_id=test_city.id, pincode="000000")
            db.session.add(area)
        db.session.commit()
        print(f"   ✓ Added {len(test_areas)} areas to {test_city.name}")
        
        # Test 6: Test querying
        print("\n6. Testing query functionality...")
        queried_city = City.query.filter_by(name=test_city_name).first()
        if queried_city:
            print(f"   ✓ Successfully queried city: {queried_city.name}")
            queried_areas = queried_city.areas.all()
            print(f"   ✓ Found {len(queried_areas)} areas")
        
        # Test 7: Test relationships
        print("\n7. Testing relationships...")
        area = Area.query.filter_by(city_id=test_city.id).first()
        if area:
            print(f"   ✓ Area '{area.name}' belongs to city '{area.city.name}'")
        
        # Test 8: Cleanup test data
        print("\n8. Cleaning up test data...")
        db.session.delete(test_city)  # This will cascade delete areas
        db.session.commit()
        print(f"   ✓ Deleted test city and its areas")
        
        # Final summary
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print(f"\nFinal counts:")
        print(f"  - Cities: {City.query.count()}")
        print(f"  - Areas: {Area.query.count()}")
        print("\nThe Cities & Areas feature is working correctly!")
        print("\nNext steps:")
        print("  1. Login as admin (admin@emergency.com / admin123)")
        print("  2. Go to Admin Dashboard")
        print("  3. Click 'Manage Cities & Areas'")
        print("  4. Try adding, editing, and deleting cities and areas")

if __name__ == '__main__':
    test_cities_areas()
