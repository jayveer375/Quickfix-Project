# 🌱 Provider Seeding Guide

This guide explains how to seed your database with 100 realistic dummy providers.

## 📋 What Gets Created

### Providers (100 total)
- **Random names** from Indian first and last names
- **Unique emails** (e.g., rajeshkumar1@gmail.com)
- **Phone numbers** in Indian format (+91XXXXXXXXXX)
- **Categories**: Plumber, Electrician, Cleaning, AC Repair, Painter, Carpenter
- **Cities**: Ahmedabad, Mumbai, Delhi, Bangalore
- **Areas**: 6 realistic areas per city
- **Price range**: ₹200 - ₹2000
- **Completed jobs**: 10-200 (random)
- **Status**: All approved and ready to use
- **Open/Close status**: 75% open, 25% closed

### Services (3-6 per provider)
Each provider gets realistic services based on their category:
- **Plumber**: Pipe repair, bathroom fitting, drain cleaning, etc.
- **Electrician**: Wiring, light fixtures, fan installation, etc.
- **Cleaning**: Deep cleaning, carpet cleaning, office cleaning, etc.
- **AC Repair**: Installation, gas refilling, servicing, etc.
- **Painter**: Interior/exterior painting, waterproofing, etc.
- **Carpenter**: Furniture repair, door installation, custom work, etc.

### Reviews & Ratings (5-20 per provider)
- **Rating**: Between 3 and 5 stars
- **Comments**: 20 realistic review templates
- **Timestamps**: Distributed over last 6 months
- **Users**: Uses existing users or generates random user IDs
- **Auto-calculated**: average_rating and total_reviews updated automatically

## 🚀 Usage Methods

### Method 1: Direct Python Script (Recommended)

```bash
python seed_providers.py
```

**Advantages:**
- Simple and straightforward
- No Flask app modifications needed
- Works immediately

### Method 2: Flask CLI Command

1. **Add to your app/__init__.py or app.py:**

```python
from seed_cli import register_seed_command

# After creating the app
app = create_app()
register_seed_command(app)
```

2. **Run the command:**

```bash
flask seed-providers
```

### Method 3: Flask Shell (Interactive)

```bash
flask shell
```

Then in the shell:

```python
from seed_providers import seed_providers
seed_providers()
```

## 📊 Expected Output

```
🌱 Starting provider seeding process...
============================================================
📊 Found 5 existing users for reviews
✅ Created 10/100 providers...
✅ Created 20/100 providers...
✅ Created 30/100 providers...
...
✅ Created 100/100 providers...
============================================================
✨ Successfully created 100 providers!
📍 Cities: Ahmedabad, Mumbai, Delhi, Bangalore
🔧 Categories: Plumber, Electrician, Cleaning, AC Repair, Painter, Carpenter
⭐ Each provider has 5-20 reviews with ratings 3-5
============================================================
🎉 Seeding completed successfully!
```

## ✅ Verification

After seeding, verify the data:

### Check Provider Count
```python
from app.models import QuickFix
print(f"Total providers: {QuickFix.query.count()}")
```

### Check Reviews
```python
from app.models import Review
print(f"Total reviews: {Review.query.count()}")
```

### Check by City
```python
from app.models import QuickFix
for city in ['Ahmedabad', 'Mumbai', 'Delhi', 'Bangalore']:
    count = QuickFix.query.filter_by(city=city).count()
    print(f"{city}: {count} providers")
```

### Check Average Ratings
```python
from app.models import QuickFix
providers = QuickFix.query.limit(5).all()
for p in providers:
    print(f"{p.business_name}: {p.average_rating:.1f} stars ({p.total_reviews} reviews)")
```

## 🔍 Features Tested

After seeding, these features should work perfectly:

1. **Search**: Search by name, category, city
2. **Filtering**: Filter by category, city, area
3. **Sorting**: 
   - By rating (high to low)
   - By reviews count
   - By name (A-Z)
4. **Rating Display**: Star ratings and review counts
5. **Provider Details**: All provider information populated
6. **Reviews Section**: Multiple reviews with ratings and comments

## ⚠️ Important Notes

### Safety Features
- ✅ Does NOT delete existing data
- ✅ Does NOT reset database
- ✅ Only INSERTS new providers
- ✅ Uses transactions (rolls back on error)
- ✅ Preserves existing users and providers

### Database Integrity
- All foreign keys properly maintained
- Categories created if they don't exist
- User accounts created for each provider
- Reviews linked to existing users when possible
- Rating stats automatically calculated

### Performance
- Creates 100 providers in ~10-30 seconds
- Generates 500-2000 reviews total
- Efficient batch operations
- Progress indicators every 10 providers

## 🧹 Cleanup (Optional)

If you want to remove seeded data:

### Using Flask CLI
```bash
flask clear-providers
```

### Manual Cleanup
```python
from app import db
from app.models import Review, Service, QuickFix, User

# Delete in correct order (foreign keys)
Review.query.delete()
Service.query.delete()
QuickFix.query.delete()
User.query.filter_by(role='provider').delete()
db.session.commit()
```

## 🐛 Troubleshooting

### Error: "No module named 'app'"
**Solution**: Run from project root directory where app/ folder exists

### Error: "Table doesn't exist"
**Solution**: Run migrations first:
```bash
flask db upgrade
```

### Error: "Duplicate email"
**Solution**: Script already ran. Check existing providers or clear first.

### Error: "Foreign key constraint"
**Solution**: Ensure categories table exists. Script creates them automatically.

## 📝 Customization

You can modify these variables in `seed_providers.py`:

```python
# Change number of providers
for i in range(1, 101):  # Change 101 to desired number + 1

# Change cities
CITIES = ['Ahmedabad', 'Mumbai', 'Delhi', 'Bangalore']

# Change categories
CATEGORIES = ['Plumber', 'Electrician', 'Cleaning', 'AC Repair', 'Painter', 'Carpenter']

# Change review count range
num_reviews = random.randint(5, 20)  # Modify min and max

# Change rating range
rating = random.randint(3, 5)  # Modify min and max
```

## 🎯 Next Steps

After seeding:

1. **Test Search**: Try searching for "plumber" or "electrician"
2. **Test Filters**: Filter by city or category
3. **Test Sorting**: Sort by rating or reviews
4. **Check Provider Pages**: View individual provider details
5. **Verify Reviews**: Check review display and calculations
6. **Test Responsiveness**: Check on mobile and desktop

## 📞 Support

If you encounter issues:
1. Check the error message carefully
2. Verify database migrations are up to date
3. Ensure Flask app is properly configured
4. Check database connection settings

---

**Happy Seeding! 🌱✨**
