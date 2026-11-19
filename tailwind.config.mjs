/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: ['class', '[data-theme="night"]'],
  theme: {
    extend: {
      colors: {
        canvas: {
          dark: '#0B0B0D',
          light: '#F7F3EB',
        },
        surface: {
          dark: '#141418',
          darkMuted: '#1A1A22',
          light: '#FFFFFF',
          lightMuted: '#EFEAE0',
        },
        cosme: {
          red: '#FF1E27',
          redDark: '#C71018',
          amber: '#FFAA00',
          amberDark: '#D98200',
          cheddar: '#F5B727',
          hop: '#288062',
          mint: '#59BD95',
          terracotta: '#C86D51',
        },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'sans-serif'],
        brand: ['"Alfa Slab One"', '"Archivo Black"', 'cursive', 'sans-serif'],
        syne: ['"Syne"', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"VT323"', 'monospace'],
        vhs: ['"VT323"', 'monospace'],
      },
      boxShadow: {
        'neon-red': '0 0 20px rgba(255, 30, 39, 0.4), 0 0 40px rgba(255, 30, 39, 0.15)',
        'neon-amber': '0 0 20px rgba(255, 170, 0, 0.4), 0 0 40px rgba(255, 170, 0, 0.15)',
        'subtle-card': '0 4px 20px -2px rgba(0, 0, 0, 0.25)',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'flicker': 'flicker 4s infinite',
      },
      keyframes: {
        flicker: {
          '0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100%': {
            opacity: '1',
          },
          '20%, 21.999%, 63%, 63.999%, 65%, 69.999%': {
            opacity: '0.4',
          },
        },
      },
    },
  },
  plugins: [],
};
