# 🚀 Quick Seed Reference Card

## One-Line Commands

### Seed 100 Providers
```bash
python seed_providers.py
```

### Verify Seeded Data
```bash
python verify_seed.py
```

### View Statistics Dashboard
```bash
python provider_stats.py
```

### Flask CLI (if configured)
```bash
flask seed-providers
```

## What You Get

| Item | Count | Details |
|------|-------|---------|
| **Providers** | 100 | Across 4 cities, 6 categories |
| **Reviews** | 500-2000 | 5-20 per provider, ratings 3-5 ⭐ |
| **Services** | 300-600 | 3-6 per provider |
| **Cities** | 4 | Ahmedabad, Mumbai, Delhi, Bangalore |
| **Categories** | 6 | Plumber, Electrician, Cleaning, AC Repair, Painter, Carpenter |

## Quick Checks

### Count Providers
```python
from app.models import QuickFix
print(QuickFix.query.count())
```

### Count Reviews
```python
from app.models import Review
print(Review.query.count())
```

### Top Rated Providers
```python
from app.models import QuickFix
providers = QuickFix.query.order_by(QuickFix.average_rating.desc()).limit(5).all()
for p in providers:
    print(f"{p.business_name}: {p.average_rating:.1f}⭐ ({p.total_reviews} reviews)")
```

### Providers by City
```python
from app.models import QuickFix
for city in ['Ahmedabad', 'Mumbai', 'Delhi', 'Bangalore']:
    count = QuickFix.query.filter_by(city=city).count()
    print(f"{city}: {count}")
```

## Features to Test After Seeding

- ✅ Search by name, category, city
- ✅ Filter by category and location
- ✅ Sort by rating (high to low)
- ✅ Sort by review count
- ✅ View provider details
- ✅ Display ratings and reviews
- ✅ Open/Close status indicators

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'app'" | Run from project root directory |
| "Table doesn't exist" | Run `flask db upgrade` first |
| "Duplicate email" | Script already ran successfully |
| Import errors | Check virtual environment is activated |

## Safety Notes

- ✅ Does NOT delete existing data
- ✅ Does NOT reset database
- ✅ Only INSERTS new providers
- ✅ Safe to run multiple times (will create more providers)
- ✅ Uses database transactions (rolls back on error)

## File Structure

```
project/
├── seed_providers.py          # Main seeding script ⭐
├── verify_seed.py             # Verification script
├── provider_stats.py          # Statistics dashboard
├── seed_cli.py                # Flask CLI commands
├── SEEDING_GUIDE.md           # Detailed documentation
└── QUICK_SEED_REFERENCE.md    # This file
```

## Need Help?

1. Read `SEEDING_GUIDE.md` for detailed instructions
2. Run `python verify_seed.py` to check data integrity
3. Run `python provider_stats.py` to see statistics
4. Check error messages carefully

---

**Quick Start**: Just run `python seed_providers.py` and you're done! 🎉
