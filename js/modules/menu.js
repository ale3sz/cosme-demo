/* ==========================================================================
   MODULE: MENU TABS & CARTAS OFICIALES MODAL
   ========================================================================== */

export function initMenu() {
  const tabNight = document.getElementById('tab-night');
  const tabDay = document.getElementById('tab-day');
  const panelNight = document.getElementById('panel-night');
  const panelDay = document.getElementById('panel-day');

  function activateTab(mode) {
    if (!tabNight || !tabDay || !panelNight || !panelDay) return;
    const isNight = mode === 'night';
    tabNight.setAttribute('aria-selected', String(isNight));
    tabDay.setAttribute('aria-selected', String(!isNight));
    panelNight.hidden = !isNight;
    panelDay.hidden = isNight;
  }

  if (tabNight && tabDay) {
    tabNight.addEventListener('click', () => activateTab('night'));
    tabDay.addEventListener('click', () => activateTab('day'));
  }

  document.querySelectorAll('[data-jump-tab]').forEach((link) => {
    link.addEventListener('click', () => {
      const mode = link.getAttribute('data-jump-tab');
      if (mode === 'day' || mode === 'night') {
        activateTab(mode);
      }
    });
  });

  // Modal de Cartas Oficiales
  const cartaDialog = document.getElementById('carta-dialog');
  const cartaTitle = document.getElementById('carta-dialog-title');
  const cartaBody = document.getElementById('carta-dialog-body');
  const cartaCloseBtn = document.getElementById('carta-dialog-close');
  const cartaPrintBtn = document.getElementById('carta-print-btn');

  const CARTAS_DATA = {
    salon: {
      title: 'Carta Salón Completa 2026 — Cosme Alberdi',
      categories: [
        {
          name: 'Especiales de la Casa & Comida Libre',
          items: [
            {
              title: 'Cascada de Queso Cheddar',
              desc: 'Dobles smash burgers bañadas en vivo con fuente de cheddar caliente + papas rústicas',
              price: 'Show en Mesa',
            },
            {
              title: 'Milanesa Libre en Torre',
              desc: 'Capas de milanesa napolitana con huevos fritos a caballo y papas libres (4+ pers.)',
              price: '$15.900 / pers.',
            },
            {
              title: 'Parrilla Libre Cosme',
              desc: 'Cortes seleccionados a las brasas con guarniciones para disfrutar sin límites',
              price: '$29.500 / pers.',
            },
            {
              title: 'El Carlito Rosarino de Vacío',
              desc: 'Clásico tostado rosarino relleno de vacío braseado desmenuzado y queso fundido',
              price: 'Clásico Local',
            },
            {
              title: 'Sushi Flambeado con Soplete',
              desc: 'Rolls de salmón sellados al fuego directo en la barra frente a los comensales',
              price: 'Barra Live',
            },
          ],
        },
        {
          name: 'Tablas Rústicas & Cumpleaños',
          items: [
            {
              title: 'Tabla "La Previa" & Tabla "La Fulanito"',
              desc: 'Tablas de madera rústica con variedades calientes y picada para grupos',
              price: 'Para Compartir',
            },
            {
              title: 'Cumpleaños Promo 1 (Comida Libre)',
              desc: 'Papas clásicas + Pizzas Muzza, Napo y Especial libres por persona',
              price: '$17.000 / pers.',
            },
            {
              title: 'Cumpleaños Promo 2 Full + DJ',
              desc: 'Papas + Pizzas + Sándwiches de carne libres + DJ en vivo y cotillón LED',
              price: '$21.000 / pers.',
            },
          ],
        },
      ],
    },
    desayunos: {
      title: 'Carta Desayunos, Brunch y Meriendas — Cosme Alberdi',
      categories: [
        {
          name: 'Torres & Brunch Artesanal',
          items: [
            {
              title: 'Torre de Merienda de 3 Pisos',
              desc: 'Medialunas, tostadas en pan de masa madre, pastelería artesanal y dips para compartir',
              price: 'Para 2 / 3',
            },
            {
              title: 'Bowl Saludable de Yogur Griego',
              desc: 'Yogur griego natural con frutos rojos de estación, granola artesanal y semillas de chía',
              price: 'Día & Salud',
            },
            {
              title: 'Tostón de Palta & Chipás Tostados',
              desc: 'Pan de campo con palta pisada + porción de chipás dorados al momento',
              price: '08:00 hs+',
            },
          ],
        },
        {
          name: 'Cafetería de Especialidad',
          items: [
            {
              title: 'Espresso Tonic / Iced Caramel Macchiato',
              desc: 'Extracción de especialidad fría sobre hielo cristalino o tónica cítrica',
              price: 'Especialidad',
            },
            {
              title: 'Flat White en Cerámica Gruesa',
              desc: 'Doble espresso equilibrado con microespuma sedosa y latte art',
              price: 'Clásico Barra',
            },
          ],
        },
      ],
    },
  };

  function openCartaModal(key) {
    const data = CARTAS_DATA[key];
    if (!data || !cartaDialog || !cartaTitle || !cartaBody) return;

    cartaTitle.textContent = data.title;
    cartaBody.innerHTML = data.categories
      .map(
        (cat) => `
      <div class="dialog-category">
        <h4>${cat.name}</h4>
        <ul class="dialog-items">
          ${cat.items
            .map(
              (item) => `
            <li>
              <div>
                <strong>${item.title}</strong>
                <span style="display: block; font-size: 0.85rem; color: var(--text-secondary);">${item.desc}</span>
              </div>
              <strong class="tabular-nums" style="color: var(--neon-amber);">${item.price}</strong>
            </li>
          `
            )
            .join('')}
        </ul>
      </div>
    `
      )
      .join('');

    if (typeof cartaDialog.showModal === 'function') {
      cartaDialog.showModal();
    }
  }

  document.querySelectorAll('[data-open-carta]').forEach((btn) => {
    btn.addEventListener('click', () => {
      openCartaModal(btn.getAttribute('data-open-carta'));
    });
  });

  if (cartaCloseBtn && cartaDialog) {
    cartaCloseBtn.addEventListener('click', () => cartaDialog.close());
    cartaDialog.addEventListener('click', (e) => {
      if (e.target === cartaDialog) cartaDialog.close();
    });
  }

  if (cartaPrintBtn) {
    cartaPrintBtn.addEventListener('click', () => window.print());
  }
}
