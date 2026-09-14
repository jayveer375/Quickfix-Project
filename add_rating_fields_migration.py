"""
Migration script to add average_rating and total_reviews fields to QuickFix model
Run this script once to update the database schema
"""
from app import create_app, db
from app.models import QuickFix, Review

def migrate():
    """Add new rating fields and calculate initial values"""
    app = create_app()
    
    with app.app_context():
        print("Starting migration...")
        
        # Add columns if they don't exist
        try:
            # Try to access the columns - if they don't exist, we'll get an error
            db.session.execute(db.text('SELECT average_rating FROM service_providers LIMIT 1'))
            print("✓ average_rating column already exists")
        except Exception:
            print("Adding average_rating column...")
            db.session.execute(db.text('ALTER TABLE service_providers ADD COLUMN average_rating FLOAT DEFAULT 0.0'))
            db.session.commit()
            print("✓ average_rating column added")
        
        try:
            db.session.execute(db.text('SELECT total_reviews FROM service_providers LIMIT 1'))
            print("✓ total_reviews column already exists")
        except Exception:
            print("Adding total_reviews column...")
            db.session.execute(db.text('ALTER TABLE service_providers ADD COLUMN total_reviews INTEGER DEFAULT 0'))
            db.session.commit()
            print("✓ total_reviews column added")
        
        # Calculate and update rating statistics for all providers
        print("\nCalculating rating statistics for all providers...")
        providers = QuickFix.query.all()
        
        for provider in providers:
            reviews = Review.query.filter_by(provider_id=provider.id).all()
            
            if reviews:
                total_rating = sum(review.rating for review in reviews)
                provider.average_rating = total_rating / len(reviews)
                provider.total_reviews = len(reviews)
                print(f"  Provider '{provider.business_name}': {provider.total_reviews} reviews, avg rating: {provider.average_rating:.1f}")
            else:
                provider.average_rating = 0.0
                provider.total_reviews = 0
        
        db.session.commit()
        print("\n✓ Migration completed successfully!")
        print(f"Updated {len(providers)} providers")

if __name__ == '__main__':
    migrate()
