# Manage Cities & Areas Feature

## Overview
The "Manage Cities & Areas" feature allows administrators to manage geographical locations (cities and their areas) that can be used throughout the application for provider registration and user service searches.

## Features Implemented

### 1. Database Models
- **City Model**: Stores city information (name, state)
- **Area Model**: Stores area/locality information linked to cities (name, city_id, pincode)

### 2. Admin Dashboard Card
- Added a new card "Manage Cities & Areas" with a location icon (📍)
- Accessible from the admin dashboard at `/admin/dashboard`
- Matches the existing dashboard design (card layout, colors, spacing)

### 3. Cities & Areas Management Page
Location: `/admin/cities`

#### Features:
- **Add City**: Form to add new cities with name and optional state
- **View Cities**: List all cities with their areas count
- **Edit City**: Modal to edit city name and state
- **Delete City**: Remove city and all its areas (with confirmation)
- **Add Area**: Form to add areas under each city with name and optional pincode
- **View Areas**: Grid display of all areas under each city
- **Edit Area**: Modal to edit area name and pincode
- **Delete Area**: Remove individual areas (with confirmation)

### 4. API Endpoints
- `GET /admin/api/cities` - Get all cities (JSON)
- `GET /admin/api/areas/<city_id>` - Get areas for a specific city (JSON)

These endpoints can be used for dynamic dropdowns in registration forms.

### 5. Default Data
The migration script adds:
- **City**: Ahmedabad, Gujarat
- **Areas**: Maninagar, Bopal, Satellite, Vastrapur, Navrangpura, Paldi, Thaltej, Ghatlodia, Chandkheda, Naranpura

## Files Created/Modified

### New Files:
1. `app/templates/admin_cities.html` - Cities & Areas management page
2. `add_cities_areas_migration.py` - Migration script to create tables and add default data
3. `CITIES_AREAS_FEATURE.md` - This documentation file

### Modified Files:
1. `app/models.py` - Added City and Area models
2. `app/routes/admin.py` - Added routes for cities/areas management
3. `app/templates/admin_dashboard_saas.html` - Added "Manage Cities & Areas" card

## Usage Instructions

### For Administrators:

1. **Access the Feature**:
   - Login as admin
   - Go to Admin Dashboard
   - Click on "Manage Cities & Areas" card

2. **Add a New City**:
   - Enter city name (required)
   - Enter state (optional)
   - Click "Add City"

3. **Add Areas to a City**:
   - Click "Add Area" button on the city card
   - Enter area name (required)
   - Enter pincode (optional)
   - Click "Add"

4. **Edit City/Area**:
   - Click the "Edit" button
   - Modify the information in the modal
   - Click "Save Changes"

5. **Delete City/Area**:
   - Click the "Delete" button
   - Confirm the deletion
   - Note: Deleting a city removes all its areas

### For Developers:

#### Using Cities & Areas in Forms:

```html
<!-- City Dropdown -->
<select name="city" id="city" onchange="loadAreas(this.value)">
    <option value="">Select City</option>
    {% for city in cities %}
    <option value="{{ city.id }}">{{ city.name }}</option>
    {% endfor %}
</select>

<!-- Area Dropdown -->
<select name="area" id="area">
    <option value="">Select Area</option>
</select>

<script>
function loadAreas(cityId) {
    if (!cityId) {
        document.getElementById('area').innerHTML = '<option value="">Select Area</option>';
        return;
    }
    
    fetch(`/admin/api/areas/${cityId}`)
        .then(response => response.json())
        .then(areas => {
            let options = '<option value="">Select Area</option>';
            areas.forEach(area => {
                options += `<option value="${area.id}">${area.name}</option>`;
            });
            document.getElementById('area').innerHTML = options;
        });
}
</script>
```

#### Querying Cities & Areas:

```python
from app.models import City, Area

# Get all cities
cities = City.query.order_by(City.name).all()

# Get areas for a specific city
city = City.query.filter_by(name='Ahmedabad').first()
areas = city.areas.order_by(Area.name).all()

# Get a specific area
area = Area.query.filter_by(name='Maninagar', city_id=city.id).first()
```

## Security
- Only admin users can access this feature
- All routes are protected with `@admin_required` decorator
- Delete operations require confirmation
- Input validation on all forms

## UI/UX Features
- Responsive grid layout
- Color-coded buttons (Edit: Blue, Delete: Red, Add: Primary)
- Modal dialogs for editing
- Collapsible area forms
- Confirmation dialogs for deletions
- Success/error flash messages
- Icon-based visual hierarchy

## Future Enhancements (Optional)
1. Link cities/areas to provider profiles
2. Add city/area filters in search functionality
3. Show provider count per area
4. Import/export cities and areas (CSV)
5. Add coordinates (latitude/longitude) for mapping
6. Multi-language support for city/area names

## Testing
To test the feature:
1. Run the migration: `python add_cities_areas_migration.py`
2. Login as admin (admin@emergency.com / admin123)
3. Navigate to Admin Dashboard
4. Click "Manage Cities & Areas"
5. Try adding, editing, and deleting cities and areas

## Support
For issues or questions, refer to the main project documentation or contact the development team.
