import React, { useEffect, useState } from 'react';
import { Moon, Sun } from '../ui/Icons';

interface IndustrialSwitchProps {
  className?: string;
}

export const IndustrialSwitch: React.FC<IndustrialSwitchProps> = ({ className = '' }) => {
  const [theme, setTheme] = useState<'night' | 'day'>('night');

  useEffect(() => {
    // Check initial document theme or localStorage
    const savedTheme = localStorage.getItem('cosme-theme') as 'night' | 'day' | null;
    const currentTheme = (document.documentElement.getAttribute('data-theme') as 'night' | 'day') || savedTheme || 'night';
    setTheme(currentTheme);
    applyTheme(currentTheme);

    const handleExternalChange = (e: CustomEvent<{ theme: 'night' | 'day' }>) => {
      setTheme(e.detail.theme);
    };

    window.addEventListener('cosme-theme-change' as any, handleExternalChange);
    return () => {
      window.removeEventListener('cosme-theme-change' as any, handleExternalChange);
    };
  }, []);

  const applyTheme = (mode: 'night' | 'day') => {
    document.documentElement.setAttribute('data-theme', mode);
    localStorage.setItem('cosme-theme', mode);
    
    // Update theme-color meta for mobile browser chrome
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', mode === 'night' ? '#0B0B0D' : '#F7F3EB');
    }

    // Dispatch event to synchronize tabs or other components
    window.dispatchEvent(new CustomEvent('cosme-theme-change', { detail: { theme: mode } }));
  };

  const toggleTheme = () => {
    const nextTheme = theme === 'night' ? 'day' : 'night';
    setTheme(nextTheme);
    applyTheme(nextTheme);

    // Optional subtle audio feedback or haptic
    if ('vibrate' in navigator) {
      navigator.vibrate(25);
    }
  };

  const isNight = theme === 'night';

  return (
    <div className={`inline-flex items-center gap-3 ${className}`}>
      <button
        type="button"
        role="switch"
        aria-checked={isNight}
        aria-label="Alternar entre Modo Noche Neón y Modo Día Café"
        onClick={toggleTheme}
        className={`relative inline-flex items-center h-9 w-18 px-1 rounded-full transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-cosme-red ${
          isNight 
            ? 'bg-[#1C1D24] border border-[#333542] shadow-[0_0_15px_rgba(255,30,39,0.25)]' 
            : 'bg-[#E5DEC9] border border-[#C5BBA4] shadow-[0_0_15px_rgba(40,128,98,0.2)]'
        }`}
        style={{ width: '74px' }}
      >
        <span className="sr-only">Cambiar modo visual</span>
        
        {/* Track Icons */}
        <span className="absolute left-2 text-[#FFAA00] opacity-80 pointer-events-none">
          <Moon className="w-3.5 h-3.5 fill-current" />
        </span>
        <span className="absolute right-2 text-[#288062] opacity-80 pointer-events-none">
          <Sun className="w-3.5 h-3.5" />
        </span>

        {/* Knob */}
        <span
          className={`inline-block w-7 h-7 transform rounded-full bg-white shadow-md transition-transform duration-300 ease-out flex items-center justify-center ${
            isNight
              ? 'translate-x-0 bg-gradient-to-br from-[#2A2B35] to-[#121318] text-[#FF1E27] border border-[#444654]'
              : 'translate-x-9 bg-gradient-to-br from-[#FAF8F5] to-[#E8E2D5] text-[#288062] border border-[#C4B9A1]'
          }`}
        >
          {isNight ? (
            <Moon className="w-3.5 h-3.5 fill-current drop-shadow-[0_0_6px_#FF1E27]" />
          ) : (
            <Sun className="w-4 h-4 stroke-[2.5]" />
          )}
        </span>
      </button>

      {/* Label Badge */}
      <span className="hidden sm:inline-flex text-xs font-mono tracking-wider uppercase font-semibold text-textSecondary select-none">
        {isNight ? (
          <span className="text-[#FF4A50] flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF1E27] animate-pulse"></span>
            Noche Neón
          </span>
        ) : (
          <span className="text-[#288062] flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#288062]"></span>
            Día & Café
          </span>
        )}
      </span>
    </div>
  );
};
