"""
Flask CLI command for seeding providers
Add this to your Flask app to use: flask seed-providers
"""
import random
from datetime import datetime, timedelta
from app import db
from app.models import User, Category, QuickFix, Service, Review

# Import data from seed_providers
from seed_providers import (
    CATEGORIES, CITIES, AREAS, FIRST_NAMES, LAST_NAMES,
    REVIEW_COMMENTS, SERVICE_DESCRIPTIONS,
    generate_phone, generate_email, get_or_create_category,
    create_provider_user, create_provider_profile,
    create_services, create_reviews
)

def register_seed_command(app):
    """Register seed command with Flask CLI"""
    
    @app.cli.command('seed-providers')
    def seed_providers_command():
        """Seed 100 dummy providers with reviews"""
        print("🌱 Starting provider seeding process...")
        print("=" * 60)
        
        # Get existing user IDs for reviews
        existing_users = User.query.filter_by(role='user').all()
        existing_user_ids = [user.id for user in existing_users]
        print(f"📊 Found {len(existing_user_ids)} existing users for reviews")
        
        created_count = 0
        
        try:
            for i in range(1, 101):
                # Generate provider data
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                name = f"{first_name} {last_name}"
                email = generate_email(name, i)
                phone = generate_phone()
                city = random.choice(CITIES)
                area = random.choice(AREAS[city])
                category_name = random.choice(CATEGORIES)
                
                # Create category if not exists
                category = get_or_create_category(category_name)
                
                # Create user account
                user = create_provider_user(name, email, phone, city, area)
                
                # Create provider profile
                provider = create_provider_profile(user, category, city, area)
                
                # Create services
                create_services(provider, category_name)
                
                # Create reviews
                create_reviews(provider, existing_user_ids)
                
                # Update rating stats
                provider.update_rating_stats()
                
                created_count += 1
                
                if i % 10 == 0:
                    print(f"✅ Created {i}/100 providers...")
            
            db.session.commit()
            
            print("=" * 60)
            print(f"✨ Successfully created {created_count} providers!")
            print(f"📍 Cities: {', '.join(CITIES)}")
            print(f"🔧 Categories: {', '.join(CATEGORIES)}")
            print(f"⭐ Each provider has 5-20 reviews with ratings 3-5")
            print("=" * 60)
            print("🎉 Seeding completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during seeding: {str(e)}")
            import traceback
            traceback.print_exc()
    
    @app.cli.command('clear-providers')
    def clear_providers_command():
        """Clear all seeded providers (use with caution!)"""
        confirm = input("⚠️  Are you sure you want to delete ALL providers? (yes/no): ")
        if confirm.lower() == 'yes':
            try:
                # Delete in correct order due to foreign keys
                Review.query.delete()
                Service.query.delete()
                QuickFix.query.delete()
                User.query.filter_by(role='provider').delete()
                db.session.commit()
                print("✅ All providers cleared successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error: {str(e)}")
        else:
            print("❌ Operation cancelled")
