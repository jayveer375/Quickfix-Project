# Integration Example: Using Cities & Areas in Forms

## Example: Provider Setup Form Integration

This example shows how to integrate the Cities & Areas feature into the provider setup form.

### Step 1: Update the Route (Backend)

```python
# In app/routes/provider.py

@provider_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """Setup service provider profile"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get cities for dropdown
    from app.models import City
    cities = City.query.order_by(City.name).all()
    
    if request.method == 'POST':
        # ... existing code ...
        city_id = request.form.get('city_id')
        area_id = request.form.get('area_id')
        
        # Get city and area names
        city = City.query.get(city_id)
        area = Area.query.get(area_id)
        
        # Use in provider profile
        provider.city = city.name if city else 'Ahmedabad'
        provider.address = f"{area.name}, {city.name}" if area and city else provider.address
        
        # ... rest of the code ...
    
    return render_template('provider_setup.html', cities=cities, ...)
```

### Step 2: Update the Template (Frontend)

```html
<!-- In app/templates/provider_setup.html -->

<div class="form-group">
    <label for="city">City *</label>
    <select name="city_id" id="city" class="form-control" required onchange="loadAreas(this.value)">
        <option value="">Select City</option>
        {% for city in cities %}
        <option value="{{ city.id }}" {% if provider and provider.city == city.name %}selected{% endif %}>
            {{ city.name }}{% if city.state %}, {{ city.state }}{% endif %}
        </option>
        {% endfor %}
    </select>
</div>

<div class="form-group">
    <label for="area">Area/Locality *</label>
    <select name="area_id" id="area" class="form-control" required>
        <option value="">Select City First</option>
    </select>
</div>

<script>
function loadAreas(cityId) {
    const areaSelect = document.getElementById('area');
    
    if (!cityId) {
        areaSelect.innerHTML = '<option value="">Select City First</option>';
        return;
    }
    
    // Show loading
    areaSelect.innerHTML = '<option value="">Loading areas...</option>';
    
    // Fetch areas for selected city
    fetch(`/admin/api/areas/${cityId}`)
        .then(response => response.json())
        .then(areas => {
            let options = '<option value="">Select Area</option>';
            areas.forEach(area => {
                options += `<option value="${area.id}">${area.name}</option>`;
            });
            areaSelect.innerHTML = options;
        })
        .catch(error => {
            console.error('Error loading areas:', error);
            areaSelect.innerHTML = '<option value="">Error loading areas</option>';
        });
}

// Load areas on page load if city is already selected
document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    if (citySelect.value) {
        loadAreas(citySelect.value);
    }
});
</script>
```

## Example: User Registration Form

```html
<!-- In app/templates/register_saas.html -->

<div class="form-group">
    <label for="city">City</label>
    <select name="city" id="city" class="form-control" onchange="loadUserAreas(this.value)">
        <option value="">Select City</option>
        {% for city in cities %}
        <option value="{{ city.name }}">{{ city.name }}</option>
        {% endfor %}
    </select>
</div>

<div class="form-group">
    <label for="area">Area</label>
    <select name="area" id="area" class="form-control">
        <option value="">Select City First</option>
    </select>
</div>

<script>
function loadUserAreas(cityName) {
    const areaSelect = document.getElementById('area');
    
    if (!cityName) {
        areaSelect.innerHTML = '<option value="">Select City First</option>';
        return;
    }
    
    // Find city ID by name
    fetch('/admin/api/cities')
        .then(response => response.json())
        .then(cities => {
            const city = cities.find(c => c.name === cityName);
            if (city) {
                return fetch(`/admin/api/areas/${city.id}`);
            }
        })
        .then(response => response.json())
        .then(areas => {
            let options = '<option value="">Select Area</option>';
            areas.forEach(area => {
                options += `<option value="${area.name}">${area.name}</option>`;
            });
            areaSelect.innerHTML = options;
        });
}
</script>
```

## Example: Search/Filter by Location

```python
# In app/routes/user.py

@user_bp.route('/search')
def search():
    """Search for service providers"""
    from app.models import City
    
    # Get filter parameters
    city_name = request.args.get('city')
    area_name = request.args.get('area')
    
    # Base query
    query = QuickFix.query.filter_by(status='approved')
    
    # Apply filters
    if city_name:
        query = query.filter_by(city=city_name)
    
    if area_name:
        query = query.filter(QuickFix.address.contains(area_name))
    
    providers = query.all()
    cities = City.query.order_by(City.name).all()
    
    return render_template('search.html', providers=providers, cities=cities)
```

```html
<!-- In search template -->
<div class="filters">
    <select name="city" onchange="this.form.submit()">
        <option value="">All Cities</option>
        {% for city in cities %}
        <option value="{{ city.name }}" {% if request.args.get('city') == city.name %}selected{% endif %}>
            {{ city.name }}
        </option>
        {% endfor %}
    </select>
    
    <select name="area" onchange="this.form.submit()">
        <option value="">All Areas</option>
        <!-- Dynamically loaded based on city -->
    </select>
</div>
```

## Tips for Integration

1. **Always validate on backend**: Don't trust client-side validation alone
2. **Handle missing data gracefully**: Provide defaults if city/area not selected
3. **Cache city data**: Cities don't change often, consider caching
4. **Use AJAX for better UX**: Load areas without page refresh
5. **Add loading states**: Show "Loading..." while fetching areas
6. **Error handling**: Handle API failures gracefully

## Common Patterns

### Pattern 1: Store IDs in Database
```python
# Store foreign keys
provider.city_id = city_id
provider.area_id = area_id
```

### Pattern 2: Store Names in Database (Current)
```python
# Store names directly (easier for display)
provider.city = city.name
provider.area = area.name
```

### Pattern 3: Hybrid Approach
```python
# Store both for flexibility
provider.city_id = city_id
provider.city_name = city.name
provider.area_id = area_id
provider.area_name = area.name
```

Choose based on your needs:
- IDs: Better for data integrity, requires joins
- Names: Easier to display, but harder to update if names change
- Hybrid: Best of both, but more storage

## Testing Checklist

- [ ] Cities dropdown loads correctly
- [ ] Areas load when city is selected
- [ ] Form validation works
- [ ] Data saves correctly to database
- [ ] Edit form pre-populates correctly
- [ ] Search/filter by location works
- [ ] Mobile responsive
- [ ] Error messages display properly
- [ ] Loading states work
- [ ] No console errors
