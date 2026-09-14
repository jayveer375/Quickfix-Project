"""
Routes package for Emergency Service Finder
"""
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_bp = Blueprint('user', __name__, url_prefix='/user')
provider_bp = Blueprint('provider', __name__, url_prefix='/provider')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import route handlers
from app.routes import auth, user, provider, admin, api
