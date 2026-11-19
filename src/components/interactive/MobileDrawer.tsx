import React, { useState, useEffect } from 'react';
import { Menu, X, MessageCircle, MapPin, Sparkles, Utensils, Disc3 } from '../ui/Icons';
import { IndustrialSwitch } from './IndustrialSwitch';

export const MobileDrawer: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  const navLinks = [
    { label: 'Entradas & Links Oficiales', href: '#accesos-rapidos', icon: Sparkles },
    { label: 'El Espacio', href: '#el-lugar', icon: Sparkles },
    { label: 'Carta Día & Noche', href: '#menu-interactivo', icon: Utensils },
    { label: 'Cumpleaños & VHS 90s', href: '#festejos-dj', icon: Disc3 },
    { label: 'Cartas en Drive & PDF', href: '#cartas-pdf', icon: Utensils },
    { label: 'Ubicación & Horarios', href: '#ubicacion', icon: MapPin },
  ];

  return (
    <div className="md:hidden">
      <button
        type="button"
        aria-label={isOpen ? 'Cerrar menú' : 'Abrir menú'}
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
        className="p-2.5 rounded-xl bg-surface-card border border-surface-border text-textPrimary hover:bg-white/10 transition-colors"
      >
        {isOpen ? <X className="w-5 h-5 text-[#FF1E27]" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-md z-40 transition-opacity"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-[85%] max-w-sm bg-surface-card border-l border-surface-border z-50 p-6 flex flex-col justify-between transform transition-transform duration-300 ease-in-out shadow-2xl ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div>
          {/* Drawer Header */}
          <div className="flex items-center justify-between pb-6 border-b border-surface-border mb-6">
            <span className="font-brand text-lg font-black tracking-wider text-cosme-red">
              COSME ALBERDI
            </span>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="p-2 rounded-xl text-textSecondary hover:text-white hover:bg-white/10"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Theme switcher inside mobile menu */}
          <div className="mb-6 p-4 rounded-2xl bg-black/20 border border-surface-border flex items-center justify-between">
            <span className="text-xs font-mono font-bold uppercase text-textSecondary">
              Ambiente Visual
            </span>
            <IndustrialSwitch />
          </div>

          {/* Nav Links */}
          <nav className="space-y-2">
            {navLinks.map((item) => {
              const Icon = item.icon;
              return (
                <a
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-3.5 py-3 px-4 rounded-xl text-base font-display font-bold text-textPrimary hover:bg-[#FF1E27]/10 hover:text-[#FF1E27] transition-all"
                >
                  <Icon className="w-4 h-4 text-cosme-red" />
                  <span>{item.label}</span>
                </a>
              );
            })}
          </nav>
        </div>

        {/* Bottom Drawer Actions */}
        <div className="pt-6 border-t border-surface-border space-y-3">
          <a
            href="https://wa.me/5493416802275?text=Hola%20Cosme%20Alberdi!%20Quiero%20reservar%20una%20mesa."
            target="_blank"
            rel="noopener noreferrer"
            className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-sm font-display font-extrabold uppercase tracking-wider text-white bg-[#FF1E27] shadow-[0_0_20px_rgba(255,30,39,0.4)]"
          >
            <MessageCircle className="w-4 h-4" />
            <span>Reservar por WhatsApp</span>
          </a>
          <p className="text-center text-[11px] font-mono text-textSecondary">
            Bv. Rondeau 1602 · Barrio Alberdi, Rosario
          </p>
        </div>
      </div>
    </div>
  );
};
