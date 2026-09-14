"""
Service provider routes for managing their profile and services
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import QuickFix, Service, Category, User
from app.routes import provider_bp
import os
from flask import current_app

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@provider_bp.route('/dashboard')
@login_required
def dashboard():
    """Service provider dashboard"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Refresh current_user data from database
    db.session.refresh(current_user)
    
    # Debug prints
    print(f"DEBUG: Dashboard - User ID: {current_user.id}")
    print(f"DEBUG: Dashboard - Profile Image: '{current_user.profile_image}'")
    print(f"DEBUG: Dashboard - Profile Image URL: {current_user.get_profile_image_url()}")
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider:
        flash('Please complete your profile first', 'info')
        return redirect(url_for('provider.setup'))
    
    services = Service.query.filter_by(provider_id=provider.id).all()
    reviews = provider.reviews
    categories = Category.query.all()
    
    return render_template('provider_dashboard.html',
                         provider=provider,
                         services=services,
                         reviews=reviews,
                         categories=categories)

@provider_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """Setup service provider profile"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    categories = Category.query.all()
    
    # Pre-fill data from user registration
    prefill_data = {
        'phone': current_user.phone,
        'city': current_user.city or 'Ahmedabad',
        'area': current_user.area or '',
        'service_type': current_user.service_type or ''
    }
    
    if request.method == 'POST':
        business_name = request.form.get('business_name', '').strip()
        category_id = request.form.get('category_id', type=int)
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        working_hours = request.form.get('working_hours', '').strip()
        description = request.form.get('description', '').strip()
        
        if not all([business_name, category_id, address, city, phone_number]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('provider.setup'))
        
        if len(phone_number.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')) < 10:
            flash('Phone number must be at least 10 digits', 'error')
            return redirect(url_for('provider.setup'))
        
        # Handle profile image upload
        profile_image_filename = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Validate file size (2MB max)
                    file.seek(0, 2)  # Seek to end
                    file_size = file.tell()
                    file.seek(0)  # Reset to beginning
                    
                    if file_size <= 2 * 1024 * 1024:  # 2MB
                        filename = secure_filename(f'user_{current_user.id}_{file.filename}')
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        
                        # Remove old profile image if exists
                        if current_user.profile_image and current_user.profile_image != 'default.png':
                            old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_image)
                            if os.path.exists(old_filepath):
                                os.remove(old_filepath)
                        
                        file.save(filepath)
                        profile_image_filename = filename
                    else:
                        flash('Profile image must be less than 2MB', 'error')
                        return redirect(url_for('provider.setup'))
                else:
                    flash('Invalid file type. Please upload JPG or PNG images only', 'error')
                    return redirect(url_for('provider.setup'))
        
        # Update user profile image if uploaded
        if profile_image_filename:
            current_user.profile_image = profile_image_filename
        
        if provider:
            provider.business_name = business_name
            provider.category_id = category_id
            provider.address = address
            provider.city = city
            provider.phone_number = phone_number
            provider.working_hours = working_hours
            provider.description = description
        else:
            provider = QuickFix(
                user_id=current_user.id,
                business_name=business_name,
                category_id=category_id,
                address=address,
                city=city,
                phone_number=phone_number,
                working_hours=working_hours,
                description=description
            )
            db.session.add(provider)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('provider.dashboard'))
    
    return render_template('provider_setup.html',
                         provider=provider,
                         categories=categories,
                         prefill_data=prefill_data)

@provider_bp.route('/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    """Add a new service"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider:
        flash('Please complete your profile first', 'info')
        return redirect(url_for('provider.setup'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        category = request.form.get('category', '').strip()
        
        if not name:
            flash('Service name is required', 'error')
            return redirect(url_for('provider.add_service'))
        
        if not category:
            flash('Service category is required', 'error')
            return redirect(url_for('provider.add_service'))
        
        service = Service(
            provider_id=provider.id,
            name=name,
            description=description,
            price=price,
            category=category
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully', 'success')
        return redirect(url_for('provider.dashboard'))
    
    return render_template('provider_add_service.html', provider=provider)

@provider_bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    """Upload service provider image"""
    from flask import jsonify
    
    if not current_user.is_provider():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider:
        return jsonify({'success': False, 'message': 'Please complete your profile first'})
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image selected'})
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No image selected'})
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file type. Allowed: png, jpg, jpeg, gif'})
    
    try:
        filename = secure_filename(f'provider_{provider.id}_{file.filename}')
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        provider.profile_image = f'/uploads/{filename}'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile image uploaded successfully', 'image_url': provider.profile_image})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to upload image'})

@provider_bp.route('/upload-service-image', methods=['POST'])
@login_required
def upload_service_image():
    """Upload service image"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider:
        flash('Please complete your profile first', 'info')
        return redirect(url_for('provider.setup'))
    
    if 'image' not in request.files:
        flash('No image selected', 'error')
        return redirect(url_for('provider.dashboard'))
    
    file = request.files['image']
    
    if file.filename == '':
        flash('No image selected', 'error')
        return redirect(url_for('provider.dashboard'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Allowed: png, jpg, jpeg, gif', 'error')
        return redirect(url_for('provider.dashboard'))
    
    filename = secure_filename(f'service_{provider.id}_{file.filename}')
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    provider.image_url = f'/uploads/{filename}'
    db.session.commit()
    
    flash('Service image uploaded successfully', 'success')
    return redirect(url_for('provider.dashboard'))

@provider_bp.route('/toggle-availability', methods=['POST'])
@login_required
def toggle_availability():
    """Toggle service open/close status"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if provider:
        provider.is_open = not provider.is_open
        db.session.commit()
        status = 'Open' if provider.is_open else 'Closed'
        flash(f'Your business is now {status}', 'success')
    
    return redirect(url_for('provider.dashboard'))

@provider_bp.route('/edit-service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    """Edit a service"""
    service = Service.query.get_or_404(service_id)
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider or service.provider_id != provider.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        service.name = request.form.get('name', '').strip()
        service.description = request.form.get('description', '').strip()
        service.price = request.form.get('price', '').strip()
        service.category = request.form.get('category', '').strip()
        
        if not service.name:
            flash('Service name is required', 'error')
            return render_template('provider_edit_service.html', service=service)
        
        if not service.category:
            flash('Service category is required', 'error')
            return render_template('provider_edit_service.html', service=service)
        
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('provider.dashboard'))
    
    return render_template('provider_edit_service.html', service=service)

@provider_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update service provider profile"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider:
        flash('Please complete your profile first', 'info')
        return redirect(url_for('provider.setup'))
    
    try:
        business_name = request.form.get('business_name', '').strip()
        category_id = request.form.get('category_id', type=int)
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        working_hours = request.form.get('working_hours', '').strip()
        description = request.form.get('description', '').strip()
        
        if not all([business_name, category_id, address, city, phone_number]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('provider.dashboard'))
        
        if len(phone_number.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')) < 10:
            flash('Phone number must be at least 10 digits', 'error')
            return redirect(url_for('provider.dashboard'))
        
        # Handle profile image upload if provided
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Validate file size (2MB max)
                    file.seek(0, 2)  # Seek to end
                    file_size = file.tell()
                    file.seek(0)  # Reset to beginning
                    
                    if file_size <= 2 * 1024 * 1024:  # 2MB
                        filename = secure_filename(f'user_{current_user.id}_{file.filename}')
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        
                        # Remove old profile image if exists
                        if current_user.profile_image and current_user.profile_image != 'default.png':
                            old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_image)
                            if os.path.exists(old_filepath):
                                os.remove(old_filepath)
                        
                        file.save(filepath)
                        current_user.profile_image = filename
                    else:
                        flash('Profile image must be less than 2MB', 'error')
                        return redirect(url_for('provider.dashboard'))
                else:
                    flash('Invalid file type. Please upload JPG or PNG images only', 'error')
                    return redirect(url_for('provider.dashboard'))
        
        provider.business_name = business_name
        provider.category_id = category_id
        provider.address = address
        provider.city = city
        provider.phone_number = phone_number
        provider.working_hours = working_hours
        provider.description = description
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Error updating profile. Please try again.', 'error')
    
    return redirect(url_for('provider.dashboard'))

@provider_bp.route('/delete-service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    """Delete a service"""
    service = Service.query.get_or_404(service_id)
    provider = QuickFix.query.filter_by(user_id=current_user.id).first()
    
    if not provider or service.provider_id != provider.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    db.session.delete(service)
    db.session.commit()
    
    flash('Service deleted successfully', 'success')
    return redirect(url_for('provider.dashboard'))