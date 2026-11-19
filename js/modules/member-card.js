/* ==========================================================================
   MODULE: MEMBER CARD (ENDOWMENT EFFECT & 3D INTERACTIVE TILT)
   Psychological trigger: The user feels ownership of exclusive VIP benefits.
   ========================================================================== */

export function initMemberCard() {
  const card = document.getElementById('member-vip-card');
  const codeEl = document.getElementById('member-code-id');
  const nameEl = document.getElementById('member-holder-name');
  const activateBtn = document.getElementById('activate-member-btn');
  const statusEl = document.getElementById('member-status-pill');

  // 1. Número correlativo o aleatorio persistente
  let memberId = 'COSME-ALB-0842';
  try {
    const savedId = localStorage.getItem('cosme-member-id');
    if (savedId) {
      memberId = savedId;
    } else {
      const randNum = Math.floor(1000 + Math.random() * 9000);
      memberId = `COSME-ALB-${randNum}`;
      localStorage.setItem('cosme-member-id', memberId);
    }
  } catch (_) {}

  if (codeEl) {
    codeEl.textContent = memberId;
  }

  // 2. 3D Tilt Effect sutil
  if (card) {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -8;
      const rotateY = ((x - centerX) / centerX) * 8;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  }

  // 3. Activación de Pase de Socio
  function activateMember() {
    try {
      localStorage.setItem('cosme-member-active', 'true');
    } catch (_) {}

    if (activateBtn) {
      activateBtn.textContent = 'PASE VIP ACTIVADO \u2713';
      activateBtn.classList.add('is-active');
      activateBtn.disabled = true;
    }
    if (statusEl) {
      statusEl.textContent = 'SOCIO ACTIVO · 15% VERMOUTH & MESA PREFERENCIAL';
      statusEl.className = 'badge-pill badge-pill--live';
    }
  }

  if (activateBtn) {
    activateBtn.addEventListener('click', activateMember);

    try {
      if (localStorage.getItem('cosme-member-active') === 'true') {
        activateMember();
      }
    } catch (_) {}
  }
}
