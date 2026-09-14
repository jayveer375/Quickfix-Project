"""
Database models for Emergency Service Finder
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for both regular users and service providers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=True)  # Male, Female, Other
    area = db.Column(db.String(100), nullable=True)  # Area/locality
    city = db.Column(db.String(100), nullable=True, default='Ahmedabad')  # City with default
    role = db.Column(db.String(20), default='user')
    service_type = db.Column(db.String(100), nullable=True)  # For service providers
    profile_image = db.Column(db.String(255), nullable=True, default='default.png')  # Profile image filename
    dark_mode = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    provider_profile = db.relationship('QuickFix', backref='user', uselist=False, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def is_provider(self):
        """Check if user is a service provider"""
        return self.role == 'provider'
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def get_profile_image_url(self):
        """Get profile image URL with proper fallback and file existence check"""
        from flask import current_app
        import os
        
        # Debug print
        print(f"DEBUG: User {self.id} profile_image: '{self.profile_image}'")
        
        if self.profile_image and self.profile_image != 'default.png':
            # Check if file actually exists
            upload_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads'), self.profile_image)
            if os.path.exists(upload_path):
                print(f"DEBUG: Profile image file exists: {upload_path}")
                return f'/static/uploads/{self.profile_image}'
            else:
                print(f"DEBUG: Profile image file NOT found: {upload_path}")
        
        print("DEBUG: Using default avatar")
        return '/static/images/default-avatar.svg'
    
    def __repr__(self):
        return f'<User {self.email}>'

class Category(db.Model):
    """Service category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    emoji = db.Column(db.String(10), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    providers = db.relationship('QuickFix', backref='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class QuickFix(db.Model):
    """Service provider profile model"""
    __tablename__ = 'service_providers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    business_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(300))
    profile_image = db.Column(db.String(300))
    phone_number = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    working_hours = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    is_open = db.Column(db.Boolean, default=True)  # Provider's current open/close status
    status = db.Column(db.String(20), default='pending')
    rating = db.Column(db.Float, default=0.0)
    average_rating = db.Column(db.Float, default=0.0)  # New: calculated average rating
    total_reviews = db.Column(db.Integer, default=0)  # New: total number of reviews
    total_calls = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    services = db.relationship('Service', backref='provider', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='provider', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='provider', cascade='all, delete-orphan')
    
    def is_approved(self):
        """Check if provider is approved"""
        return self.status == 'approved'
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if self.total_reviews > 0:
            return round(self.average_rating, 1)
        return 0.0

    def update_rating_stats(self):
        """Recalculate and update average rating and total reviews"""
        reviews = Review.query.filter_by(provider_id=self.id).all()
        if reviews:
            total = sum(review.rating for review in reviews)
            self.average_rating = total / len(reviews)
            self.total_reviews = len(reviews)
        else:
            self.average_rating = 0.0
            self.total_reviews = 0
        db.session.commit()
    
    def get_rating_stars(self):
        """Get star rating display"""
        rating = self.get_average_rating()
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        return full_stars, half_star
    
    def __repr__(self):
        return f'<QuickFix {self.business_name}>'

class Service(db.Model):
    """Individual service model"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.String(100))
    category = db.Column(db.String(100), nullable=True)  # Service category field
    availability = db.Column(db.String(50), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Review(db.Model):
    """Review and rating model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.rating} stars>'

class Favorite(db.Model):
    """Favorite service provider model"""
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'provider_id', name='unique_favorite'),)
    
    def __repr__(self):
        return f'<Favorite user_id={self.user_id} provider_id={self.provider_id}>'

class City(db.Model):
    """City model for location management"""
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    state = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    areas = db.relationship('Area', backref='city', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<City {self.name}>'

class Area(db.Model):
    """Area/locality model under cities"""
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    pincode = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('name', 'city_id', name='unique_area_per_city'),)
    
    def __repr__(self):
        return f'<Area {self.name}>'
