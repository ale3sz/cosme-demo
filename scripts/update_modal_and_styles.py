def update_app_and_styles():
    # 1. Update app.js
    with open('app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    pdf_viewer_logic = """  // =========================================================================
  // 10B. GESTIÓN DEL VISOR DE CARTA DIGITAL IN-PAGE
  // =========================================================================
  const pdfFrame = document.getElementById('pdf-frame');
  const pdfBadge = document.getElementById('modal-pdf-badge');
  const pdfDownloadLink = document.getElementById('modal-pdf-download-link');
  const pdfSwitchTabs = document.querySelectorAll('.pdf-switch-tab');

  const PDF_DOC_DATA = {
    noche: {
      title: 'Carta Salón & Noche',
      badge: 'CARTA SALÓN & NOCHE',
      previewUrl: 'https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/preview',
      downloadUrl: 'assets/docs/carta-noche.pdf',
      downloadName: 'Carta_Cosme_Alberdi_Noche.pdf'
    },
    dia: {
      title: 'Desayunos & Meriendas',
      badge: 'DESAYUNOS & MERIENDAS',
      previewUrl: 'https://drive.google.com/file/d/1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N/preview',
      downloadUrl: 'assets/docs/carta-dia.pdf',
      downloadName: 'Carta_Cosme_Alberdi_Desayunos_Meriendas.pdf'
    }
  };

  function setPdfDoc(docKey) {
    const data = PDF_DOC_DATA[docKey] || PDF_DOC_DATA.noche;
    if (pdfFrame && pdfFrame.src !== data.previewUrl) {
      pdfFrame.src = data.previewUrl;
    }
    if (pdfBadge) pdfBadge.textContent = data.badge;
    if (pdfDownloadLink) {
      pdfDownloadLink.href = data.downloadUrl;
      pdfDownloadLink.setAttribute('download', data.downloadName);
    }
    pdfSwitchTabs.forEach(tab => {
      if (tab.getAttribute('data-pdf-doc') === docKey) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
  }

  // Clicks en pestañas del visor
  pdfSwitchTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      const doc = tab.getAttribute('data-pdf-doc');
      setPdfDoc(doc);
    });
  });

  // Gatillos externos [data-open-pdf]
  document.querySelectorAll('[data-open-pdf]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const doc = trigger.getAttribute('data-open-pdf');
      setPdfDoc(doc);
      openModal(modalCarta);
    });
  });
"""

    # Check if pdf_viewer_logic already exists or where to insert it
    if '10B. GESTIÓN DEL VISOR DE CARTA' not in js:
        # Insert before modal click events
        insert_marker = "document.querySelectorAll('[data-open-modal]').forEach(trigger => {"
        if insert_marker in js:
            js = js.replace(insert_marker, pdf_viewer_logic + "\n  " + insert_marker, 1)
            print("Inserted PDF viewer logic into app.js")

    # Update modalCarta trigger to default to current theme doc
    old_carta_trigger = "if (target === 'carta') openModal(modalCarta);"
    new_carta_trigger = """if (target === 'carta') {
        const defaultDoc = (currentTheme === 'day') ? 'dia' : 'noche';
        setPdfDoc(defaultDoc);
        openModal(modalCarta);
      }"""
    if old_carta_trigger in js:
        js = js.replace(old_carta_trigger, new_carta_trigger, 1)

    # Ensure robust modal closing
    old_close_logic = """  document.querySelectorAll('.modal-backdrop, .modal-close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal-container');
      closeModal(modal);
    });
  });"""

    new_close_logic = """  document.querySelectorAll('.modal-close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const modal = btn.closest('.modal-backdrop, .modal-container');
      closeModal(modal);
    });
  });

  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        closeModal(backdrop);
      }
    });
  });"""

    if old_close_logic in js:
        js = js.replace(old_close_logic, new_close_logic, 1)

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js updated successfully!")

    # 2. Update styles.css
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    pdf_styles = """
/* =========================================================================
   VISOR IN-PAGE DE CARTA DIGITAL (SIN SALIR DEL SITIO)
   ========================================================================= */
.modal-window-pdf {
  max-width: 980px;
  width: 95vw;
  height: 90vh;
  max-height: 900px;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
  background: rgba(14, 16, 21, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.14);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(255, 30, 39, 0.1);
  border-radius: 20px;
}

html[data-theme="day"] .modal-window-pdf {
  background: rgba(255, 255, 255, 0.98);
  border-color: rgba(0, 0, 0, 0.12);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.modal-pdf-header {
  padding: 16px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--border-color);
  background: rgba(0, 0, 0, 0.35);
}

html[data-theme="day"] .modal-pdf-header {
  background: rgba(0, 0, 0, 0.03);
}

.modal-pdf-titles {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-pdf-badge {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255, 30, 39, 0.18);
  color: var(--neon-red);
  border: 1px solid rgba(255, 30, 39, 0.35);
  text-transform: uppercase;
}

html[data-theme="day"] .modal-pdf-badge {
  background: rgba(40, 128, 98, 0.15);
  color: var(--hop-green);
  border-color: rgba(40, 128, 98, 0.3);
}

.pdf-switch-tabs {
  display: flex;
  gap: 6px;
  background: rgba(255, 255, 255, 0.06);
  padding: 4px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
}

.pdf-switch-tab {
  padding: 6px 14px;
  border-radius: 7px;
  font-size: 0.82rem;
  font-weight: 600;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.pdf-switch-tab.active {
  background: var(--neon-red);
  color: #fff;
  box-shadow: 0 0 12px var(--neon-red-glow);
}

html[data-theme="day"] .pdf-switch-tab.active {
  background: var(--hop-green);
  box-shadow: 0 2px 8px rgba(40, 128, 98, 0.3);
}

.modal-pdf-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-pdf-action {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  font-family: var(--font-mono);
  padding: 7px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-pdf-action:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.modal-pdf-body {
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background: #0c0d10;
}

.pdf-embed-frame {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

.modal-pdf-footer {
  padding: 12px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-color);
  background: rgba(0, 0, 0, 0.35);
  font-size: 0.82rem;
  color: var(--text-muted);
}
"""

    if '.modal-window-pdf' not in css:
        css += "\n" + pdf_styles
        with open('styles.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("styles.css updated with PDF viewer styles successfully!")
    else:
        print("PDF styles already exist in styles.css")

if __name__ == '__main__':
    update_app_and_styles()
