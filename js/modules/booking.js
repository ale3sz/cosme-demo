/* ==========================================================================
   MODULE: NATIVE BOOKING FLOW (FAST & DIRECT CRO FUNNEL)
   ========================================================================== */

export function initBooking() {
  const dialog = document.getElementById('booking-dialog');
  const closeBtn = document.getElementById('booking-dialog-close');
  const openButtons = document.querySelectorAll('[data-open-booking]');

  // Step Elements
  const stepDots = document.querySelectorAll('.step-dot');
  const stepPanes = document.querySelectorAll('.booking-step-pane');
  const nextBtn = document.getElementById('booking-next-btn');
  const backBtn = document.getElementById('booking-back-btn');

  // Form Inputs
  const zoneChips = document.querySelectorAll('.zone-chip');
  const dateInput = document.getElementById('booking-date');
  const timeSelect = document.getElementById('booking-time');
  const guestsSelect = document.getElementById('booking-guests');
  const nameInput = document.getElementById('booking-name');
  const phoneInput = document.getElementById('booking-phone');

  // Confirmation Ticket Elements
  const ticketIdEl = document.getElementById('ticket-id-val');
  const ticketDateTimeEl = document.getElementById('ticket-datetime-val');
  const ticketGuestsEl = document.getElementById('ticket-guests-val');
  const ticketZoneEl = document.getElementById('ticket-zone-val');
  const ticketWaCta = document.getElementById('ticket-wa-cta');

  let currentStep = 1;
  let bookingData = {
    date: '',
    time: '21:00 hs',
    guests: '4 personas',
    zone: 'Salón Neón Central',
    name: '',
    phone: '',
  };

  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
    dateInput.min = today;
    bookingData.date = today;
  }

  function updateStepUI() {
    stepDots.forEach((dot, idx) => {
      const stepNum = idx + 1;
      dot.classList.toggle('is-active', stepNum === currentStep);
      dot.classList.toggle('is-completed', stepNum < currentStep);
    });

    stepPanes.forEach((pane) => {
      const paneStep = Number(pane.getAttribute('data-step'));
      pane.classList.toggle('is-active', paneStep === currentStep);
    });

    if (backBtn) {
      backBtn.style.visibility = currentStep === 1 || currentStep === 3 ? 'hidden' : 'visible';
    }

    if (nextBtn) {
      if (currentStep === 2) {
        nextBtn.textContent = 'Confirmar Mesa \u2192';
        nextBtn.style.display = 'inline-flex';
      } else if (currentStep === 3) {
        nextBtn.style.display = 'none';
      } else {
        nextBtn.style.display = 'inline-flex';
        nextBtn.textContent = 'Siguiente \u2192';
      }
    }
  }

  function generateTicket() {
    const randCode = Math.floor(1000 + Math.random() * 9000);
    const ticketId = `COSME-RES-${randCode}`;

    if (ticketIdEl) ticketIdEl.textContent = ticketId;
    if (ticketDateTimeEl) ticketDateTimeEl.textContent = `${bookingData.date} · ${bookingData.time}`;
    if (ticketGuestsEl) ticketGuestsEl.textContent = bookingData.guests;
    if (ticketZoneEl) ticketZoneEl.textContent = bookingData.zone;

    if (ticketWaCta) {
      const msg = `Hola Cosme Alberdi! Confirmo mi reserva (${ticketId}):
- Canilla / Mesa: ${bookingData.zone}
- Fecha y Turno: ${bookingData.date} a las ${bookingData.time}
- Personas: ${bookingData.guests}
- A nombre de: ${bookingData.name || 'Cliente Cosme'} (${bookingData.phone || 'WhatsApp'})`;

      ticketWaCta.href = `https://wa.me/5493416802275?text=${encodeURIComponent(msg)}`;
    }
  }

  function openModal() {
    if (typeof dialog.showModal === 'function') {
      currentStep = 1;
      updateStepUI();
      dialog.showModal();
    }
  }

  openButtons.forEach((btn) => btn.addEventListener('click', openModal));

  if (closeBtn && dialog) {
    closeBtn.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => {
      if (e.target === dialog) dialog.close();
    });
  }

  // Zone choice
  zoneChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      zoneChips.forEach((c) => c.classList.remove('is-selected'));
      chip.classList.add('is-selected');
      bookingData.zone = chip.getAttribute('data-zone') || 'Salón Neón Central';
    });
  });

  // Next & Back
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentStep === 1) {
        if (dateInput) bookingData.date = dateInput.value;
        if (timeSelect) bookingData.time = timeSelect.value;
        if (guestsSelect) bookingData.guests = guestsSelect.value;
        if (nameInput) bookingData.name = nameInput.value;
        if (phoneInput) bookingData.phone = phoneInput.value;
        currentStep = 2;
      } else if (currentStep === 2) {
        generateTicket();
        currentStep = 3;
      }
      updateStepUI();
    });
  }

  if (backBtn) {
    backBtn.addEventListener('click', () => {
      if (currentStep > 1) {
        currentStep -= 1;
        updateStepUI();
      }
    });
  }

  updateStepUI();
}
