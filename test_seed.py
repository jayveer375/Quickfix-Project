"""
Quick test script to verify seeding functionality
Usage: python test_seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from app import create_app, db
        from app.models import User, Category, QuickFix, Service, Review
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")
    try:
        from app import create_app, db
        app = create_app('development')
        with app.app_context():
            # Try a simple query
            from app.models import User
            count = User.query.count()
            print(f"✅ Database connected! Found {count} users.")
            return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_seed_functions():
    """Test if seed functions are available"""
    print("\n🧪 Testing seed functions...")
    try:
        from seed_providers import (
            generate_phone, generate_email, get_or_create_category,
            create_provider_user, create_provider_profile,
            create_services, create_reviews
        )
        print("✅ All seed functions available!")
        return True
    except ImportError as e:
        print(f"❌ Seed function import error: {e}")
        return False

def test_data_generation():
    """Test data generation functions"""
    print("\n🧪 Testing data generation...")
    try:
        from seed_providers import generate_phone, generate_email
        
        # Test phone generation
        phone = generate_phone()
        assert phone.startswith('+91'), "Phone should start with +91"
        assert len(phone) == 13, "Phone should be 13 characters (+91XXXXXXXXXX)"
        print(f"✅ Phone generation works: {phone}")
        
        # Test email generation
        email = generate_email("Test User", 1)
        assert '@' in email, "Email should contain @"
        assert email.endswith(('.com', '.in')), "Email should have valid domain"
        print(f"✅ Email generation works: {email}")
        
        return True
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

def test_models():
    """Test if models have required fields"""
    print("\n🧪 Testing model structure...")
    try:
        from app.models import QuickFix, Review
        
        # Check QuickFix model
        required_fields = ['average_rating', 'total_reviews', 'business_name', 'city']
        for field in required_fields:
            assert hasattr(QuickFix, field), f"QuickFix missing field: {field}"
        print("✅ QuickFix model has all required fields")
        
        # Check Review model
        required_fields = ['provider_id', 'user_id', 'rating', 'comment']
        for field in required_fields:
            assert hasattr(Review, field), f"Review missing field: {field}"
        print("✅ Review model has all required fields")
        
        return True
    except Exception as e:
        print(f"❌ Model structure error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 SEEDING FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_connection,
        test_seed_functions,
        test_data_generation,
        test_models
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n✅ ALL TESTS PASSED! Ready to seed providers.")
        print("\nRun: python seed_providers.py")
    else:
        print("\n❌ SOME TESTS FAILED! Please fix issues before seeding.")
        print("\nCommon issues:")
        print("  - Virtual environment not activated")
        print("  - Database not configured")
        print("  - Missing dependencies")
        print("  - Run 'flask db upgrade' to create tables")
    
    print("=" * 60)
    
    return all(results)

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
