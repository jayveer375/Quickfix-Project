"""
Provider Statistics Dashboard
Usage: python provider_stats.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import QuickFix, Review, Service, Category
from sqlalchemy import func, desc

def show_statistics():
    """Display comprehensive provider statistics"""
    app = create_app('development')
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("📊 PROVIDER STATISTICS DASHBOARD")
        print("=" * 70)
        
        # Top rated providers
        print("\n🏆 TOP 10 HIGHEST RATED PROVIDERS:")
        print("-" * 70)
        top_providers = QuickFix.query.filter(
            QuickFix.total_reviews >= 5
        ).order_by(
            desc(QuickFix.average_rating),
            desc(QuickFix.total_reviews)
        ).limit(10).all()
        
        for idx, provider in enumerate(top_providers, 1):
            stars = "⭐" * int(provider.average_rating)
            print(f"{idx:2d}. {provider.business_name[:40]:<40} {stars} {provider.average_rating:.1f} ({provider.total_reviews} reviews)")
            print(f"    📍 {provider.city} | 🔧 {provider.category.name} | 📞 {provider.phone_number}")
        
        # Most reviewed providers
        print("\n💬 TOP 10 MOST REVIEWED PROVIDERS:")
        print("-" * 70)
        most_reviewed = QuickFix.query.order_by(
            desc(QuickFix.total_reviews)
        ).limit(10).all()
        
        for idx, provider in enumerate(most_reviewed, 1):
            print(f"{idx:2d}. {provider.business_name[:40]:<40} {provider.total_reviews} reviews (⭐ {provider.average_rating:.1f})")
            print(f"    📍 {provider.city} | 🔧 {provider.category.name}")
        
        # Category statistics
        print("\n🔧 CATEGORY STATISTICS:")
        print("-" * 70)
        category_stats = db.session.query(
            Category.name,
            func.count(QuickFix.id).label('count'),
            func.avg(QuickFix.average_rating).label('avg_rating'),
            func.sum(QuickFix.total_reviews).label('total_reviews')
        ).join(QuickFix).group_by(Category.name).order_by(desc('count')).all()
        
        print(f"{'Category':<20} {'Providers':<12} {'Avg Rating':<15} {'Total Reviews'}")
        for cat_name, count, avg_rating, total_rev in category_stats:
            avg_rating_val = avg_rating or 0
            total_rev_val = total_rev or 0
            print(f"{cat_name:<20} {count:<12} {avg_rating_val:>6.1f} ⭐      {total_rev_val:>6}")
        
        # City statistics
        print("\n📍 CITY STATISTICS:")
        print("-" * 70)
        city_stats = db.session.query(
            QuickFix.city,
            func.count(QuickFix.id).label('count'),
            func.avg(QuickFix.average_rating).label('avg_rating'),
            func.sum(QuickFix.total_reviews).label('total_reviews')
        ).group_by(QuickFix.city).order_by(desc('count')).all()
        
        print(f"{'City':<20} {'Providers':<12} {'Avg Rating':<15} {'Total Reviews'}")
        for city, count, avg_rating, total_rev in city_stats:
            avg_rating_val = avg_rating or 0
            total_rev_val = total_rev or 0
            print(f"{city:<20} {count:<12} {avg_rating_val:>6.1f} ⭐      {total_rev_val:>6}")
        
        # Service statistics
        print("\n🛠️  SERVICE STATISTICS:")
        print("-" * 70)
        total_services = Service.query.count()
        total_providers = QuickFix.query.count()
        
        service_stats = db.session.query(
            Service.category,
            func.count(Service.id).label('count')
        ).group_by(Service.category).order_by(desc('count')).all()
        
        print(f"Total Services: {total_services}")
        print(f"Average Services per Provider: {total_services/total_providers:.1f}")
        print(f"\nTop Service Categories:")
        for service_cat, count in service_stats[:10]:
            if service_cat:
                print(f"   {service_cat}: {count}")
        
        # Rating distribution
        print("\n⭐ RATING DISTRIBUTION:")
        print("-" * 70)
        rating_dist = db.session.query(
            Review.rating,
            func.count(Review.id).label('count')
        ).group_by(Review.rating).order_by(desc(Review.rating)).all()
        
        total_reviews = sum(count for _, count in rating_dist)
        for rating, count in rating_dist:
            percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"{rating} ⭐ {bar:<50} {count:>5} ({percentage:>5.1f}%)")
        
        # Provider status
        print("\n🏪 PROVIDER STATUS:")
        print("-" * 70)
        total = QuickFix.query.count()
        open_now = QuickFix.query.filter_by(is_open=True).count()
        closed_now = QuickFix.query.filter_by(is_open=False).count()
        verified = QuickFix.query.filter_by(is_verified=True).count()
        available = QuickFix.query.filter_by(is_available=True).count()
        
        print(f"Total Providers:     {total}")
        print(f"Open Now:            {open_now} ({open_now/total*100:.1f}%)")
        print(f"Closed Now:          {closed_now} ({closed_now/total*100:.1f}%)")
        print(f"Verified:            {verified} ({verified/total*100:.1f}%)")
        print(f"Available:           {available} ({available/total*100:.1f}%)")
        
        # Recent reviews
        print("\n💬 RECENT REVIEWS:")
        print("-" * 70)
        recent_reviews = Review.query.order_by(desc(Review.created_at)).limit(5).all()
        
        for review in recent_reviews:
            provider = QuickFix.query.get(review.provider_id)
            stars = "⭐" * review.rating
            print(f"{stars} {review.rating}/5 - {provider.business_name}")
            print(f"   \"{review.comment}\"")
            print(f"   {review.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
        
        print("=" * 70)
        print("✅ Statistics Generated Successfully!")
        print("=" * 70 + "\n")

if __name__ == '__main__':
    show_statistics()
