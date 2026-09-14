"""
Script to delete all reviews for specific service providers
"""
from app import create_app, db
from app.models import QuickFix, Review

def delete_provider_reviews():
    """Delete all reviews for providers named 'ali' and 'priyam'"""
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("Deleting Reviews for Specific Providers")
        print("=" * 60)
        
        # Find providers with business names containing 'ali' or 'priyam' (case insensitive)
        providers_to_clean = QuickFix.query.filter(
            db.or_(
                QuickFix.business_name.ilike('%ali%'),
                QuickFix.business_name.ilike('%priyam%')
            )
        ).all()
        
        if not providers_to_clean:
            print("No providers found with names containing 'ali' or 'priyam'")
            return
        
        total_reviews_deleted = 0
        
        for provider in providers_to_clean:
            print(f"\nProcessing provider: {provider.business_name}")
            
            # Get all reviews for this provider
            reviews = Review.query.filter_by(provider_id=provider.id).all()
            review_count = len(reviews)
            
            if review_count > 0:
                print(f"  Found {review_count} reviews to delete")
                
                # Delete all reviews for this provider
                for review in reviews:
                    db.session.delete(review)
                
                total_reviews_deleted += review_count
                print(f"  ✓ Deleted {review_count} reviews")
                
                # Update provider's rating statistics
                provider.average_rating = 0.0
                provider.total_reviews = 0
                print(f"  ✓ Reset rating statistics")
            else:
                print(f"  No reviews found for this provider")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("DELETION SUMMARY")
        print("=" * 60)
        print(f"Providers processed: {len(providers_to_clean)}")
        print(f"Total reviews deleted: {total_reviews_deleted}")
        print("✓ All changes committed to database")
        print("✓ Provider rating statistics updated")
        
        # Show remaining review counts
        print("\nVerification - Current review counts:")
        for provider in providers_to_clean:
            remaining_reviews = Review.query.filter_by(provider_id=provider.id).count()
            print(f"  {provider.business_name}: {remaining_reviews} reviews remaining")

if __name__ == '__main__':
    delete_provider_reviews()