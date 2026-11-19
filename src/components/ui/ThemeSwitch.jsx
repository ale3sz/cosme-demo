import React from 'react';
import { Moon, Sun } from 'lucide-react';

/**
 * ThemeSwitch — Switch Minimalista Shadcn UI / iOS Style
 * Micro-interacción pura con Lucide Moon y Sun, sin textos rígidos.
 */
export const ThemeSwitch = ({ isNight, onToggle }) => {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={!isNight}
      aria-label="Cambiar modo de iluminación"
      onClick={onToggle}
      className={`relative inline-flex h-7 w-13 shrink-0 cursor-pointer items-center rounded-full border transition-colors duration-300 focus:outline-none ${
        isNight
          ? 'bg-zinc-900 border-white/20'
          : 'bg-amber-100 border-amber-300'
      }`}
    >
      <span
        className={`pointer-events-none flex h-5 w-5 items-center justify-center rounded-full shadow-md transition-transform duration-300 ${
          isNight
            ? 'translate-x-1 bg-zinc-950 text-amber-400 border border-white/10'
            : 'translate-x-7 bg-white text-amber-600 border border-amber-200'
        }`}
      >
        {isNight ? (
          <Moon className="h-3 w-3" />
        ) : (
          <Sun className="h-3 w-3" />
        )}
      </span>
    </button>
  );
};

export default ThemeSwitch;
