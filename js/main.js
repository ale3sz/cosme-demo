/* ==========================================================================
   COSME ALBERDI — MAIN INTERACTIVE ORCHESTRATOR (BURGER DEVIL EDITION)
   Theme, Menu, VHS & Quote, Fast Booking Funnel
   ========================================================================== */

import { initTheme } from './modules/theme.js';
import { initMenu } from './modules/menu.js';
import { initVhsAndQuote } from './modules/vhs-quote.js';
import { initBooking } from './modules/booking.js';

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Subsystems
  initTheme();
  initMenu();
  initVhsAndQuote();
  initBooking();

  // Mobile Drawer Menu
  const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
  const mobileDrawer = document.getElementById('mobile-drawer');

  function toggleMobileDrawer(forceOpen) {
    if (!mobileMenuBtn || !mobileDrawer) return;
    const isOpen =
      typeof forceOpen === 'boolean'
        ? forceOpen
        : !mobileDrawer.classList.contains('is-open');

    mobileDrawer.classList.toggle('is-open', isOpen);
    mobileMenuBtn.setAttribute('aria-expanded', String(isOpen));
    mobileDrawer.setAttribute('aria-hidden', String(!isOpen));
  }

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', () => toggleMobileDrawer());
    mobileDrawer.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => toggleMobileDrawer(false));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileDrawer.classList.contains('is-open')) {
        toggleMobileDrawer(false);
      }
    });
  }

  // Sticky Mobile Action Bar
  const mobileBar = document.querySelector('.mobile-action-bar');
  if (mobileBar) {
    const syncMobileBar = () => {
      const isMobile = window.innerWidth <= 900;
      mobileBar.classList.toggle('is-visible', isMobile && window.scrollY > 280);
    };
    window.addEventListener('scroll', syncMobileBar, { passive: true });
    window.addEventListener('resize', syncMobileBar, { passive: true });
    syncMobileBar();
  }

  // Live Opening Schedule Pill
  const openStatusPill = document.getElementById('open-status-pill');
  if (openStatusPill) {
    try {
      const now = new Date();
      const parts = new Intl.DateTimeFormat('en-US', {
        timeZone: 'America/Argentina/Buenos_Aires',
        hour: 'numeric',
        hour12: false,
      }).formatToParts(now);

      const hour = Number(parts.find((p) => p.type === 'hour')?.value || 12);
      const isOpenNow = (hour >= 8 && hour < 24) || (hour >= 0 && hour < 3);

      openStatusPill.textContent = isOpenNow
        ? '● ABIERTO AHORA EN ROSARIO · LUN A DOM'
        : 'PRÓXIMA APERTURA 08:00 HS · BV. RONDEAU';
    } catch (_) {}
  }
});
