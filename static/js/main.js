/**
 * SANSKAR PUBLIC SCHOOL — Main Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Drawer & Taskbar Menu Toggle
  const menuToggles = document.querySelectorAll('.mobile-menu-toggle, .taskbar-menu-toggle-btn');
  const navMenu = document.querySelector('.nav-menu');
  const closeBtn = document.querySelector('.mobile-close-btn');
  const backdrop = document.querySelector('.nav-menu-backdrop');

  if (navMenu) {
    const openMenu = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      navMenu.classList.add('open');
      if (backdrop) backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
      menuToggles.forEach(btn => btn.setAttribute('aria-expanded', 'true'));
    };

    const closeMenu = (e) => {
      if (e) {
        e.stopPropagation();
      }
      navMenu.classList.remove('open');
      if (backdrop) backdrop.classList.remove('active');
      document.body.style.overflow = '';
      menuToggles.forEach(btn => btn.setAttribute('aria-expanded', 'false'));
    };

    const toggleMenu = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      if (navMenu.classList.contains('open')) {
        closeMenu(e);
      } else {
        openMenu(e);
      }
    };

    menuToggles.forEach(btn => {
      btn.addEventListener('click', toggleMenu);
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', closeMenu);
    }

    if (backdrop) {
      backdrop.addEventListener('click', closeMenu);
      backdrop.addEventListener('touchstart', (e) => {
        closeMenu(e);
      }, { passive: true });
    }

    // Close drawer when clicking any nav link
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('open')) {
        closeMenu();
      }
    });

    // Reset on desktop resize
    window.addEventListener('resize', () => {
      if (window.innerWidth > 992 && navMenu.classList.contains('open')) {
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
