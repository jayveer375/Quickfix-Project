"""
Script to delete all reviews from all service providers
"""
from app import create_app, db
from app.models import QuickFix, Review

def delete_all_reviews():
    """Delete all reviews from all service providers"""
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("Deleting ALL Reviews from ALL Providers")
        print("=" * 60)
        
        # Get all providers
        all_providers = QuickFix.query.all()
        
        if not all_providers:
            print("No providers found in database")
            return
        
        print(f"Found {len(all_providers)} providers")
        
        # Get total review count before deletion
        total_reviews_before = Review.query.count()
        print(f"Total reviews in database: {total_reviews_before}")
        
        if total_reviews_before == 0:
            print("No reviews to delete")
            return
        
        print("\nProcessing providers:")
        
        providers_with_reviews = 0
        total_reviews_deleted = 0
        
        for provider in all_providers:
            # Get review count for this provider
            review_count = Review.query.filter_by(provider_id=provider.id).count()
            
            if review_count > 0:
                providers_with_reviews += 1
                print(f"  {provider.business_name}: {review_count} reviews")
                
                # Delete all reviews for this provider
                Review.query.filter_by(provider_id=provider.id).delete()
                total_reviews_deleted += review_count
                
                # Reset provider's rating statistics
                provider.average_rating = 0.0
                provider.total_reviews = 0
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("DELETION SUMMARY")
        print("=" * 60)
        print(f"Total providers: {len(all_providers)}")
        print(f"Providers with reviews: {providers_with_reviews}")
        print(f"Total reviews deleted: {total_reviews_deleted}")
        print("✓ All reviews deleted from database")
        print("✓ All provider rating statistics reset")
        
        # Verify deletion
        remaining_reviews = Review.query.count()
        print(f"\nVerification:")
        print(f"  Reviews remaining in database: {remaining_reviews}")
        
        if remaining_reviews == 0:
            print("  ✓ All reviews successfully deleted!")
        else:
            print(f"  ⚠️ Warning: {remaining_reviews} reviews still remain")

if __name__ == '__main__':
    delete_all_reviews()