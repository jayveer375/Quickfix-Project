"""
Verification script to check seeded provider data
Usage: python verify_seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, QuickFix, Service, Review
from sqlalchemy import func

def verify_seeded_data():
    """Verify the seeded provider data"""
    app = create_app('development')
    
    with app.app_context():
        print("🔍 Verifying Seeded Data")
        print("=" * 60)
        
        # Count providers
        total_providers = QuickFix.query.count()
        print(f"\n📊 Total Providers: {total_providers}")
        
        # Count by status
        approved = QuickFix.query.filter_by(status='approved').count()
        print(f"✅ Approved: {approved}")
        
        # Count by city
        print(f"\n📍 Providers by City:")
        cities = db.session.query(
            QuickFix.city, 
            func.count(QuickFix.id)
        ).group_by(QuickFix.city).all()
        
        for city, count in cities:
            print(f"   {city}: {count}")
        
        # Count by category
        print(f"\n🔧 Providers by Category:")
        categories = db.session.query(
            Category.name,
            func.count(QuickFix.id)
        ).join(QuickFix).group_by(Category.name).all()
        
        for category, count in categories:
            print(f"   {category}: {count}")
        
        # Total reviews
        total_reviews = Review.query.count()
        print(f"\n⭐ Total Reviews: {total_reviews}")
        
        # Average reviews per provider
        if total_providers > 0:
            avg_reviews = total_reviews / total_providers
            print(f"📈 Average Reviews per Provider: {avg_reviews:.1f}")
        
        # Rating distribution
        print(f"\n⭐ Rating Distribution:")
        for rating in [5, 4, 3]:
            count = Review.query.filter_by(rating=rating).count()
            percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
            print(f"   {rating} stars: {count} ({percentage:.1f}%)")
        
        # Total services
        total_services = Service.query.count()
        print(f"\n🛠️  Total Services: {total_services}")
        if total_providers > 0:
            avg_services = total_services / total_providers
            print(f"📊 Average Services per Provider: {avg_services:.1f}")
        
        # Sample providers with ratings
        print(f"\n🌟 Sample Providers with Ratings:")
        sample_providers = QuickFix.query.order_by(
            QuickFix.average_rating.desc()
        ).limit(5).all()
        
        for provider in sample_providers:
            print(f"   {provider.business_name}")
            print(f"      Rating: {provider.average_rating:.1f} ⭐ ({provider.total_reviews} reviews)")
            print(f"      City: {provider.city} | Category: {provider.category.name}")
        
        # Open/Close status
        print(f"\n🏪 Provider Status:")
        open_count = QuickFix.query.filter_by(is_open=True).count()
        closed_count = QuickFix.query.filter_by(is_open=False).count()
        print(f"   Open: {open_count}")
        print(f"   Closed: {closed_count}")
        
        # Verified status
        verified_count = QuickFix.query.filter_by(is_verified=True).count()
        print(f"\n✓ Verified Providers: {verified_count}")
        
        print("\n" + "=" * 60)
        print("✅ Verification Complete!")
        
        # Check for data integrity issues
        print("\n🔍 Data Integrity Check:")
        issues = []
        
        # Check for providers without services
        providers_without_services = QuickFix.query.outerjoin(Service).filter(
            Service.id == None
        ).count()
        if providers_without_services > 0:
            issues.append(f"⚠️  {providers_without_services} providers have no services")
        
        # Check for providers without reviews
        providers_without_reviews = QuickFix.query.filter_by(total_reviews=0).count()
        if providers_without_reviews > 0:
            issues.append(f"⚠️  {providers_without_reviews} providers have no reviews")
        
        # Check for mismatched rating stats
        providers = QuickFix.query.all()
        mismatched = 0
        for provider in providers:
            actual_reviews = Review.query.filter_by(provider_id=provider.id).count()
            if actual_reviews != provider.total_reviews:
                mismatched += 1
        
        if mismatched > 0:
            issues.append(f"⚠️  {mismatched} providers have mismatched review counts")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print("   ✅ No issues found! All data is consistent.")
        
        print("\n" + "=" * 60)

if __name__ == '__main__':
    verify_seeded_data()
