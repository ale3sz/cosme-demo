def update_app_and_styles():
    # Update app.js
    with open('app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    old_tab_logic = """  // =========================================================================
  // 3. TABS Y FILTRADO DEL MENÚ (DÍA / NOCHE)
  // =========================================================================
  const menuTabs = document.querySelectorAll('.menu-mode-tab');
  const dishesNight = document.querySelectorAll('.dish-night');
  const dishesDay = document.querySelectorAll('.dish-day');
  const lunchSuggester = document.getElementById('lunch-suggester-box');

  menuTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-menu-target');
      setMenuMode(target);
    });
  });

  function setMenuMode(mode) {
    menuTabs.forEach(t => {
      if (t.getAttribute('data-menu-target') === mode) {
        t.classList.add('active');
      } else {
        t.classList.remove('active');
      }
    });

    if (mode === 'day') {
      dishesNight.forEach(el => el.style.display = 'none');
      dishesDay.forEach(el => el.style.display = 'flex');
      if (lunchSuggester) lunchSuggester.style.display = 'block';
    } else {
      dishesNight.forEach(el => el.style.display = 'flex');
      dishesDay.forEach(el => el.style.display = 'none');
      if (lunchSuggester) lunchSuggester.style.display = 'none';
    }
  }

  // Inicializar menú con el tema actual
  setMenuMode(initialTheme);"""

    new_tab_logic = """  // =========================================================================
  // 3. TABS Y FILTRADO DEL MENÚ UNIFICADO (DÍA / NOCHE / CANILLAS)
  // =========================================================================
  const menuTabs = document.querySelectorAll('.menu-mode-tab');
  const dishesNight = document.querySelectorAll('.dish-night');
  const dishesDay = document.querySelectorAll('.dish-day');
  const lunchSuggester = document.getElementById('lunch-suggester-box');
  const tapsBoard = document.getElementById('canillas');
  const menuGrid = document.querySelector('.menu-grid');
  const menuFooterBar = document.querySelector('.menu-footer-bar');

  menuTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-menu-target');
      setMenuMode(target);
    });
  });

  function setMenuMode(mode) {
    menuTabs.forEach(t => {
      if (t.getAttribute('data-menu-target') === mode) {
        t.classList.add('active');
      } else {
        t.classList.remove('active');
      }
    });

    if (mode === 'taps') {
      if (tapsBoard) tapsBoard.style.display = 'block';
      if (menuGrid) menuGrid.style.display = 'none';
      if (lunchSuggester) lunchSuggester.style.display = 'none';
      if (menuFooterBar) menuFooterBar.style.display = 'none';
    } else if (mode === 'day') {
      if (tapsBoard) tapsBoard.style.display = 'none';
      if (menuGrid) menuGrid.style.display = 'grid';
      if (menuFooterBar) menuFooterBar.style.display = 'flex';
      dishesNight.forEach(el => el.style.display = 'none');
      dishesDay.forEach(el => el.style.display = 'flex');
      if (lunchSuggester) lunchSuggester.style.display = 'block';
    } else {
      // mode === 'night'
      if (tapsBoard) tapsBoard.style.display = 'none';
      if (menuGrid) menuGrid.style.display = 'grid';
      if (menuFooterBar) menuFooterBar.style.display = 'flex';
      dishesNight.forEach(el => el.style.display = 'flex');
      dishesDay.forEach(el => el.style.display = 'none');
      if (lunchSuggester) lunchSuggester.style.display = 'none';
    }
  }

  // Soporte directo para hash #canillas
  function checkHashTab() {
    if (window.location.hash === '#canillas') {
      setMenuMode('taps');
    }
  }
  window.addEventListener('hashchange', checkHashTab);
  checkHashTab();

  // Inicializar menú con el tema actual
  setMenuMode(initialTheme);"""

    if old_tab_logic in js:
        js = js.replace(old_tab_logic, new_tab_logic, 1)
        with open('app.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("app.js updated successfully!")
    else:
        print("Warning: old_tab_logic not matched exactly in app.js, checking alternate match")
        # Try regex replacement
        import re
        pattern = r'const menuTabs = document\.querySelectorAll\(\'\.menu-mode-tab\'\);[\s\S]*?setMenuMode\(initialTheme\);'
        if re.search(pattern, js):
            js = re.sub(pattern, new_tab_logic.strip(), js, count=1)
            with open('app.js', 'w', encoding='utf-8') as f:
                f.write(js)
            print("app.js updated via regex successfully!")
        else:
            print("ERROR: Could not match menuTabs section in app.js")

    # Update styles.css
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    old_css_tabs = """.menu-mode-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
}"""

    new_css_tabs = """.menu-mode-tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 32px;
}
#canillas.taps-board {
  margin-bottom: 40px;
}"""

    if old_css_tabs in css:
        css = css.replace(old_css_tabs, new_css_tabs, 1)
        with open('styles.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("styles.css updated successfully!")
    else:
        print("styles.css tabs rule not found directly, appending helper")
        css += "\n\n/* Enhanced layout helper */\n.menu-mode-tabs { flex-wrap: wrap; }\n#canillas.taps-board { margin-bottom: 40px; }\n"
        with open('styles.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("styles.css helper appended!")

if __name__ == '__main__':
    update_app_and_styles()
