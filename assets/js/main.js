/* ============================================================
   湯縁 Yu-en — main.js
   ============================================================ */

// ---- Hamburger menu ----
const toggle = document.querySelector('.nav-toggle');
const nav    = document.getElementById('site-nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
  });
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ============================================================
// FULL-PAGE SCROLL (index.html only)
// ============================================================
const fpContainer = document.getElementById('fp-container');
const fpDotsNav   = document.getElementById('fp-dots');
const siteHeader  = document.getElementById('site-header');

if (fpContainer) {
  const sections = Array.from(fpContainer.querySelectorAll('.fp-section'));
  const dots     = fpDotsNav ? Array.from(fpDotsNav.querySelectorAll('.fp-dot')) : [];
  let currentIndex = 0;

  function activateSection(index) {
    if (index === currentIndex && index !== 0) return;
    currentIndex = index;

    // Section active class
    sections.forEach((sec, i) => sec.classList.toggle('is-active', i === index));

    // Dot active state
    dots.forEach((dot, i) => dot.classList.toggle('is-active', i === index));

    // Hero section only gets transparent header; work sections (white bg) stay normal
    const isHero = index === 0;
    if (siteHeader) siteHeader.classList.toggle('is-dark', isHero);
  }

  // IntersectionObserver — detect which section is in view
  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.6) {
          const idx = sections.indexOf(entry.target);
          if (idx !== -1) activateSection(idx);
        }
      });
    },
    { root: fpContainer, threshold: 0.6 }
  );
  sections.forEach(sec => io.observe(sec));

  // Dot navigation
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      fpContainer.scrollTo({ top: i * window.innerHeight, behavior: 'smooth' });
    });
  });

  // Hero button → scroll to first work
  const heroBtn = document.getElementById('hero-btn');
  if (heroBtn) {
    heroBtn.addEventListener('click', (e) => {
      e.preventDefault();
      fpContainer.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
    });
  }

  // Keyboard navigation
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' && currentIndex < sections.length - 1) {
      fpContainer.scrollTo({ top: (currentIndex + 1) * window.innerHeight, behavior: 'smooth' });
    }
    if (e.key === 'ArrowUp' && currentIndex > 0) {
      fpContainer.scrollTo({ top: (currentIndex - 1) * window.innerHeight, behavior: 'smooth' });
    }
  });

  // Natural scroll — no wheel interception, browser handles freely

  // Init
  activateSection(0);
}

// ============================================================
// REGULAR PAGES (non-fullpage)
// ============================================================
if (!fpContainer) {
  // Header shadow on scroll
  window.addEventListener('scroll', () => {
    if (siteHeader) {
      siteHeader.style.boxShadow = window.scrollY > 10
        ? '0 2px 20px rgba(42,39,35,0.08)'
        : 'none';
    }
  }, { passive: true });

  // Scroll-in reveal animation
  const revealEls = document.querySelectorAll('.js-reveal');
  if (revealEls.length) {
    const revealObserver = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach(el => revealObserver.observe(el));
  }
}
