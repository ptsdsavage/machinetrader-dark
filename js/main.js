/* ============================================
   MachineTrader — Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---- Navbar scroll effect ----
  const navbar = document.getElementById('navbar');
  const handleScroll = () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // run once on load

  // ---- Mobile menu toggle ----
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  mobileBtn.addEventListener('click', () => {
    const isOpen = !mobileMenu.classList.contains('hidden');
    mobileMenu.classList.toggle('hidden');
    mobileBtn.classList.toggle('menu-open');
    document.body.style.overflow = isOpen ? '' : 'hidden';
  });

  // Close mobile menu on link click
  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
      mobileBtn.classList.remove('menu-open');
      document.body.style.overflow = '';
    });
  });

  // ---- Scroll reveal ----
  const revealElements = () => {
    const elements = document.querySelectorAll('.feature-card, .reveal');
    const windowHeight = window.innerHeight;

    elements.forEach(el => {
      const rect = el.getBoundingClientRect();
      const triggerPoint = windowHeight * 0.85;

      if (rect.top < triggerPoint) {
        el.classList.add('visible');
      }
    });
  };

  window.addEventListener('scroll', revealElements, { passive: true });
  // Trigger once on load
  setTimeout(revealElements, 100);

  // ---- Smooth scroll for anchor links ----
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        const navHeight = navbar.offsetHeight;
        const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ---- Stats counter animation ----
  const animateCounters = () => {
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => {
      if (counter.dataset.animated) return;

      const rect = counter.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.9) {
        counter.dataset.animated = 'true';
        const target = parseInt(counter.dataset.count);
        const duration = 2000;
        const start = performance.now();

        const tick = (now) => {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          // Ease out cubic
          const ease = 1 - Math.pow(1 - progress, 3);
          const current = Math.floor(ease * target);
          counter.textContent = current.toLocaleString() + '+';

          if (progress < 1) {
            requestAnimationFrame(tick);
          }
        };

        requestAnimationFrame(tick);
      }
    });
  };

  window.addEventListener('scroll', animateCounters, { passive: true });
  setTimeout(animateCounters, 500);

});

// ---- FAQ toggle (global function for inline onclick) ----
function toggleFaq(button) {
  const item = button.closest('.faq-item');
  const content = item.querySelector('.faq-content');
  const isActive = item.classList.contains('active');

  // Close all
  document.querySelectorAll('.faq-item').forEach(faqItem => {
    faqItem.classList.remove('active');
    const c = faqItem.querySelector('.faq-content');
    c.classList.remove('show');
    c.classList.add('hidden');
    c.style.maxHeight = '0';
    c.style.paddingBottom = '0';
  });

  // Open clicked (if it wasn't already open)
  if (!isActive) {
    item.classList.add('active');
    content.classList.remove('hidden');
    content.classList.add('show');
    content.style.maxHeight = content.scrollHeight + 'px';
    content.style.paddingBottom = '20px';
  }
}
