"""
Admin routes for managing the platform
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from app import db
from app.models import QuickFix, Category, User, Review, Service, City, Area
from app.routes import admin_bp

def admin_required(f):
    """Decorator to check if user is admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    total_users = User.query.count()
    total_providers = QuickFix.query.count()
    approved_providers = QuickFix.query.filter_by(status='approved').count()
    pending_providers = QuickFix.query.filter_by(status='pending').count()
    verified_providers = QuickFix.query.filter_by(is_verified=True).count()
    total_reviews = Review.query.count()
    total_services = Service.query.count()
    total_calls = db.session.query(db.func.sum(QuickFix.total_calls)).scalar() or 0
    
    # Get provider distribution by category
    categories = Category.query.all()
    category_data = []
    for category in categories:
        count = QuickFix.query.filter_by(category_id=category.id).count()
        if count > 0:  # Only include categories with providers
            category_data.append({
                'name': category.name,
                'count': count
            })
    
    stats = {
        'total_users': total_users,
        'total_providers': total_providers,
        'approved_providers': approved_providers,
        'pending_providers': pending_providers,
        'verified_providers': verified_providers,
        'total_reviews': total_reviews,
        'total_services': total_services,
        'total_calls': total_calls,
        'category_data': category_data
    }
    
    return render_template('admin_dashboard_saas.html', stats=stats)

@admin_bp.route('/approvals')
@login_required
@admin_required
def approvals():
    """View pending service provider approvals"""
    pending_providers = QuickFix.query.filter_by(status='pending').all()
    
    return render_template('admin_approvals.html', providers=pending_providers)

@admin_bp.route('/approve/<int:provider_id>', methods=['POST'])
@login_required
@admin_required
def approve(provider_id):
    """Approve a service provider"""
    provider = QuickFix.query.get_or_404(provider_id)
    provider.status = 'approved'
    db.session.commit()
    
    flash(f'{provider.business_name} has been approved', 'success')
    return redirect(url_for('admin.approvals'))

@admin_bp.route('/reject/<int:provider_id>', methods=['POST'])
@login_required
@admin_required
def reject(provider_id):
    """Reject a service provider"""
    provider = QuickFix.query.get_or_404(provider_id)
    provider.status = 'rejected'
    db.session.commit()
    
    flash(f'{provider.business_name} has been rejected', 'info')
    return redirect(url_for('admin.approvals'))

@admin_bp.route('/delete-provider/<int:provider_id>', methods=['POST'])
@login_required
@admin_required
def delete_provider(provider_id):
    """Delete a service provider"""
    provider = QuickFix.query.get_or_404(provider_id)
    business_name = provider.business_name
    
    # Get the referrer to redirect back to the correct page
    referrer = request.referrer
    
    db.session.delete(provider)
    db.session.commit()
    
    flash(f'{business_name} has been deleted', 'success')
    
    # Redirect back to the page where delete was triggered
    if referrer and 'providers' in referrer:
        return redirect(url_for('admin.providers'))
    else:
        return redirect(url_for('admin.approvals'))

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """Manage service categories"""
    categories = Category.query.all()
    return render_template('admin_categories.html', categories=categories)

@admin_bp.route('/add-category', methods=['POST'])
@login_required
@admin_required
def add_category():
    """Add a new category"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Category name is required', 'error')
        return redirect(url_for('admin.categories'))
    
    if Category.query.filter_by(name=name).first():
        flash('Category already exists', 'error')
        return redirect(url_for('admin.categories'))
    
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    
    flash('Category added successfully', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/delete-category/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)
    
    # Check if category has providers
    if category.providers:
        flash('Cannot delete category with existing providers', 'error')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/providers')
@login_required
@admin_required
def providers():
    """View all service providers"""
    providers = QuickFix.query.options(joinedload(QuickFix.user), joinedload(QuickFix.category)).all()
    return render_template('admin_providers.html', providers=providers)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """View all users"""
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/cities')
@login_required
@admin_required
def cities():
    """Manage cities and areas"""
    cities = City.query.order_by(City.name).all()
    return render_template('admin_cities.html', cities=cities)

@admin_bp.route('/add-city', methods=['POST'])
@login_required
@admin_required
def add_city():
    """Add a new city"""
    name = request.form.get('name', '').strip()
    state = request.form.get('state', '').strip()
    
    if not name:
        flash('City name is required', 'error')
        return redirect(url_for('admin.cities'))
    
    if City.query.filter_by(name=name).first():
        flash('City already exists', 'error')
        return redirect(url_for('admin.cities'))
    
    city = City(name=name, state=state)
    db.session.add(city)
    db.session.commit()
    
    flash(f'City "{name}" added successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/edit-city/<int:city_id>', methods=['POST'])
@login_required
@admin_required
def edit_city(city_id):
    """Edit a city"""
    city = City.query.get_or_404(city_id)
    name = request.form.get('name', '').strip()
    state = request.form.get('state', '').strip()
    
    if not name:
        flash('City name is required', 'error')
        return redirect(url_for('admin.cities'))
    
    # Check if another city with same name exists
    existing = City.query.filter(City.name == name, City.id != city_id).first()
    if existing:
        flash('Another city with this name already exists', 'error')
        return redirect(url_for('admin.cities'))
    
    city.name = name
    city.state = state
    db.session.commit()
    
    flash(f'City "{name}" updated successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/delete-city/<int:city_id>', methods=['POST'])
@login_required
@admin_required
def delete_city(city_id):
    """Delete a city"""
    city = City.query.get_or_404(city_id)
    city_name = city.name
    
    db.session.delete(city)
    db.session.commit()
    
    flash(f'City "{city_name}" and all its areas deleted successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/add-area', methods=['POST'])
@login_required
@admin_required
def add_area():
    """Add a new area to a city"""
    city_id = request.form.get('city_id', type=int)
    name = request.form.get('name', '').strip()
    pincode = request.form.get('pincode', '').strip()
    
    if not city_id or not name:
        flash('City and area name are required', 'error')
        return redirect(url_for('admin.cities'))
    
    city = City.query.get_or_404(city_id)
    
    # Check if area already exists in this city
    existing = Area.query.filter_by(name=name, city_id=city_id).first()
    if existing:
        flash(f'Area "{name}" already exists in {city.name}', 'error')
        return redirect(url_for('admin.cities'))
    
    area = Area(name=name, city_id=city_id, pincode=pincode)
    db.session.add(area)
    db.session.commit()
    
    flash(f'Area "{name}" added to {city.name} successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/edit-area/<int:area_id>', methods=['POST'])
@login_required
@admin_required
def edit_area(area_id):
    """Edit an area"""
    area = Area.query.get_or_404(area_id)
    name = request.form.get('name', '').strip()
    pincode = request.form.get('pincode', '').strip()
    
    if not name:
        flash('Area name is required', 'error')
        return redirect(url_for('admin.cities'))
    
    # Check if another area with same name exists in this city
    existing = Area.query.filter(Area.name == name, Area.city_id == area.city_id, Area.id != area_id).first()
    if existing:
        flash(f'Another area with name "{name}" already exists in this city', 'error')
        return redirect(url_for('admin.cities'))
    
    area.name = name
    area.pincode = pincode
    db.session.commit()
    
    flash(f'Area "{name}" updated successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/delete-area/<int:area_id>', methods=['POST'])
@login_required
@admin_required
def delete_area(area_id):
    """Delete an area"""
    area = Area.query.get_or_404(area_id)
    area_name = area.name
    
    db.session.delete(area)
    db.session.commit()
    
    flash(f'Area "{area_name}" deleted successfully', 'success')
    return redirect(url_for('admin.cities'))

@admin_bp.route('/api/cities', methods=['GET'])
def get_cities():
    """API endpoint to get all cities"""
    cities = City.query.order_by(City.name).all()
    return jsonify([{'id': city.id, 'name': city.name} for city in cities])

@admin_bp.route('/api/areas/<int:city_id>', methods=['GET'])
def get_areas(city_id):
    """API endpoint to get areas for a specific city"""
    areas = Area.query.filter_by(city_id=city_id).order_by(Area.name).all()
    return jsonify([{'id': area.id, 'name': area.name} for area in areas])
