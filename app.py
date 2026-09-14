"""
Emergency & Service Finder - Main Application Entry Point
"""
import os
from app import create_app, db
from flask import render_template, redirect, url_for

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Home route
@app.route('/')
def index():
    """Home page"""
    return render_template('index_saas.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
