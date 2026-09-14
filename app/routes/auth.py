"""
Authentication routes for login and registration
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.routes import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('auth.login'))
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Force refresh user data before login
            db.session.refresh(user)
            
            # Debug print
            print(f"DEBUG: Logging in user {user.id}, profile_image: '{user.profile_image}'")
            
            login_user(user, remember=request.form.get('remember'))
            
            # Redirect based on role
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_provider():
                return redirect(url_for('provider.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login_saas.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    from app.models import City, Area
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Get cities for dropdown
    cities = City.query.order_by(City.name).all()
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        gender = request.form.get('gender', '').strip()
        area = request.form.get('area', '').strip()
        city = request.form.get('city', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'user')  # 'user' or 'provider'
        service_type = request.form.get('service_type', '').strip() if role == 'provider' else None
        
        # Validate input
        if not all([email, name, phone, password, confirm_password]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('auth.register'))
        
        # Validate service type for providers
        if role == 'provider' and not service_type:
            flash('Service type is required for provider accounts', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            email=email,
            name=name,
            phone=phone,
            gender=gender,
            area=area if role == 'provider' else None,
            city=city if role == 'provider' else None,
            role=role,
            service_type=service_type
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        if role == 'provider':
            flash(f'Provider account created successfully! Service: {service_type}', 'success')
        else:
            flash('User account created successfully!', 'success')
        
        return redirect(url_for('auth.login'))
    
    return render_template('register_saas.html', cities=cities)

@auth_bp.route('/register-provider', methods=['GET', 'POST'])
def register_provider():
    """Provider registration route"""
    from app.models import City, Area
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Get cities for dropdown
    cities = City.query.order_by(City.name).all()
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        gender = request.form.get('gender', '').strip()
        area = request.form.get('area', '').strip()
        city = request.form.get('city', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = 'provider'  # Always provider for this route
        service_type = request.form.get('service_type', '').strip()
        
        # Validate input
        if not all([email, name, phone, password, confirm_password]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('auth.register_provider'))
        
        # Validate service type for providers
        if not service_type:
            flash('Service type is required for provider accounts', 'error')
            return redirect(url_for('auth.register_provider'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register_provider'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.register_provider'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register_provider'))
        
        # Create new provider user
        user = User(
            email=email,
            name=name,
            phone=phone,
            gender=gender,
            area=area,
            city=city,
            role=role,
            service_type=service_type
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Provider account created successfully! Service: {service_type}', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register_saas(1).html', cities=cities)

@auth_bp.route('/register-user', methods=['GET', 'POST'])
def register_user():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        gender = request.form.get('gender', '').strip()
        area = request.form.get('area', '').strip()
        city = request.form.get('city', 'Ahmedabad').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = 'user'  # Always user for this route
        
        # Validate input
        if not all([email, name, phone, password, confirm_password]):
            flash('All required fields must be filled', 'error')
            return redirect(url_for('auth.register_user'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register_user'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.register_user'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register_user'))
        
        # Create new user
        user = User(
            email=email,
            name=name,
            phone=phone,
            gender=gender,
            area=None,  # Users don't need area
            city=None,  # Users don't need city
            role=role,
            service_type=None  # Users don't have service types
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('User account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register_saas(2).html')

@auth_bp.route('/logout')
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))
