/* ============================================
   PREMIUM UI - INTERACTIVE FEATURES
   ============================================ */

// Dark Mode Toggle
const themeToggle = document.querySelector('.theme-toggle');
const htmlElement = document.documentElement;

// Check for saved theme preference or default to dark mode
const currentTheme = localStorage.getItem('theme') || 'dark';
if (currentTheme === 'light') {
  document.body.classList.add('light-mode');
  htmlElement.setAttribute('data-theme', 'light');
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    const theme = document.body.classList.contains('light-mode') ? 'light' : 'dark';
    localStorage.setItem('theme', theme);
    htmlElement.setAttribute('data-theme', theme);
    themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
  });

  // Set initial icon
  themeToggle.textContent = currentTheme === 'light' ? '🌙' : '☀️';
}

// 3D Tilt Effect for Provider Cards
const providerCards = document.querySelectorAll('.provider-card');

providerCards.forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;

    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'rotateX(0) rotateY(0) translateZ(0)';
  });
});

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

// Smooth Page Transitions
document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('page-transition');
});

// Sort Providers by Rating
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
    } else if (sortValue === 'rating-low') {
      cards.sort((a, b) => {
        const ratingA = parseFloat(a.getAttribute('data-rating')) || 0;
        const ratingB = parseFloat(b.getAttribute('data-rating')) || 0;
        return ratingA - ratingB;
      });
    } else if (sortValue === 'name-asc') {
      cards.sort((a, b) => {
        const nameA = a.getAttribute('data-name') || '';
        const nameB = b.getAttribute('data-name') || '';
        return nameA.localeCompare(nameB);
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

// Floating Emergency Button
const floatingBtn = document.querySelector('.floating-btn');
if (floatingBtn) {
  floatingBtn.addEventListener('click', () => {
    alert('Emergency services: Call 911 or your local emergency number');
  });
}

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

// Add ripple animation CSS dynamically
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

// Lazy load images
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('loaded');
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}

// Filter providers by category
const categoryFilter = document.querySelector('.category-filter');
if (categoryFilter) {
  categoryFilter.addEventListener('change', (e) => {
    const category = e.target.value;
    const cards = document.querySelectorAll('.provider-card');

    cards.forEach(card => {
      if (category === 'all' || card.getAttribute('data-category') === category) {
        card.style.display = 'block';
        card.style.animation = 'fadeIn 0.5s ease';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Add scroll animation for elements
const scrollElements = document.querySelectorAll('.glass-card, .provider-card, .stat-card');

const elementInView = (el, dividend = 1) => {
  const elementTop = el.getBoundingClientRect().top;
  return (
    elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
  );
};

const elementOutofView = (el) => {
  const elementTop = el.getBoundingClientRect().top;
  return elementTop > (window.innerHeight || document.documentElement.clientHeight);
};

const displayScrollElement = (element) => {
  element.classList.add('scrolled');
};

const hideScrollElement = (element) => {
  element.classList.remove('scrolled');
};

window.addEventListener('scroll', () => {
  scrollElements.forEach((element) => {
    if (elementInView(element, 1.25)) {
      displayScrollElement(element);
    } else if (elementOutofView(element)) {
      hideScrollElement(element);
    }
  });
});

// Initialize animations on page load
window.addEventListener('load', () => {
  document.body.style.opacity = '1';
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Alt + D for dark mode toggle
  if (e.altKey && e.key === 'd') {
    themeToggle?.click();
  }
});

// Prevent layout shift
document.addEventListener('DOMContentLoaded', () => {
  const html = document.documentElement;
  const scrollbarWidth = window.innerWidth - html.clientWidth;
  html.style.setProperty('--scrollbar-width', scrollbarWidth + 'px');
});

// Add loading state to forms
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', function() {
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner"></span> Loading...';
    }
  });
});

console.log('Premium UI loaded successfully!');
