/* ============================================
   SERVICEFINDER - MODERN SAAS UI 2026
   ============================================ */

// Dark Mode Toggle
const themeToggle = document.querySelector('.theme-toggle');
const htmlElement = document.documentElement;

// Check for saved theme preference
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
  document.body.classList.add('dark-mode');
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
  });

  // Set initial icon
  themeToggle.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
}

// Animate Counter Numbers
function animateCounter(element, target, duration = 1000) {
  let current = 0;
  const increment = target / (duration / 16);
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = target;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(current);
    }
  }, 16);
}

// Trigger counter animation when stats are visible
const observerOptions = {
  threshold: 0.5,
  rootMargin: '0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && entry.target.classList.contains('stat-number')) {
      const target = parseInt(entry.target.getAttribute('data-target')) || 0;
      animateCounter(entry.target, target);
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.stat-number').forEach(el => {
  observer.observe(el);
});

// Call Counter - Increment on button click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('call-btn')) {
    const providerId = e.target.getAttribute('data-provider-id');
    const callCountElement = e.target.closest('.provider-card')?.querySelector('.call-count');
    
    if (providerId) {
      fetch(`/api/call/${providerId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (callCountElement) {
          callCountElement.textContent = data.total_calls;
        }
      })
      .catch(error => console.error('Error:', error));
    }
  }
});

// Emergency Mode - Show top 3 providers
const emergencyBtn = document.querySelector('.emergency-btn');
const emergencyModal = document.querySelector('.emergency-modal');
const emergencyClose = document.querySelector('.emergency-close');

if (emergencyBtn) {
  emergencyBtn.addEventListener('click', () => {
    if (emergencyModal) {
      emergencyModal.classList.add('active');
      loadEmergencyProviders();
    }
  });
}

if (emergencyClose) {
  emergencyClose.addEventListener('click', () => {
    if (emergencyModal) {
      emergencyModal.classList.remove('active');
    }
  });
}

// Close modal on background click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('active');
  }
});

function loadEmergencyProviders() {
  fetch('/api/emergency-providers')
    .then(response => response.json())
    .then(data => {
      const container = document.querySelector('.emergency-providers');
      if (container) {
        container.innerHTML = data.providers.map(provider => `
          <div class="provider-card">
            <div class="provider-emoji">${provider.emoji}</div>
            <h3 class="provider-name">${provider.business_name}</h3>
            <p class="provider-city">📍 ${provider.city}</p>
            <div class="rating-stars">
              ${Array(5).fill().map((_, i) => 
                `<span class="star">${i < Math.floor(provider.rating) ? '★' : '☆'}</span>`
              ).join('')}
              <span class="rating-text">(${provider.rating})</span>
            </div>
            <a href="tel:${provider.phone_number}" class="btn btn-danger w-full">
              📞 Call Now
            </a>
          </div>
        `).join('');
      }
    })
    .catch(error => console.error('Error:', error));
}

// Location Detection
function detectLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        // Store location for filtering
        localStorage.setItem('userLocation', JSON.stringify({ latitude, longitude }));
        filterByLocation(latitude, longitude);
      },
      (error) => {
        console.log('Location access denied, using manual filter');
      }
    );
  }
}

function filterByLocation(lat, lng) {
  // Filter providers by proximity
  const providers = document.querySelectorAll('.provider-card');
  providers.forEach(card => {
    const providerLat = parseFloat(card.getAttribute('data-lat'));
    const providerLng = parseFloat(card.getAttribute('data-lng'));
    
    if (providerLat && providerLng) {
      const distance = calculateDistance(lat, lng, providerLat, providerLng);
      card.setAttribute('data-distance', distance);
    }
  });
}

function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth's radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// Sorting Functionality
const sortSelect = document.querySelector('.sort-select');
if (sortSelect) {
  sortSelect.addEventListener('change', (e) => {
    const sortValue = e.target.value;
    const grid = document.querySelector('.providers-grid');
    const cards = Array.from(grid.querySelectorAll('.provider-card'));

    if (sortValue === 'rating-high') {
      cards.sort((a, b) => {
        const ratingA = parseFloat(a.getAttribute('data-rating')) || 0;
        const ratingB = parseFloat(b.getAttribute('data-rating')) || 0;
        return ratingB - ratingA;
      });
    } else if (sortValue === 'calls-high') {
      cards.sort((a, b) => {
        const callsA = parseInt(a.getAttribute('data-calls')) || 0;
        const callsB = parseInt(b.getAttribute('data-calls')) || 0;
        return callsB - callsA;
      });
    } else if (sortValue === 'newest') {
      cards.sort((a, b) => {
        const dateA = new Date(a.getAttribute('data-created'));
        const dateB = new Date(b.getAttribute('data-created'));
        return dateB - dateA;
      });
    }

    // Re-append sorted cards with animation
    cards.forEach((card, index) => {
      card.style.animation = 'none';
      setTimeout(() => {
        card.style.animation = `fadeIn 0.5s ease ${index * 0.05}s`;
      }, 10);
      grid.appendChild(card);
    });
  });
}

// Smooth Page Transitions
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '1';
});

// Add ripple effect to buttons
document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', function (e) {
    const ripple = document.createElement('span');
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    this.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  });
});

// Add ripple animation CSS
const style = document.createElement('style');
style.textContent = `
  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s ease-out;
    pointer-events: none;
  }

  @keyframes ripple-animation {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Filter by Rating
const ratingFilter = document.querySelector('.rating-filter');
if (ratingFilter) {
  ratingFilter.addEventListener('change', (e) => {
    const minRating = parseFloat(e.target.value);
    const cards = document.querySelectorAll('.provider-card');
    
    cards.forEach(card => {
      const rating = parseFloat(card.getAttribute('data-rating')) || 0;
      if (rating >= minRating) {
        card.style.display = 'block';
        card.style.animation = 'fadeIn 0.5s ease';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Filter by City
const cityFilter = document.querySelector('.city-filter');
if (cityFilter) {
  cityFilter.addEventListener('change', (e) => {
    const city = e.target.value;
    const cards = document.querySelectorAll('.provider-card');
    
    cards.forEach(card => {
      const providerCity = card.getAttribute('data-city');
      if (city === '' || providerCity === city) {
        card.style.display = 'block';
        card.style.animation = 'fadeIn 0.5s ease';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Initialize on page load
window.addEventListener('load', () => {
  // Detect location if on search page
  if (document.querySelector('.providers-grid')) {
    detectLocation();
  }
});

console.log('ServiceFinder SaaS UI loaded successfully!');
/* ============================================
   PROFILE IMAGE UTILITIES
   ============================================ */

// Profile image error handling
function handleProfileImageError(img) {
    img.onerror = null; // Prevent infinite loop
    img.src = '/static/images/default-avatar.svg';
    img.classList.add('profile-image-error');
}

// Profile image loading state
function showProfileImageLoading(container) {
    container.classList.add('profile-image-loading');
    container.innerHTML = '<div class="loading-spinner"></div>';
}

// Profile image loaded successfully
function handleProfileImageLoad(img) {
    img.classList.add('profile-image-loaded');
    img.classList.remove('profile-image-loading');
}

// Initialize profile images with error handling
function initializeProfileImages() {
    document.querySelectorAll('img[src*="uploads/"], img[src*="profile"]').forEach(img => {
        // Add error handling
        img.onerror = function() {
            handleProfileImageError(this);
        };
        
        // Add load handling
        img.onload = function() {
            handleProfileImageLoad(this);
        };
        
        // Add loading class initially
        img.classList.add('profile-image-lazy');
        
        // Check if image is already loaded
        if (img.complete && img.naturalHeight !== 0) {
            handleProfileImageLoad(img);
        }
    });
}

// Lazy load profile images
function lazyLoadProfileImages() {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('profile-image-lazy');
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Profile image upload preview
function previewProfileImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please select a valid image file (JPG, PNG)', 'error');
            input.value = '';
            return;
        }
        
        // Validate file size (2MB)
        if (file.size > 2 * 1024 * 1024) {
            showNotification('File size must be less than 2MB', 'error');
            input.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.classList.add('profile-image-loaded');
        };
        reader.readAsDataURL(file);
    }
}

// Add hover effects to profile images
function addProfileImageHoverEffects() {
    document.querySelectorAll('.profile-image-hover, .admin-profile-image, .provider-profile-image').forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = 'var(--shadow-lg)';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'var(--shadow-md)';
        });
    });
}

// Initialize profile image functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProfileImages();
    addProfileImageHoverEffects();
    
    // Initialize lazy loading if supported
    if ('IntersectionObserver' in window) {
        lazyLoadProfileImages();
    }
});

// Profile image utility functions
const ProfileImageUtils = {
    // Get default avatar URL
    getDefaultAvatarUrl: () => '/static/images/default-avatar.svg',
    
    // Check if image URL is valid
    isValidImageUrl: (url) => {
        return url && url !== 'default.png' && !url.includes('default-avatar');
    },
    
    // Generate profile image URL
    generateProfileImageUrl: (filename) => {
        if (!filename || filename === 'default.png') {
            return ProfileImageUtils.getDefaultAvatarUrl();
        }
        return `/static/uploads/${filename}`;
    },
    
    // Handle profile image click
    handleProfileImageClick: (imageElement) => {
        // Add click functionality if needed
        imageElement.style.cursor = 'pointer';
    },
    
    // Update profile image
    updateProfileImage: (element, newSrc) => {
        element.src = newSrc;
        element.onerror = function() {
            handleProfileImageError(this);
        };
    }
};

// Export for use in other scripts
window.ProfileImageUtils = ProfileImageUtils;