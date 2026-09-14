/**
 * Emergency & Service Finder - Main JavaScript
 */

// Close alert messages
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});

/**
 * Toggle favorite service
 */
function toggleFavorite(providerId) {
    fetch(`/api/favorite/${providerId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating favorite');
    });
}

/**
 * Call emergency service
 */
function callEmergency(service) {
    fetch(`/api/emergency/${service}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                const provider = data[0];
                window.location.href = `tel:${provider.phone}`;
            } else {
                alert(`No ${service} services found in your area`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error finding emergency service');
        });
}

/**
 * Search services via API
 */
function searchServices(query, category, city) {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (category) params.append('category', category);
    if (city) params.append('city', city);

    fetch(`/api/search?${params}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

/**
 * Display search results
 */
function displaySearchResults(providers) {
    const resultsContainer = document.getElementById('search-results');
    
    if (!resultsContainer) return;

    if (providers.length === 0) {
        resultsContainer.innerHTML = '<p class="no-results">No services found</p>';
        return;
    }

    let html = `<p class="results-count">Found ${providers.length} service(s)</p>`;
    html += '<div class="services-grid">';

    providers.forEach(provider => {
        html += `
            <div class="service-card">
                <div class="service-image-placeholder">📷</div>
                <div class="service-info">
                    <h3>${provider.business_name}</h3>
                    <p class="category">${provider.category}</p>
                    <p class="address">📍 ${provider.address}</p>
                    <p class="city">${provider.city}</p>
                    <div class="rating">⭐ ${provider.rating} (${provider.reviews_count} reviews)</div>
                    <div class="status">
                        ${provider.is_available ? '<span class="badge-open">🟢 Open</span>' : '<span class="badge-closed">🔴 Closed</span>'}
                    </div>
                    <div class="service-actions">
                        <a href="/user/service/${provider.id}" class="btn-secondary">View Details</a>
                        <a href="tel:${provider.phone}" class="btn-primary">📞 Call</a>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    resultsContainer.innerHTML = html;
}

/**
 * Get user's location
 */
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                console.log(`Location: ${lat}, ${lon}`);
                // Can be used for location-based search
            },
            error => {
                console.log('Location access denied');
            }
        );
    }
}

/**
 * Format phone number
 */
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

/**
 * Validate email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number
 */
function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]{10,}$/;
    return re.test(phone);
}

/**
 * Show loading spinner
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<p>Loading...</p>';
    document.body.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Confirm action
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Real-time search
 */
const debouncedSearch = debounce(function(query) {
    if (query.length > 2) {
        searchServices(query);
    }
}, 300);

// Export functions for use in templates
window.toggleFavorite = toggleFavorite;
window.callEmergency = callEmergency;
window.searchServices = searchServices;
window.getUserLocation = getUserLocation;
window.confirmAction = confirmAction;
