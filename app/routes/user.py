"""
User routes for searching and managing favorites
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import QuickFix, Category, Favorite, Review, User
from app.routes import user_bp

@user_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """Search for services"""
    from app.models import Service, City, Area
    
    categories = Category.query.all()
    cities = City.query.order_by(City.name).all()
    providers = []
    search_query = ''
    selected_category = None
    selected_city = None
    selected_area = None
    sort_by = request.args.get('sort', 'rating')  # Default to rating
    
    if request.method == 'POST' or request.args:
        search_query = request.form.get('search', '') or request.args.get('search', '')
        search_query = search_query.strip()
        selected_category = request.form.get('category', '') or request.args.get('category', '')
        selected_city = request.form.get('city', '') or request.args.get('city', '')
        selected_city = selected_city.strip()
        selected_area = request.form.get('area', '') or request.args.get('area', '')
        selected_area = selected_area.strip()
        
        # Build query
        query = QuickFix.query.filter_by(status='approved')
        
        if selected_category:
            query = query.filter_by(category_id=int(selected_category))
        
        if selected_city:
            query = query.filter(QuickFix.city.ilike(f'%{selected_city}%'))
        
        # Filter by area using the user's area field
        if selected_area:
            query = query.join(QuickFix.user).filter(
                db.func.lower(db.func.trim(db.text('users.area'))) == selected_area.lower()
            )
        
        if search_query:
            query = query.filter(
                (QuickFix.business_name.ilike(f'%{search_query}%')) |
                (QuickFix.address.ilike(f'%{search_query}%'))
            )
        
        # Apply sorting at database level for better performance
        if sort_by == 'rating':
            # Sort by highest rating first
            query = query.order_by(QuickFix.average_rating.desc(), QuickFix.total_reviews.desc())
        elif sort_by == 'reviews':
            # Sort by most reviews first
            query = query.order_by(QuickFix.total_reviews.desc(), QuickFix.average_rating.desc())
        elif sort_by == 'calls-high':
            # Legacy support - sort by most calls
            query = query.order_by(QuickFix.total_calls.desc())
        elif sort_by == 'newest':
            # Sort by newest providers
            query = query.order_by(QuickFix.created_at.desc())
        else:
            # Default: sort by rating and reviews
            query = query.order_by(QuickFix.average_rating.desc(), QuickFix.total_reviews.desc())
        
        providers = query.all()
        
        # For price sorting, we need to sort in Python since price is in Service model
        if sort_by in ['low_price', 'high_price']:
            # Get providers with their minimum service price
            providers_with_price = []
            for provider in providers:
                if provider.services:
                    # Get minimum price from services (convert string to float, handle non-numeric)
                    prices = []
                    for service in provider.services:
                        if service.price:
                            try:
                                # Remove currency symbols and convert to float
                                price_str = service.price.replace('₹', '').replace(',', '').strip()
                                prices.append(float(price_str))
                            except (ValueError, AttributeError):
                                pass
                    
                    if prices:
                        min_price = min(prices)
                        providers_with_price.append((provider, min_price))
                    else:
                        # No valid prices, put at end with high value
                        providers_with_price.append((provider, float('inf')))
                else:
                    # No services, put at end
                    providers_with_price.append((provider, float('inf')))
            
            # Sort by price
            reverse = (sort_by == 'high_price')
            providers_with_price.sort(key=lambda x: x[1], reverse=reverse)
            providers = [p[0] for p in providers_with_price]
    else:
        # Default: show all approved providers sorted by rating
        providers = QuickFix.query.filter_by(status='approved')\
            .order_by(QuickFix.average_rating.desc(), QuickFix.total_reviews.desc())\
            .all()
    
    return render_template('search_saas.html', 
                         categories=categories,
                         cities=cities,
                         providers=providers,
                         search_query=search_query,
                         selected_category=selected_category,
                         selected_city=selected_city,
                         selected_area=selected_area,
                         sort_by=sort_by)

@user_bp.route('/service/<int:provider_id>')
def service_detail(provider_id):
    """Legacy route - redirect to provider profile"""
    return redirect(url_for('user.provider_profile', provider_id=provider_id))
@user_bp.route('/provider/<int:provider_id>')
def provider_profile(provider_id):
    """View provider profile with ratings and reviews"""
    provider = QuickFix.query.get_or_404(provider_id)

    if provider.status != 'approved':
        flash('This provider is not available', 'error')
        return redirect(url_for('user.search'))

    # Get all reviews sorted by newest first
    reviews = Review.query.filter_by(provider_id=provider_id).order_by(Review.created_at.desc()).all()

    # Check if favorite
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            provider_id=provider_id
        ).first() is not None

    return render_template('provider_profile.html',
                         provider=provider,
                         reviews=reviews,
                         is_favorite=is_favorite)

@user_bp.route('/favorites')
@login_required
def favorites():
    """View user's favorite services"""
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    providers = [fav.provider for fav in favorites]
    
    return render_template('favorites.html', providers=providers)

@user_bp.route('/add-review/<int:provider_id>', methods=['POST'])
@login_required
def add_review(provider_id):
    """Add a new review for a service provider"""
    provider = QuickFix.query.get_or_404(provider_id)

    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    # Validate rating
    if not rating or rating < 1 or rating > 5:
        flash('Please select a rating between 1 and 5 stars', 'error')
        return redirect(url_for('user.provider_profile', provider_id=provider_id))

    # Always create new review (allow multiple reviews per user)
    review = Review(
        provider_id=provider_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    flash('Thank you for your review!', 'success')

    # Update provider's rating statistics
    db.session.commit()
    provider.update_rating_stats()

    return redirect(url_for('user.provider_profile', provider_id=provider_id))

@user_bp.route('/update-review/<int:review_id>', methods=['POST'])
@login_required
def update_review(review_id):
    """Update an existing review"""
    review = Review.query.get_or_404(review_id)

    # Ensure user can only update their own review
    if review.user_id != current_user.id:
        flash('You can only update your own reviews', 'error')
        return redirect(url_for('user.search'))

    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    # Validate rating
    if not rating or rating < 1 or rating > 5:
        flash('Please select a rating between 1 and 5 stars', 'error')
        return redirect(url_for('user.provider_profile', provider_id=review.provider_id))

    # Update existing review
    review.rating = rating
    review.comment = comment
    review.created_at = db.func.now()
    db.session.commit()

    # Update provider's rating statistics
    provider = QuickFix.query.get(review.provider_id)
    if provider:
        provider.update_rating_stats()

    flash('Your review has been updated successfully', 'success')
    return redirect(url_for('user.provider_profile', provider_id=review.provider_id))
@user_bp.route('/delete-review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    """Delete a user's own review"""
    review = Review.query.get_or_404(review_id)

    # Ensure user can only delete their own review
    if review.user_id != current_user.id:
        flash('You can only delete your own reviews', 'error')
        return redirect(url_for('user.search'))

    provider_id = review.provider_id
    db.session.delete(review)
    db.session.commit()

    # Update provider's rating statistics
    provider = QuickFix.query.get(provider_id)
    if provider:
        provider.update_rating_stats()

    flash('Your review has been deleted', 'success')
    return redirect(url_for('user.provider_profile', provider_id=provider_id))
