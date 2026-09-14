# Complete Profile Image Implementation Snippets

## 1️⃣ PROVIDER DASHBOARD

### HTML Template (provider_dashboard.html)
```html
<!-- Profile Photo Section -->
<div class="profile-photo-section">
    <div class="profile-photo-dashboard">
        {% if current_user.profile_image and current_user.profile_image != 'default.png' %}
            <img src="{{ url_for('static', filename='uploads/' + current_user.profile_image) }}" 
                 alt="{{ provider.business_name }}" 
                 class="profile-img-dashboard"
                 onerror="this.src='{{ url_for('static', filename='images/default-avatar.svg') }}'">
        {% else %}
            <img src="{{ url_for('static', filename='images/default-avatar.svg') }}" 
                 alt="Default Profile" 
                 class="profile-img-dashboard">
        {% endif %}
    </div>
</div>
```

### CSS for Dashboard
```css
.profile-photo-dashboard {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 3px solid var(--primary);
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    position: relative;
}

.profile-img-dashboard {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.profile-photo-dashboard:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

body.dark-mode .profile-photo-dashboard {
    border-color: var(--primary-light);
    box-shadow: 0 8px 16px rgba(255,255,255,0.1);
}
```

## 2️⃣ PROVIDER PUBLIC PROFILE PAGE

### HTML Template (service_detail.html)
```html
<!-- Provider Header with Large Profile Image -->
<div class="provider-detail-header">
    <!-- Large Profile Image -->
    <div class="provider-profile-large">
        {% if provider.user.profile_image and provider.user.profile_image != 'default.png' %}
            <img src="{{ url_for('static', filename='uploads/' + provider.user.profile_image) }}" 
                 alt="{{ provider.business_name }}" 
                 class="profile-img-large"
                 onerror="this.src='{{ url_for('static', filename='images/default-avatar.svg') }}'">
        {% else %}
            <img src="{{ url_for('static', filename='images/default-avatar.svg') }}" 
                 alt="Default Profile" 
                 class="profile-img-large">
        {% endif %}
    </div>

    <!-- Provider Info -->
    <div class="provider-info">
        <h1>{{ provider.business_name }}</h1>
        <p class="category">{{ provider.category.name }}</p>
        <!-- Rest of provider details -->
    </div>
</div>
```

### CSS for Public Profile
```css
.provider-profile-large {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 4px solid var(--primary);
    overflow: hidden;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.profile-img-large {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.provider-profile-large:hover {
    transform: scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
    .provider-profile-large {
        width: 120px;
        height: 120px;
        border-width: 3px;
    }
}
```

## 3️⃣ SEARCH PAGE (Service Provider Cards)

### HTML Template (search_saas.html)
```html
<!-- Provider Card with Profile Image -->
<div class="provider-card">
    <div class="provider-card-content">
        <!-- Profile Image -->
        <div class="provider-profile-card">
            {% if provider.user.profile_image and provider.user.profile_image != 'default.png' %}
                <img src="{{ url_for('static', filename='uploads/' + provider.user.profile_image) }}" 
                     alt="{{ provider.business_name }}" 
                     class="profile-img-card"
                     onerror="this.src='{{ url_for('static', filename='images/default-avatar.svg') }}'">
            {% else %}
                <img src="{{ url_for('static', filename='images/default-avatar.svg') }}" 
                     alt="Default Profile" 
                     class="profile-img-card">
            {% endif %}
        </div>

        <!-- Provider Name -->
        <h3 class="provider-name">{{ provider.business_name }}</h3>
        
        <!-- Rest of card content -->
    </div>
</div>
```

### CSS for Search Cards
```css
.provider-profile-card {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 2px solid var(--primary);
    overflow: hidden;
    margin: 0 auto 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.profile-img-card {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.provider-card:hover .provider-profile-card {
    transform: scale(1.1);
    border-color: var(--primary-light);
    box-shadow: 0 6px 12px rgba(99, 102, 241, 0.3);
}

@media (max-width: 480px) {
    .provider-profile-card {
        width: 45px;
        height: 45px;
    }
}
```

## 4️⃣ ADMIN PANEL (All Providers List)

### HTML Template (admin_providers.html)
```html
<table>
    <thead>
        <tr>
            <th>Profile</th>
            <th>Business Name</th>
            <th>Category</th>
            <th>Owner</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for provider in providers %}
        <tr>
            <td>
                <div class="admin-profile-thumbnail">
                    {% if provider.user.profile_image and provider.user.profile_image != 'default.png' %}
                        <img src="{{ url_for('static', filename='uploads/' + provider.user.profile_image) }}" 
                             alt="{{ provider.business_name }}" 
                             class="profile-img-admin"
                             onerror="this.src='{{ url_for('static', filename='images/default-avatar.svg') }}'">
                    {% else %}
                        <img src="{{ url_for('static', filename='images/default-avatar.svg') }}" 
                             alt="Default Profile" 
                             class="profile-img-admin">
                    {% endif %}
                </div>
            </td>
            <td>{{ provider.business_name }}</td>
            <td>{{ provider.category.name }}</td>
            <td>{{ provider.user.name }}</td>
            <td>
                <span class="status-badge status-{{ provider.status }}">
                    {{ provider.status|upper }}
                </span>
            </td>
            <td>
                <!-- Action buttons -->
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

### CSS for Admin Panel
```css
.admin-profile-thumbnail {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--primary);
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.profile-img-admin {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.admin-profile-thumbnail:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.status-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-approved { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
.status-pending { background: rgba(251, 146, 60, 0.2); color: #fb923c; }
.status-rejected { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
```

## 5️⃣ FLASK ROUTES CONFIRMATION

### Provider Routes (app/routes/provider.py)
```python
@provider_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """Setup service provider profile with image upload"""
    if not current_user.is_provider():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    provider = ServiceProvider.query.filter_by(user_id=current_user.id).first()
    categories = Category.query.all()
    
    if request.method == 'POST':
        # Handle profile image upload
        profile_image_filename = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Validate file size (2MB max)
                    file.seek(0, 2)
                    file_size = file.tell()
                    file.seek(0)
                    
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
        
        # Handle other form fields
        business_name = request.form.get('business_name', '').strip()
        category_id = request.form.get('category_id', type=int)
        # ... other fields
        
        # Save provider data
        if provider:
            # Update existing provider
            provider.business_name = business_name
            provider.category_id = category_id
            # ... update other fields
        else:
            # Create new provider
            provider = ServiceProvider(
                user_id=current_user.id,
                business_name=business_name,
                category_id=category_id,
                # ... other fields
            )
            db.session.add(provider)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('provider.dashboard'))
    
    return render_template('provider_setup.html', provider=provider, categories=categories)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### User Model Enhancement (app/models.py)
```python
class User(UserMixin, db.Model):
    # ... existing fields
    profile_image = db.Column(db.String(255), nullable=True, default='default.png')
    
    def get_profile_image_url(self):
        """Get profile image URL with fallback"""
        if self.profile_image and self.profile_image != 'default.png':
            return url_for('static', filename=f'uploads/{self.profile_image}')
        return url_for('static', filename='images/default-avatar.svg')
```

## 6️⃣ EDIT PROFILE MODAL

### HTML Template (provider_dashboard.html - Modal Section)
```html
<!-- Edit Profile Modal -->
<div class="modal" id="editProfileModal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Edit Profile</h2>
            <button class="modal-close" onclick="closeEditModal()">&times;</button>
        </div>
        
        <form id="editProfileForm" method="POST" action="{{ url_for('provider.update_profile') }}" enctype="multipart/form-data">
            <!-- Profile Photo Upload -->
            <div class="form-group text-center">
                <div class="profile-upload-container">
                    <div class="profile-photo-preview">
                        <img id="modalProfilePreview" 
                             src="{{ current_user.get_profile_image_url() }}" 
                             alt="Profile Preview"
                             onerror="this.src='{{ url_for('static', filename='images/default-avatar.svg') }}'">
                    </div>
                    <button type="button" class="profile-upload-btn" onclick="document.getElementById('modalProfilePhoto').click()">
                        <i class="fas fa-camera"></i>
                    </button>
                </div>
                <input type="file" id="modalProfilePhoto" name="profile_image" accept="image/jpeg,image/jpg,image/png" style="display: none;">
                <p class="upload-hint">Click camera to change photo (JPG, PNG - Max 2MB)</p>
            </div>
            
            <!-- Other form fields -->
            <div class="form-group">
                <label for="edit_business_name">Business Name *</label>
                <input type="text" id="edit_business_name" name="business_name" 
                       value="{{ provider.business_name }}" required>
            </div>
            
            <!-- More form fields... -->
            
            <div class="modal-actions">
                <button type="button" onclick="closeEditModal()" class="btn btn-secondary">Cancel</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
        </form>
    </div>
</div>
```

### CSS for Edit Modal
```css
.profile-upload-container {
    position: relative;
    display: inline-block;
    margin-bottom: 1rem;
}

.profile-photo-preview {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid var(--primary);
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    position: relative;
}

.profile-photo-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-upload-btn {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.profile-upload-btn:hover {
    transform: scale(1.1);
    background: var(--primary-dark);
}

.upload-hint {
    font-size: 0.875rem;
    color: var(--gray);
    margin-top: 0.5rem;
}
```

## 7️⃣ JAVASCRIPT FOR IMAGE HANDLING

### JavaScript (saas.js)
```javascript
// Profile image preview functionality
function initializeProfileImageHandling() {
    // Setup page profile photo
    const setupPhotoInput = document.getElementById('profilePhoto');
    if (setupPhotoInput) {
        setupPhotoInput.addEventListener('change', function(e) {
            handleProfileImagePreview(e, 'profilePreview');
        });
    }
    
    // Modal profile photo
    const modalPhotoInput = document.getElementById('modalProfilePhoto');
    if (modalPhotoInput) {
        modalPhotoInput.addEventListener('change', function(e) {
            handleProfileImagePreview(e, 'modalProfilePreview');
        });
    }
}

function handleProfileImagePreview(event, previewId) {
    const file = event.target.files[0];
    if (file) {
        // Validate file size (2MB max)
        if (file.size > 2 * 1024 * 1024) {
            showNotification('File size must be less than 2MB', 'error');
            event.target.value = '';
            return;
        }
        
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please select a valid image file (JPG, PNG)', 'error');
            event.target.value = '';
            return;
        }
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
            }
        };
        reader.readAsDataURL(file);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProfileImageHandling();
});
```

## 8️⃣ FALLBACK LOGIC & ERROR HANDLING

### Enhanced Image Error Handling
```javascript
// Global image error handler
function handleImageError(img) {
    img.onerror = null; // Prevent infinite loop
    img.src = '/static/images/default-avatar.svg';
    img.classList.add('image-error');
}

// Initialize all profile images with error handling
function initializeAllProfileImages() {
    document.querySelectorAll('img[src*="uploads/"]').forEach(img => {
        img.onerror = function() {
            handleImageError(this);
        };
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', initializeAllProfileImages);
```

### CSS for Error States
```css
.image-error {
    opacity: 0.7;
    filter: grayscale(100%);
}

.profile-image-loading {
    background: var(--gray-lighter);
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-image-loading::after {
    content: '';
    width: 20px;
    height: 20px;
    border: 2px solid var(--gray-light);
    border-top: 2px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
```

## 9️⃣ RESPONSIVE CSS FRAMEWORK

### Complete Responsive Profile Image CSS
```css
/* Base profile image styles */
.profile-image-base {
    border-radius: 50%;
    object-fit: cover;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Size variations */
.profile-xs { width: 30px; height: 30px; border: 1px solid var(--primary); }
.profile-sm { width: 40px; height: 40px; border: 2px solid var(--primary); }
.profile-md { width: 50px; height: 50px; border: 2px solid var(--primary); }
.profile-lg { width: 80px; height: 80px; border: 3px solid var(--primary); }
.profile-xl { width: 120px; height: 120px; border: 3px solid var(--primary); }
.profile-2xl { width: 150px; height: 150px; border: 4px solid var(--primary); }

/* Hover effects */
.profile-hover:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

/* Dark mode support */
body.dark-mode .profile-image-base {
    border-color: var(--primary-light);
    box-shadow: 0 4px 8px rgba(255,255,255,0.1);
}

/* Responsive breakpoints */
@media (max-width: 768px) {
    .profile-2xl { width: 120px; height: 120px; border-width: 3px; }
    .profile-xl { width: 100px; height: 100px; border-width: 3px; }
    .profile-lg { width: 70px; height: 70px; border-width: 2px; }
}

@media (max-width: 480px) {
    .profile-2xl { width: 100px; height: 100px; border-width: 3px; }
    .profile-xl { width: 80px; height: 80px; border-width: 2px; }
    .profile-lg { width: 60px; height: 60px; border-width: 2px; }
    .profile-md { width: 45px; height: 45px; border-width: 2px; }
    .profile-sm { width: 35px; height: 35px; border-width: 1px; }
}
```

## 🔟 SECURITY IMPLEMENTATION

### Enhanced Security Measures
```python
import os
from werkzeug.utils import secure_filename
from PIL import Image
import magic

def validate_and_process_image(file):
    """Comprehensive image validation and processing"""
    
    # Check file size (2MB max)
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 2 * 1024 * 1024:
        return False, "File size exceeds 2MB limit"
    
    # Validate file extension
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return False, "Invalid file type. Only JPG and PNG allowed"
    
    # Validate MIME type using python-magic
    file_content = file.read()
    file.seek(0)
    
    mime_type = magic.from_buffer(file_content, mime=True)
    allowed_mimes = {'image/jpeg', 'image/png'}
    
    if mime_type not in allowed_mimes:
        return False, "Invalid file format detected"
    
    # Additional security: Try to open with PIL to ensure it's a valid image
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)  # Reset file pointer after verification
    except Exception:
        return False, "Corrupted or invalid image file"
    
    return True, "Valid image file"

def save_profile_image(file, user_id):
    """Securely save profile image"""
    
    # Validate image
    is_valid, message = validate_and_process_image(file)
    if not is_valid:
        return False, message
    
    # Generate secure filename
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'user_{user_id}_{int(time.time())}.{file_extension}')
    
    # Ensure upload directory exists
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Optional: Resize image to standard size
    try:
        with Image.open(filepath) as img:
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            img.save(filepath, optimize=True, quality=85)
    except Exception:
        pass  # Continue even if resize fails
    
    return True, filename
```

This implementation provides:
- ✅ Complete profile image display across all pages
- ✅ Proper fallback handling for missing images
- ✅ Responsive design with appropriate sizing
- ✅ Security validation and file handling
- ✅ Clean, production-ready code
- ✅ Error handling and user feedback
- ✅ Modern CSS with hover effects
- ✅ JavaScript for real-time preview
- ✅ Database integration with proper cleanup
- ✅ Cross-browser compatibility