# Sort By Feature - Visual Guide

## Feature Location
The "Sort By" dropdown is located on the `/user/search` page, alongside the existing filters (Category, City, Area).

## UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Find Your Perfect Service Provider                         │
│  Browse through our verified providers...                   │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Category    │  City        │  Area        │  Sort By     │
│  ▼           │  ▼           │  ▼           │  ▼           │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ All          │ Ahmedabad    │ All Areas    │ Highest      │
│ Categories   │              │              │ Rating       │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

## Sort Options

When you click the "Sort By" dropdown, you'll see:

```
┌─────────────────────┐
│ Sort By             │
├─────────────────────┤
│ ✓ Highest Rating    │  ← Default
│   Most Reviews      │
│   Lowest Price      │
│   Highest Price     │
└─────────────────────┘
```

## Responsive Behavior

### Desktop (> 768px)
```
┌──────────┬──────────┬──────────┬──────────┐
│ Category │   City   │   Area   │ Sort By  │
└──────────┴──────────┴──────────┴──────────┘
```

### Tablet (≤ 768px)
```
┌──────────┬──────────┐
│ Category │   City   │
├──────────┼──────────┤
│   Area   │ Sort By  │
└──────────┴──────────┘
```

### Mobile (≤ 480px)
```
┌──────────────┐
│  Category    │
├──────────────┤
│    City      │
├──────────────┤
│    Area      │
├──────────────┤
│  Sort By     │
└──────────────┘
```

## How It Works

### 1. User Interaction
- User selects a sort option from the dropdown
- Page automatically refreshes with sorted results
- All other filters are preserved

### 2. URL Examples

**Sort by Highest Rating (default):**
```
/user/search?sort=rating
```

**Sort by Most Reviews:**
```
/user/search?sort=reviews
```

**Sort by Lowest Price:**
```
/user/search?sort=low_price
```

**Sort by Highest Price:**
```
/user/search?sort=high_price
```

**Combined with other filters:**
```
/user/search?category=1&area=Maninagar&sort=low_price
```

## Sorting Logic

### Highest Rating
- Primary: Average rating (highest first)
- Secondary: Total reviews (most first)
- Shows providers with best ratings at the top

### Most Reviews
- Primary: Total reviews (most first)
- Secondary: Average rating (highest first)
- Shows most reviewed providers at the top

### Lowest Price
- Extracts minimum price from each provider's services
- Sorts ascending (cheapest first)
- Providers without prices appear at the end

### Highest Price
- Extracts minimum price from each provider's services
- Sorts descending (most expensive first)
- Providers without prices appear at the end

## Visual Indicators

Each provider card shows:
```
┌─────────────────────────────────────┐
│  [Profile Image]                    │
│  🏥 Provider Name                   │
│  📍 Location                        │
│  ⭐⭐⭐⭐⭐ 4.5 (23 reviews)        │
│  💰 Services: Service 1, Service 2 │
│  [View Profile] [Call] [WhatsApp]  │
└─────────────────────────────────────┘
```

## User Benefits

1. **Quick Comparison**: Easily find top-rated providers
2. **Budget-Friendly**: Sort by price to find affordable options
3. **Popular Choices**: See most reviewed providers
4. **Premium Services**: Find high-end providers with highest prices

## Technical Notes

- No page reload required (uses GET parameters)
- Maintains all active filters
- Works on all devices
- Fast database queries for rating/reviews
- Python sorting for price (due to Service model structure)
