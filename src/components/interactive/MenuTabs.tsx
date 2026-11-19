import React, { useState, useEffect } from 'react';
import { nightMenu, dayMenu, type MenuItem } from '../../data/menuData';
import { Utensils, Coffee, Sparkles, ArrowRight } from '../ui/Icons';

export const MenuTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'night' | 'day'>('night');

  useEffect(() => {
    const handleThemeChange = (e: any) => {
      if (e.detail?.theme) {
        setActiveTab(e.detail.theme);
      }
    };
    window.addEventListener('cosme-theme-change', handleThemeChange);
    return () => window.removeEventListener('cosme-theme-change', handleThemeChange);
  }, []);

  const items = activeTab === 'night' ? nightMenu : dayMenu;

  return (
    <div className="w-full">
      {/* Tab Switcher Buttons */}
      <div 
        role="tablist" 
        aria-label="Seleccionar propuesta gastronómica" 
        className="flex flex-col sm:flex-row items-center justify-center gap-3 p-1.5 rounded-2xl bg-surface-card border border-surface-border max-w-xl mx-auto mb-10 shadow-lg"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'night'}
          id="tab-night"
          aria-controls="panel-menu"
          onClick={() => setActiveTab('night')}
          className={`w-full sm:w-1/2 flex items-center justify-center gap-2.5 py-3 px-5 rounded-xl font-display text-sm tracking-wide font-bold transition-all duration-300 ${
            activeTab === 'night'
              ? 'bg-[#FF1E27] text-white shadow-[0_0_20px_rgba(255,30,39,0.4)] scale-[1.02]'
              : 'text-textSecondary hover:text-textPrimary hover:bg-white/5'
          }`}
        >
          <Utensils className="w-4 h-4" />
          <span>Noche · Food Porn & Birra</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'day'}
          id="tab-day"
          aria-controls="panel-menu"
          onClick={() => setActiveTab('day')}
          className={`w-full sm:w-1/2 flex items-center justify-center gap-2.5 py-3 px-5 rounded-xl font-display text-sm tracking-wide font-bold transition-all duration-300 ${
            activeTab === 'day'
              ? 'bg-[#288062] text-white shadow-[0_0_20px_rgba(40,128,98,0.35)] scale-[1.02]'
              : 'text-textSecondary hover:text-textPrimary hover:bg-white/5'
          }`}
        >
          <Coffee className="w-4 h-4" />
          <span>Día · Cafetería & Brunch</span>
        </button>
      </div>

      {/* Menu Cards Grid */}
      <div 
        id="panel-menu"
        role="tabpanel"
        aria-labelledby={activeTab === 'night' ? 'tab-night' : 'tab-day'}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {items.map((dish) => (
          <article
            key={dish.id}
            className={`group rounded-2xl bg-surface-card border border-surface-border overflow-hidden flex flex-col transition-all duration-300 hover:-translate-y-1 hover:border-[#FF1E27]/40 hover:shadow-2xl ${
              dish.isWide ? 'md:col-span-2 lg:col-span-1' : ''
            }`}
          >
            {/* Dish Image Container */}
            {dish.image && (
              <div className="relative aspect-[16/10] overflow-hidden bg-black/40">
                <img
                  src={dish.image}
                  alt={dish.alt || dish.title}
                  loading="lazy"
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  width={600}
                  height={375}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
                
                {/* Badge Overlay */}
                <div className="absolute top-3 left-3">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider backdrop-blur-md bg-black/70 text-white border border-white/10">
                    <Sparkles className="w-3 h-3 text-[#FFAA00]" />
                    {dish.badge}
                  </span>
                </div>

                {dish.price && (
                  <div className="absolute bottom-3 right-3">
                    <span className="inline-block px-3 py-1 rounded-lg text-sm font-display font-extrabold bg-[#FF1E27] text-white shadow-md">
                      {dish.price}
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* Content */}
            <div className="p-6 flex-1 flex flex-col justify-between">
              <div>
                <h3 className="font-display text-xl font-bold mb-2 group-hover:text-[#FF1E27] transition-colors">
                  {dish.title}
                </h3>
                <p className="text-textSecondary text-sm leading-relaxed mb-4">
                  {dish.description}
                </p>

                {/* Bullet details */}
                <ul className="space-y-1.5 mb-6">
                  {dish.bullets.map((bullet, idx) => (
                    <li key={idx} className="flex items-center gap-2 text-xs text-textSecondary/90 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#FFAA00]"></span>
                      {bullet}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Action Link to WhatsApp with custom item query */}
              <a
                href={`https://wa.me/5493416802275?text=${encodeURIComponent(
                  `Hola Cosme Alberdi! Quiero consultar por ${dish.title} para mi visita.`
                )}`}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-auto inline-flex items-center justify-between w-full py-2.5 px-4 rounded-xl text-xs font-bold uppercase tracking-wider text-textPrimary bg-white/5 hover:bg-[#FF1E27] hover:text-white transition-all duration-200 border border-white/5 hover:border-transparent group/btn"
              >
                <span>Pedir o consultar</span>
                <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover/btn:translate-x-1" />
              </a>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};
