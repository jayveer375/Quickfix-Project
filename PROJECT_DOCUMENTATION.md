# QuickFix - Emergency & Service Provider Platform

## Project Name
**QuickFix** - A Modern SaaS Platform for Finding Emergency and Professional Services

---

## Project Description
QuickFix is a comprehensive web-based platform that connects users with verified service providers in their area. The application provides a seamless experience for finding emergency services, professional services, and connecting with trusted providers. Built with modern web technologies, it features a premium SaaS design with advanced functionality for both users and administrators.

---

## Project Objectives
1. Create a centralized platform for service discovery and provider management
2. Implement real-time service provider search with location-based filtering
3. Provide emergency service access with quick provider lookup
4. Enable service providers to manage their profiles and services
5. Implement an admin dashboard for platform management and monitoring
6. Deliver a modern, responsive user interface with dark mode support
7. Track service provider performance through call counters and ratings
8. Verify and badge trusted service providers

---

## Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Server**: Python 3.13

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom SaaS design with glassmorphism effects
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js for analytics

### Key Libraries
- Flask-SQLAlchemy 3.0.5 - Database ORM
- Werkzeug 2.3.7 - Security utilities
- python-dotenv 1.0.0 - Environment configuration

---

## Database Used
**SQLite** with SQLAlchemy ORM

### Database Location
`instance/database.db`

### Database Schema
The application uses 6 main tables:
- **users** - User accounts (regular users, providers, admins)
- **categories** - Service categories
- **service_providers** - Provider profiles with ratings and verification status
- **services** - Individual services offered by providers
- **reviews** - User reviews and ratings
- **favorites** - User favorite providers

---

## Features List

### 🎨 User Interface Features
1. **Modern SaaS Design** - Premium glassmorphism UI with gradient buttons
2. **Dark Mode Support** - Full dark/light theme toggle with localStorage persistence
3. **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
4. **Smooth Animations** - 3D button effects, hover animations, and transitions
5. **Real-time Search** - Instant service provider search with filters

### 👥 User Features
1. **Service Search** - Search providers by name, category, and location
2. **Location Filtering** - Browser geolocation detection and distance calculation
3. **Provider Details** - View comprehensive provider information and reviews
4. **Favorites System** - Save and manage favorite service providers
5. **Rating & Reviews** - Leave ratings and reviews for services used
6. **Call Counter** - Track how many times a provider has been contacted
7. **Emergency Mode** - Quick access to top-rated emergency services
8. **Sorting Options** - Sort by rating, popularity (calls), or newest

### 🏢 Provider Features
1. **Provider Dashboard** - Manage profile and services
2. **Service Management** - Add, edit, and manage services
3. **Profile Setup** - Complete provider profile with images and details
4. **Availability Status** - Toggle service availability
5. **Performance Tracking** - View call count and ratings

### 👨‍💼 Admin Features
1. **Admin Dashboard** - Overview with statistics and charts
2. **Provider Management** - View, approve, reject, and delete providers
3. **Approval System** - Review pending provider applications
4. **Category Management** - Create and manage service categories
5. **User Management** - View all users and their roles
6. **Analytics** - Charts showing provider distribution, growth, ratings, and verification status
7. **Verification System** - Mark providers as verified

### 🚨 Emergency Mode
- Floating red emergency button on search page
- Quick access to top 3 highest-rated emergency providers
- Categories: Hospital, Ambulance, Police, Fire Department
- One-click calling interface

### 📊 Call Counter System
- Tracks total calls for each provider
- Incremented via API endpoint
- Displayed on provider cards
- Used for popularity sorting

### 🌙 Dark Mode
- Toggle button in navigation bar
- Smooth transitions between themes
- Persistent preference storage
- Full UI coverage including all templates

### ✅ Verified Provider Badge
- Green checkmark badge for verified providers
- Orange pending badge for unverified providers
- Visual distinction in search results
- Admin verification system

### 📍 Location Filter
- Browser geolocation detection
- City-based filtering
- Distance calculation
- Automatic location suggestions

---

## How to Run the Project

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or Extract the Project**
   ```bash
   cd QuickFix
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open browser and go to: `http://localhost:5000`

### Test Credentials
- **Admin**: admin@emergency.com / admin123
- **Provider**: hospital_provider_0@demo.com / provider123
- **Regular User**: Create new account via registration

---

## Folder Structure

```
QuickFix/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py             # Admin routes
│   │   ├── auth.py              # Authentication routes
│   │   ├── user.py              # User search routes
│   │   ├── provider.py          # Provider routes
│   │   └── api.py               # API endpoints
│   ├── static/
│   │   ├── css/
│   │   │   ├── saas.css         # Main SaaS styling
│   │   │   ├── style.css        # Additional styles
│   │   │   ├── modern.css       # Modern theme
│   │   │   └── premium.css      # Premium theme
│   │   └── js/
│   │       ├── saas.js          # SaaS functionality
│   │       ├── script.js        # Main scripts
│   │       └── premium.js       # Premium features
│   └── templates/
│       ├── base_saas.html       # Main SaaS base template
│       ├── index_saas.html      # Home page
│       ├── search_saas.html     # Search page
│       ├── login_saas.html      # Login page
│       ├── register_saas.html   # Registration page
│       ├── admin_dashboard_saas.html  # Admin dashboard
│       ├── admin_approvals.html # Provider approvals
│       ├── admin_providers.html # Provider management
│       ├── admin_categories.html # Category management
│       ├── admin_users.html     # User management
│       ├── service_detail.html  # Service details
│       ├── favorites.html       # Favorites page
│       ├── provider_dashboard.html
│       ├── provider_setup.html
│       ├── provider_add_service.html
│       ├── provider_edit_service.html
│       ├── 404.html             # 404 error page
│       └── 500.html             # 500 error page
├── instance/
│   └── database.db              # SQLite database
├── uploads/                     # User uploaded files
├── app.py                       # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
└── .gitignore                   # Git ignore file
```

---

## Key Files Description

### Core Application Files
- **app.py** - Main entry point, defines home route
- **config.py** - Configuration for development, testing, and production
- **app/__init__.py** - Application factory, database initialization
- **app/models.py** - SQLAlchemy database models

### Routes
- **app/routes/admin.py** - Admin dashboard, provider management, approvals
- **app/routes/auth.py** - Login, registration, logout
- **app/routes/user.py** - Service search, favorites, reviews
- **app/routes/provider.py** - Provider dashboard, service management
- **app/routes/api.py** - REST API endpoints for AJAX requests

### Frontend Assets
- **app/static/css/saas.css** - Complete SaaS design system (2000+ lines)
- **app/static/js/saas.js** - Dark mode, call counter, emergency mode (500+ lines)

### Templates
- **base_saas.html** - Main layout with navigation and dark mode toggle
- **index_saas.html** - Home page with hero section and features
- **search_saas.html** - Service search with filters and emergency button
- **admin_dashboard_saas.html** - Admin dashboard with charts and statistics

---

## API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /user/search` - Search services
- `GET /auth/login` - Login page
- `GET /auth/register` - Registration page
- `GET /api/categories` - Get all categories
- `GET /api/services/<city>` - Get services by city
- `GET /api/emergency-providers` - Get emergency providers

### Authenticated Endpoints
- `POST /api/call/<provider_id>` - Increment call counter
- `POST /api/favorite/<provider_id>` - Toggle favorite
- `GET /user/favorites` - View favorites
- `POST /user/add-review/<provider_id>` - Add review

### Admin Endpoints
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/approvals` - Pending approvals
- `POST /admin/approve/<provider_id>` - Approve provider
- `POST /admin/reject/<provider_id>` - Reject provider
- `POST /admin/delete-provider/<provider_id>` - Delete provider
- `GET /admin/providers` - All providers
- `GET /admin/users` - All users
- `GET /admin/categories` - Manage categories

---

## Database Models

### User Model
- id, email, password_hash, name, phone, role, dark_mode, created_at
- Relationships: provider_profile, favorites, reviews

### ServiceProvider Model
- id, user_id, category_id, business_name, address, city, latitude, longitude
- image_url, profile_image, phone_number, description, working_hours
- is_available, status, rating, total_calls, is_verified, created_at, updated_at
- Relationships: services, reviews, favorites

### Category Model
- id, name, description, emoji, created_at
- Relationships: providers

### Service Model
- id, provider_id, name, description, price, availability, created_at

### Review Model
- id, provider_id, user_id, rating, comment, created_at

### Favorite Model
- id, user_id, provider_id, created_at

---

## Future Improvements

1. **Payment Integration** - Add payment gateway for premium services
2. **Real-time Notifications** - Push notifications for service requests
3. **Advanced Analytics** - Detailed provider performance metrics
4. **Mobile App** - Native iOS and Android applications
5. **Video Calls** - In-app video consultation feature
6. **AI Recommendations** - Machine learning-based provider suggestions
7. **Multi-language Support** - Internationalization (i18n)
8. **Advanced Filtering** - Price range, availability, certifications
9. **Provider Verification** - Document upload and verification system
10. **Booking System** - Schedule appointments with providers
11. **Payment History** - Transaction tracking and invoicing
12. **Provider Analytics** - Detailed performance dashboards

---

## Security Features

1. **Password Hashing** - Werkzeug security for password storage
2. **Session Management** - Secure session cookies with HTTPOnly flag
3. **CSRF Protection** - Flask-Login integration
4. **SQL Injection Prevention** - SQLAlchemy parameterized queries
5. **File Upload Validation** - Allowed extensions and size limits
6. **Role-Based Access Control** - Admin, provider, and user roles

---

## Performance Optimizations

1. **Database Indexing** - Indexed city column for faster searches
2. **Lazy Loading** - SQLAlchemy relationships configured efficiently
3. **CSS Optimization** - Minified and organized stylesheets
4. **JavaScript Optimization** - Vanilla JS without heavy dependencies
5. **Image Optimization** - Compressed uploaded images

---

## Conclusion

QuickFix is a production-ready SaaS platform that demonstrates modern web development practices. It combines a robust backend with Flask and SQLAlchemy with a premium frontend featuring glassmorphism design, dark mode, and advanced interactivity. The application is scalable, maintainable, and suitable for real-world deployment.

The project showcases:
- Full-stack web development capabilities
- Database design and optimization
- User authentication and authorization
- Responsive UI/UX design
- RESTful API development
- Admin panel implementation
- Real-time features (call counter, favorites)

This project is ideal for college submission as it demonstrates comprehensive understanding of web development frameworks, database management, and modern UI/UX principles.

---

## Author Notes

This project was developed as a comprehensive demonstration of Flask web development with modern SaaS design principles. All code is production-ready and follows best practices for security, performance, and maintainability.

**Last Updated**: February 2026
**Version**: 1.0.0
**Status**: Production Ready
