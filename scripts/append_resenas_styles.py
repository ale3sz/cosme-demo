css_to_append = """
/* =========================================================================
   12. SECCIÓN RESEÑAS & PRUEBA SOCIAL (CRO & NEUROMARKETING)
   ========================================================================= */
.resenas-section {
  padding: 80px 0;
  border-top: 1px solid var(--border-color);
  background: linear-gradient(180deg, rgba(12,13,16,0.3) 0%, rgba(18,20,24,0.6) 100%);
}

html[data-theme="day"] .resenas-section {
  background: linear-gradient(180deg, rgba(245,240,230,0.4) 0%, rgba(235,228,214,0.7) 100%);
}

.resenas-summary-box {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 24px 32px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.resenas-score-group {
  display: flex;
  align-items: center;
  gap: 20px;
}

.resenas-score-big {
  font-family: var(--font-heading);
  font-size: 3.5rem;
  line-height: 1;
  color: var(--neon-amber);
  font-weight: 800;
}

.resenas-score-meta h4 {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  text-transform: uppercase;
  margin-bottom: 4px;
  color: var(--text-main);
  letter-spacing: 0.05em;
}

.resenas-score-meta p {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
}

.stars-row {
  display: flex;
  align-items: center;
  gap: 3px;
  color: #ffaa00;
  margin-bottom: 4px;
}

.resenas-metrics-strip {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.resena-metric-item {
  display: flex;
  flex-direction: column;
}

.resena-metric-val {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: var(--text-main);
  font-weight: 700;
}

.resena-metric-lbl {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.resenas-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 900px) {
  .resenas-cards-grid {
    grid-template-columns: 1fr;
  }
  .resenas-summary-box {
    flex-direction: column;
    align-items: flex-start;
  }
}

.resena-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 26px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 18px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.16);
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.resena-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 170, 0, 0.4);
}

.resena-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-family: var(--font-mono);
  font-weight: 700;
  text-transform: uppercase;
  background: rgba(255, 170, 0, 0.12);
  color: var(--neon-amber);
  border: 1px solid rgba(255, 170, 0, 0.25);
  margin-bottom: 14px;
  align-self: flex-start;
}

.resena-quote {
  font-size: 0.92rem;
  line-height: 1.6;
  color: var(--text-main);
  margin-bottom: 20px;
  font-style: normal;
}

.resena-author-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.resena-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 170, 0, 0.15);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: 800;
  color: var(--neon-amber);
  font-size: 0.95rem;
}

.resena-author-info h5 {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
}

.resena-author-info span {
  font-size: 0.75rem;
  color: var(--text-muted);
}
"""

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.resenas-section' not in css:
    with open('styles.css', 'a', encoding='utf-8') as f:
        f.write("\n" + css_to_append)
    print("styles.css updated with resenas styles!")
else:
    print("resenas styles already present.")
