"""
Seed script to insert 100 dummy providers with realistic data
Usage: python seed_providers.py
"""
import os
import sys
import random
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, QuickFix, Service, Review

# Realistic data for seeding
CATEGORIES = [
    'Plumber', 'Electrician', 'Cleaning', 'AC Repair', 'Painter', 'Carpenter'
]

CITIES = ['Ahmedabad', 'Mumbai', 'Delhi', 'Bangalore']

AREAS = {
    'Ahmedabad': ['Satellite', 'Vastrapur', 'Maninagar', 'Navrangpura', 'Bodakdev', 'Ghatlodia'],
    'Mumbai': ['Andheri', 'Bandra', 'Powai', 'Juhu', 'Malad', 'Goregaon'],
    'Delhi': ['Connaught Place', 'Dwarka', 'Rohini', 'Saket', 'Karol Bagh', 'Lajpat Nagar'],
    'Bangalore': ['Koramangala', 'Whitefield', 'Indiranagar', 'HSR Layout', 'Marathahalli', 'Jayanagar']
}

FIRST_NAMES = [
    'Rajesh', 'Amit', 'Suresh', 'Vijay', 'Ramesh', 'Prakash', 'Mahesh', 'Dinesh',
    'Anil', 'Sanjay', 'Ravi', 'Manoj', 'Ashok', 'Deepak', 'Nitin', 'Rahul',
    'Kiran', 'Sachin', 'Vishal', 'Ajay', 'Sandeep', 'Pankaj', 'Yogesh', 'Pradeep'
]

LAST_NAMES = [
    'Kumar', 'Sharma', 'Patel', 'Singh', 'Verma', 'Gupta', 'Reddy', 'Rao',
    'Joshi', 'Mehta', 'Shah', 'Desai', 'Nair', 'Iyer', 'Pillai', 'Menon'
]

REVIEW_COMMENTS = [
    "Excellent service! Very professional and punctual.",
    "Great work! Highly recommended for quality service.",
    "Very satisfied with the service. Will hire again.",
    "Professional and efficient. Fixed the issue quickly.",
    "Good service at reasonable price. Happy with the work.",
    "Prompt response and quality work. Recommended!",
    "Skilled professional. Completed work on time.",
    "Very helpful and knowledgeable. Great experience.",
    "Quality service with attention to detail.",
    "Reliable and trustworthy. Will definitely call again.",
    "Fast and efficient service. Very pleased.",
    "Courteous and professional. Job well done!",
    "Excellent workmanship. Worth every penny.",
    "Very responsive and completed work as promised.",
    "Good experience overall. Would recommend to others.",
    "Professional approach and quality results.",
    "Timely service and fair pricing. Satisfied!",
    "Skilled technician with good work ethics.",
    "Impressed with the quality of work delivered.",
    "Friendly service and excellent results."
]

SERVICE_DESCRIPTIONS = {
    'Plumber': [
        'Pipe leak repair and replacement',
        'Bathroom fitting installation',
        'Kitchen sink repair',
        'Water heater installation',
        'Drain cleaning and unclogging',
        'Tap and faucet repair'
    ],
    'Electrician': [
        'Electrical wiring and rewiring',
        'Light fixture installation',
        'Fan installation and repair',
        'Switch and socket replacement',
        'Circuit breaker repair',
        'Electrical safety inspection'
    ],
    'Cleaning': [
        'Deep house cleaning',
        'Kitchen and bathroom cleaning',
        'Carpet and sofa cleaning',
        'Window and glass cleaning',
        'Post-construction cleaning',
        'Office cleaning services'
    ],
    'AC Repair': [
        'AC installation and uninstallation',
        'AC gas refilling',
        'AC servicing and maintenance',
        'AC repair and troubleshooting',
        'Split AC installation',
        'Window AC repair'
    ],
    'Painter': [
        'Interior wall painting',
        'Exterior wall painting',
        'Texture painting',
        'Waterproofing services',
        'Wood polishing',
        'Furniture painting'
    ],
    'Carpenter': [
        'Furniture repair and assembly',
        'Door and window installation',
        'Kitchen cabinet installation',
        'Wardrobe installation',
        'Bed and sofa repair',
        'Custom furniture making'
    ]
}

def generate_phone():
    """Generate random Indian phone number"""
    return f"+91{random.randint(7000000000, 9999999999)}"

def generate_email(name, index):
    """Generate unique email"""
    clean_name = name.lower().replace(' ', '')
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
    return f"{clean_name}{index}@{random.choice(domains)}"

def get_or_create_category(category_name):
    """Get or create category"""
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(
            name=category_name,
            description=f"Professional {category_name} services",
            emoji='🔧' if category_name in ['Plumber', 'Electrician'] else '🏠'
        )
        db.session.add(category)
        db.session.flush()
    return category

def create_provider_user(name, email, phone, city, area):
    """Create a user account for provider"""
    user = User(
        email=email,
        name=name,
        phone=phone,
        role='provider',
        city=city,
        area=area,
        gender=random.choice(['Male', 'Female']),
        profile_image='default.png'
    )
    user.set_password('password123')  # Default password
    db.session.add(user)
    db.session.flush()
    return user

def create_provider_profile(user, category, city, area):
    """Create provider profile"""
    category_name = category.name
    business_name = f"{user.name} {category_name} Services"
    
    provider = QuickFix(
        user_id=user.id,
        category_id=category.id,
        business_name=business_name,
        address=f"{random.randint(1, 999)}, {area}, {city}",
        city=city,
        phone_number=user.phone,
        description=f"Professional {category_name.lower()} with years of experience. Quality service guaranteed.",
        working_hours="Mon-Sat: 9:00 AM - 7:00 PM",
        is_available=True,
        is_open=random.choice([True, True, True, False]),  # 75% open
        status='approved',
        is_verified=random.choice([True, False]),
        latitude=random.uniform(12.0, 28.0),
        longitude=random.uniform(72.0, 88.0),
        total_calls=random.randint(10, 200)
    )
    db.session.add(provider)
    db.session.flush()
    return provider

def create_services(provider, category_name):
    """Create services for provider"""
    services_list = SERVICE_DESCRIPTIONS.get(category_name, [])
    num_services = random.randint(3, 6)
    selected_services = random.sample(services_list, min(num_services, len(services_list)))
    
    for service_name in selected_services:
        price = random.randint(200, 2000)
        service = Service(
            provider_id=provider.id,
            name=service_name,
            description=f"Professional {service_name.lower()} service",
            price=f"₹{price}",
            category=category_name,
            availability='available'
        )
        db.session.add(service)

def create_reviews(provider, existing_user_ids):
    """Create reviews for provider"""
    num_reviews = random.randint(5, 20)
    
    for _ in range(num_reviews):
        # Use existing user or create a random user_id
        if existing_user_ids and random.random() > 0.3:
            user_id = random.choice(existing_user_ids)
        else:
            user_id = random.randint(1, 1000)  # Random user ID
        
        rating = random.randint(3, 5)  # Rating between 3 and 5
        comment = random.choice(REVIEW_COMMENTS)
        
        # Random date within last 6 months
        days_ago = random.randint(1, 180)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        review = Review(
            provider_id=provider.id,
            user_id=user_id,
            rating=rating,
            comment=comment,
            created_at=created_at
        )
        db.session.add(review)

def seed_providers():
    """Main seeding function"""
    app = create_app('development')
    
    with app.app_context():
        print("🌱 Starting provider seeding process...")
        print("=" * 60)
        
        # Get existing user IDs for reviews
        existing_users = User.query.filter_by(role='user').all()
        existing_user_ids = [user.id for user in existing_users]
        print(f"📊 Found {len(existing_user_ids)} existing users for reviews")
        
        # Track created providers
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
                
                # Progress indicator
                if i % 10 == 0:
                    print(f"✅ Created {i}/100 providers...")
            
            # Commit all changes
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
            sys.exit(1)

if __name__ == '__main__':
    seed_providers()
