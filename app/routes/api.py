"""
API routes for AJAX requests and data retrieval
"""
from flask import jsonify, request
from app import db
from app.models import QuickFix, Favorite, Category
from app.routes import api_bp
from flask_login import current_user, login_required

@api_bp.route('/services/<city>')
def get_services_by_city(city):
    """Get services by city"""
    providers = QuickFix.query.filter(
        QuickFix.city.ilike(f'%{city}%'),
        QuickFix.status == 'approved'
    ).all()
    
    data = [{
        'id': p.id,
        'business_name': p.business_name,
        'category': p.category.name,
        'address': p.address,
        'phone': p.phone_number,
        'rating': p.get_average_rating(),
        'is_available': p.is_available,
        'profile_image': p.profile_image
    } for p in providers]
    
    return jsonify(data)

@api_bp.route('/service/<int:provider_id>')
def get_service_detail(provider_id):
    """Get service provider details"""
    provider = QuickFix.query.get_or_404(provider_id)
    
    if provider.status != 'approved':
        return jsonify({'error': 'Service not available'}), 404
    
    data = {
        'id': provider.id,
        'business_name': provider.business_name,
        'category': provider.category.name,
        'address': provider.address,
        'city': provider.city,
        'phone': provider.phone_number,
        'description': provider.description,
        'working_hours': provider.working_hours,
        'rating': provider.get_average_rating(),
        'is_available': provider.is_available,
        'image_url': provider.image_url,
        'profile_image': provider.profile_image,
        'reviews_count': len(provider.reviews)
    }
    
    return jsonify(data)

@api_bp.route('/categories')
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    data = [{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories]
    
    return jsonify(data)

@api_bp.route('/favorite/<int:provider_id>', methods=['POST'])
@login_required
def toggle_favorite(provider_id):
    """Add or remove from favorites"""
    provider = QuickFix.query.get_or_404(provider_id)
    
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        provider_id=provider_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Removed from favorites'})
    else:
        favorite = Favorite(
            user_id=current_user.id,
            provider_id=provider_id
        )
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Added to favorites'})

@api_bp.route('/call/<int:provider_id>', methods=['POST'])
def track_call(provider_id):
    """Track a call to a service provider"""
    try:
        provider = QuickFix.query.get_or_404(provider_id)
        provider.total_calls = (provider.total_calls or 0) + 1
        db.session.commit()
        return jsonify({'success': True, 'total_calls': provider.total_calls})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error tracking call'})

@api_bp.route('/search')
def search():
    """Search services"""
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    city = request.args.get('city', '').strip()
    
    providers = QuickFix.query.filter_by(status='approved')
    
    if category_id:
        providers = providers.filter_by(category_id=category_id)
    
    if city:
        providers = providers.filter(QuickFix.city.ilike(f'%{city}%'))
    
    if query:
        providers = providers.filter(
            (QuickFix.business_name.ilike(f'%{query}%')) |
            (QuickFix.address.ilike(f'%{query}%'))
        )
    
    providers = providers.all()
    
    data = [{
        'id': p.id,
        'business_name': p.business_name,
        'category': p.category.name,
        'address': p.address,
        'city': p.city,
        'phone': p.phone_number,
        'rating': p.get_average_rating(),
        'is_available': p.is_available,
        'profile_image': p.profile_image
    } for p in providers]
    
    return jsonify(data)

@api_bp.route('/emergency/<category>')
def get_emergency_services(category):
    """Get emergency services by category"""
    providers = QuickFix.query.join(
        QuickFix.category
    ).filter(
        Category.name.ilike(f'%{category}%'),
        QuickFix.status == 'approved',
        QuickFix.is_available == True
    ).all()
    
    data = [{
        'id': p.id,
        'business_name': p.business_name,
        'phone': p.phone_number,
        'address': p.address,
        'city': p.city
    } for p in providers]
    
    return jsonify(data)

@api_bp.route('/call/<int:provider_id>', methods=['POST'])
def increment_call_count(provider_id):
    """Increment call count for a provider"""
    provider = QuickFix.query.get_or_404(provider_id)
    provider.total_calls += 1
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'total_calls': provider.total_calls,
        'message': 'Call count incremented'
    })

@api_bp.route('/emergency-providers')
def get_emergency_providers():
    """Get top 3 highest rated providers for emergency"""
    emergency_categories = ['Hospital', 'Ambulance', 'Police', 'Fire Department']
    
    providers = QuickFix.query.filter(
        QuickFix.status == 'approved',
        QuickFix.category.has(Category.name.in_(emergency_categories))
    ).all()
    
    # Sort by rating and get top 3
    providers.sort(key=lambda p: p.get_average_rating(), reverse=True)
    top_providers = providers[:3]
    
    data = {
        'providers': [{
            'id': p.id,
            'business_name': p.business_name,
            'category': p.category.name,
            'phone_number': p.phone_number,
            'city': p.city,
            'rating': p.get_average_rating(),
            'emoji': '🏥' if p.category.name == 'Hospital' else 
                     '🚑' if p.category.name == 'Ambulance' else
                     '👮' if p.category.name == 'Police' else
                     '🚒' if p.category.name == 'Fire Department' else '⭐'
        } for p in top_providers]
    }
    
    return jsonify(data)
