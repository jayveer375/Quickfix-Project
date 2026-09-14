"""
Script to add sample reviews for testing the rating system
Run this to populate the database with test reviews
"""
from app import create_app, db
from app.models import QuickFix, Review, User
from datetime import datetime, timedelta
import random

def add_sample_reviews():
    """Add sample reviews to test the rating system"""
    app = create_app()
    
    with app.app_context():
        print("Adding sample reviews...")
        
        # Get all providers
        providers = QuickFix.query.filter_by(status='approved').all()
        
        if not providers:
            print("No approved providers found. Please approve some providers first.")
            return
        
        # Get all users (excluding providers and admin)
        users = User.query.filter_by(role='user').all()
        
        if not users:
            print("No regular users found. Creating sample users...")
            # Create sample users
            sample_users = [
                {'name': 'John Doe', 'email': 'john@example.com', 'phone': '9876543210'},
                {'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '9876543211'},
                {'name': 'Mike Johnson', 'email': 'mike@example.com', 'phone': '9876543212'},
                {'name': 'Sarah Williams', 'email': 'sarah@example.com', 'phone': '9876543213'},
                {'name': 'David Brown', 'email': 'david@example.com', 'phone': '9876543214'},
            ]
            
            for user_data in sample_users:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    role='user'
                )
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
            users = User.query.filter_by(role='user').all()
            print(f"Created {len(users)} sample users")
        
        # Sample comments for different ratings
        comments_5_star = [
            "Excellent service! Highly professional and very responsive. Would definitely recommend!",
            "Outstanding work! They went above and beyond my expectations. Very satisfied!",
            "Best service provider I've ever worked with. Quick, efficient, and friendly!",
            "Amazing experience! Very knowledgeable and solved my problem quickly.",
            "Top-notch service! Professional, punctual, and reasonably priced."
        ]
        
        comments_4_star = [
            "Very good service. Professional and efficient. Minor delay but overall satisfied.",
            "Great work! Would have been 5 stars if they arrived a bit earlier.",
            "Good experience overall. Quality work and fair pricing.",
            "Satisfied with the service. Professional and knowledgeable.",
            "Good service provider. Would use again."
        ]
        
        comments_3_star = [
            "Decent service. Got the job done but nothing exceptional.",
            "Average experience. Service was okay but could be better.",
            "Fair service. Met basic expectations.",
            "Okay service. Room for improvement in communication.",
            "Acceptable work. Price was reasonable."
        ]
        
        comments_2_star = [
            "Service was below expectations. Had to follow up multiple times.",
            "Not very satisfied. Work quality could be better.",
            "Disappointing experience. Expected more professionalism.",
            "Below average service. Would not recommend.",
            "Not happy with the service. Many issues."
        ]
        
        comments_1_star = [
            "Very poor service. Would not recommend at all.",
            "Terrible experience. Unprofessional and unreliable.",
            "Worst service ever. Complete waste of time and money.",
            "Extremely disappointed. Did not deliver as promised.",
            "Awful service. Would give zero stars if possible."
        ]
        
        # Add reviews for each provider
        reviews_added = 0
        
        for provider in providers:
            # Random number of reviews (1 to min of 8 or available users)
            max_reviews = min(8, len(users))
            num_reviews = random.randint(1, max(1, max_reviews))
            
            # Select random users for this provider
            selected_users = random.sample(users, num_reviews)
            
            for i, user in enumerate(selected_users):
                # Check if user already reviewed this provider
                existing = Review.query.filter_by(
                    provider_id=provider.id,
                    user_id=user.id
                ).first()
                
                if existing:
                    continue
                
                # Generate rating with bias towards higher ratings (more realistic)
                rating_weights = [5, 15, 20, 35, 25]  # 1-5 stars
                rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
                
                # Select appropriate comment based on rating
                if rating == 5:
                    comment = random.choice(comments_5_star)
                elif rating == 4:
                    comment = random.choice(comments_4_star)
                elif rating == 3:
                    comment = random.choice(comments_3_star)
                elif rating == 2:
                    comment = random.choice(comments_2_star)
                else:
                    comment = random.choice(comments_1_star)
                
                # Create review with varied dates
                days_ago = random.randint(1, 60)
                created_at = datetime.utcnow() - timedelta(days=days_ago)
                
                review = Review(
                    provider_id=provider.id,
                    user_id=user.id,
                    rating=rating,
                    comment=comment,
                    created_at=created_at
                )
                
                db.session.add(review)
                reviews_added += 1
            
            # Update provider rating statistics
            db.session.commit()
            provider.update_rating_stats()
            
            print(f"  ✓ {provider.business_name}: {provider.total_reviews} reviews, avg rating: {provider.average_rating:.1f}")
        
        print(f"\n✓ Successfully added {reviews_added} sample reviews!")
        print("\nProvider Ratings Summary:")
        
        providers = QuickFix.query.order_by(QuickFix.average_rating.desc()).all()
        for provider in providers:
            stars = '⭐' * int(provider.average_rating)
            print(f"  {provider.business_name}: {stars} {provider.average_rating:.1f} ({provider.total_reviews} reviews)")

if __name__ == '__main__':
    add_sample_reviews()
