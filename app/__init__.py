"""
Application factory for Emergency Service Finder
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment (development, testing, production)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth_bp, user_bp, provider_bp, admin_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Initialize default data
        from app.models import Category, User
        
        # Create default categories if they don't exist
        if Category.query.count() == 0:
            categories = [
                Category(name='Hospital', description='Medical facilities and hospitals'),
                Category(name='Ambulance', description='Emergency ambulance services'),
                Category(name='Electrician', description='Electrical repair and installation'),
                Category(name='Plumber', description='Plumbing services'),
                Category(name='Mechanic', description='Vehicle repair and maintenance'),
                Category(name='Police', description='Police and law enforcement'),
                Category(name='Fire Department', description='Fire and rescue services'),
                Category(name='Locksmith', description='Lock and key services'),
                Category(name='Gas Station', description='Fuel and gas services'),
                Category(name='Pharmacy', description='Pharmacy and medical supplies'),
            ]
            for category in categories:
                db.session.add(category)
            db.session.commit()
        
        # Create admin user if it doesn't exist
        if User.query.filter_by(email='admin@gmail.com').first() is None:
            admin = User(
                email='admin@gmail.com',
                name='Admin User',
                phone='0000000000',
                role='admin'
            )
            admin.set_password('admin@123')
            db.session.add(admin)
            db.session.commit()
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Custom Jinja filters
    @app.template_filter('whatsapp_format')
    def whatsapp_format(phone_number):
        """
        Format phone number for WhatsApp link
        Removes all non-digit characters
        For 10-digit numbers, adds India country code (+91)
        For numbers with +, preserves the country code
        """
        if not phone_number:
            return ''
        
        original = str(phone_number).strip()
        # Remove all non-digit characters
        clean_number = ''.join(filter(str.isdigit, original))
        
        # If original had + and resulted in 10 digits, user likely entered country code separately
        # Example: "+95 1 210 8880" -> "9512108880" (10 digits)
        # In this case, we should NOT add 91
        if original.startswith('+'):
            # User explicitly provided country code, use as-is
            return clean_number
        
        # If number is exactly 10 digits and no + was present, assume India (+91)
        if len(clean_number) == 10:
            clean_number = '91' + clean_number
        
        return clean_number
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app
