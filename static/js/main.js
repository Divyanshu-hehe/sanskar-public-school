/**
 * SANSKAR PUBLIC SCHOOL — Main Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Header Navigation Dropdown Accordion
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const navDropdown = document.getElementById('mobile-nav-dropdown');

  if (menuToggle && navDropdown) {
    const openMenu = () => {
      navDropdown.classList.add('is-open');
      menuToggle.classList.add('active');
      menuToggle.setAttribute('aria-expanded', 'true');
      navDropdown.setAttribute('aria-hidden', 'false');
    };

    const closeMenu = () => {
      navDropdown.classList.remove('is-open');
      menuToggle.classList.remove('active');
      menuToggle.setAttribute('aria-expanded', 'false');
      navDropdown.setAttribute('aria-hidden', 'true');
    };

    const toggleMenu = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      if (navDropdown.classList.contains('is-open')) {
        closeMenu();
      } else {
        openMenu();
      }
    };

    menuToggle.addEventListener('click', toggleMenu);

    // Close when tapping outside the header or dropdown
    document.addEventListener('click', (e) => {
      if (!navDropdown.classList.contains('is-open')) return;
      const header = document.getElementById('site-header');
      if (header && !header.contains(e.target)) {
        closeMenu();
      }
    });

    // Close when tapping any link inside the dropdown
    navDropdown.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navDropdown.classList.contains('is-open')) {
        closeMenu();
      }
    });

    // Reset on desktop resize
    window.addEventListener('resize', () => {
      if (window.innerWidth > 992 && navDropdown.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }

  // 2. Sticky Header Effect
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  });

  // 3. Back to Top Button
  const backToTopBtn = document.querySelector('.back-to-top-btn');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 4. FAQ Accordion Interaction
  const faqItems = document.querySelectorAll('.faq-accordion-item');
  faqItems.forEach(item => {
    const trigger = item.querySelector('.faq-question-btn');
    if (trigger) {
      trigger.addEventListener('click', () => {
        const isOpen = item.classList.contains('active');
        faqItems.forEach(sib => sib.classList.remove('active'));
        if (!isOpen) {
          item.classList.add('active');
        }
      });
    }
  });

  // 5. Toast Notification System
  window.showToast = function(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    
    const iconClass = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle');
    toast.innerHTML = `
      <i class="fas ${iconClass}"></i>
      <span class="toast-msg">${message}</span>
      <button class="toast-close">&times;</button>
    `;
    
    container.appendChild(toast);
    
    const close = toast.querySelector('.toast-close');
    close.addEventListener('click', () => toast.remove());

    setTimeout(() => {
      toast.classList.add('fade-out');
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  };

  function createToastContainer() {
    const tc = document.createElement('div');
    tc.id = 'toast-container';
    tc.style.cssText = 'position:fixed;bottom:24px;left:24px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
    document.body.appendChild(tc);
    return tc;
  }
});
