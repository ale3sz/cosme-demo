import React, { useState } from 'react';

/**
 * COSME ALBERDI — LANDING PAGE COMPLETA (React + Tailwind CSS)
 * Gastrobar & Cervecería Artesanal | Boulevard Rondeau 1602, Barrio Alberdi, Rosario
 * 
 * Fidelidad 1:1 con la referencia visual:
 * - Cartel de neón doble tubular auténtico sobre acrílico con cables.
 * - Botón "EXPLORAR LAS CARTAS" en cartón kraft rasgado con fibras reales.
 * - Botones de neón rectangulares con esquinas de 8px (Reservar Mesa y Reservar en WhatsApp).
 * - Chapa enamel postal "BV. RONDEAU 1602 · BARRIO ALBERDI, ROSARIO" inclinada.
 * - Doodles laterales a mano alzada en blanco/gris (cero tonos violetas/púrpuras).
 * - Secciones completas scrolleables: Bento Grid (El Espacio), Menú (Día/Noche), Festejos, Ubicación y Footer.
 */

export default function CosmeLanding() {
  const [isNight, setIsNight] = useState(true);
  const [activeMenuTab, setActiveMenuTab] = useState('night');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleTheme = () => {
    const nextTheme = !isNight;
    setIsNight(nextTheme);
    setActiveMenuTab(nextTheme ? 'night' : 'day');
  };

  return (
    <div className={`min-h-screen relative font-sans text-neutral-100 overflow-x-hidden ${isNight ? 'bg-[#0D0E11]' : 'bg-[#181412]'}`}>
      
      {/* 1. FONDO CONTINUO DE LADRILLOS ATENUADO PARA MÁXIMA LEGIBILIDAD */}
      <div 
        className="absolute inset-0 pointer-events-none z-0 bg-repeat bg-top"
        style={{
          backgroundImage: `linear-gradient(rgba(11, 12, 15, 0.74), rgba(11, 12, 15, 0.74)), url('/assets/seamless_brick_tile.jpg')`,
          backgroundSize: '100% 100%, 720px auto',
          backgroundColor: '#0B0C0E'
        }}
      />

      {/* Grano analógico de película sutil */}
      <div 
        className="fixed inset-0 pointer-events-none z-50 opacity-[0.02]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`
        }}
      />

      {/* 2. HEADER FIJO CON TEXTURA DE PIZARRA, 5 LINKS Y BOTÓN NEÓN RECTANGULAR 8PX */}
      <header className="sticky top-0 z-40 w-full bg-[#0C0C0E]/90 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          
          {/* Marca: Isotipo Original Ámbar + Tipografía Rústica Slab-Serif */}
          <a href="#hero" className="flex items-center gap-3 group">
            <img 
              src="/assets/cosme-mascot-amber.png" 
              alt="Isotipo Cosme Alberdi" 
              className="w-10 h-12 object-contain drop-shadow-[0_0_12px_rgba(255,170,0,0.7)] group-hover:scale-105 transition-transform"
            />
            <span className="font-['Alfa_Slab_One',serif] text-xl tracking-wider text-white">
              COSME ALBERDI
            </span>
          </a>

          {/* Menú Desktop con los 5 Enlaces Exactos de la Imagen */}
          <nav className="hidden lg:flex items-center gap-7 text-sm font-medium tracking-wide text-neutral-300">
            <a href="#el-lugar" className="hover:text-white transition-colors">El Lugar</a>
            <a href="#menu" onClick={() => setActiveMenuTab('day')} className="hover:text-white transition-colors">Día &amp; Café</a>
            <a href="#menu" onClick={() => setActiveMenuTab('night')} className="hover:text-white transition-colors">Noche &amp; Birra</a>
            <a href="#festejos" className="hover:text-white transition-colors">Festejos &amp; DJ</a>
            <a href="#ubicacion" className="hover:text-white transition-colors">Ubicación</a>
          </nav>

          {/* Header Derecho: Toggle Plano con Perilla + Botón Neón Rectangular 8px */}
          <div className="flex items-center gap-4">
            
            <div className="hidden sm:flex flex-col items-center gap-1">
              <span className="text-[10px] tracking-widest uppercase font-mono text-neutral-400 font-semibold">
                MODO DÍA / NOCHE
              </span>
              <button
                onClick={toggleTheme}
                type="button"
                className="flex items-center gap-2 px-3 py-1 rounded-full border border-neutral-700 bg-neutral-900/90 hover:border-neutral-500 transition-all text-xs font-mono font-bold"
                aria-label="Cambiar entre modo día y noche"
              >
                <div className={`w-3.5 h-3.5 rounded-full transition-colors ${isNight ? 'bg-[#9E9EA8]' : 'bg-[#FFAA00]'}`} />
                <span>{isNight ? '🌙 NOCHE' : '☀️ DÍA'}</span>
              </button>
            </div>

            {/* Botón Reservar Mesa (Rectangular 8px con Tubo de Neón Rojo) */}
            <a
              href="https://wa.me/5493416802275?text=Hola%20Cosme%20Alberdi!%20Quiero%20reservar%20una%20mesa."
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:inline-flex px-5 py-2.5 rounded-lg text-xs font-bold tracking-wider uppercase text-white bg-[#0C0A0D] border-2 border-[#FF1E27] shadow-[0_0_16px_rgba(255,30,39,0.75),inset_0_0_6px_rgba(255,30,39,0.25)] hover:bg-[#180B0D] hover:shadow-[0_0_24px_rgba(255,30,39,0.95)] hover:-translate-y-0.5 transition-all"
            >
              RESERVAR MESA
            </a>

            {/* Botón Menú Móvil */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 text-neutral-300 hover:text-white"
              aria-label="Menú móvil"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Menú Móvil Desplegable */}
        {isMobileMenuOpen && (
          <div className="lg:hidden bg-neutral-950/95 border-b border-neutral-800 px-6 py-6 flex flex-col gap-4 text-center">
            <a href="#el-lugar" onClick={() => setIsMobileMenuOpen(false)} className="text-lg font-medium hover:text-red-500">El Lugar</a>
            <a href="#menu" onClick={() => { setActiveMenuTab('day'); setIsMobileMenuOpen(false); }} className="text-lg font-medium hover:text-amber-500">Día &amp; Café</a>
            <a href="#menu" onClick={() => { setActiveMenuTab('night'); setIsMobileMenuOpen(false); }} className="text-lg font-medium hover:text-red-500">Noche &amp; Birra</a>
            <a href="#festejos" onClick={() => setIsMobileMenuOpen(false)} className="text-lg font-medium hover:text-red-500">Festejos &amp; DJ</a>
            <a href="#ubicacion" onClick={() => setIsMobileMenuOpen(false)} className="text-lg font-medium hover:text-red-500">Ubicación</a>
          </div>
        )}
      </header>

      {/* 3. CONTENIDO PRINCIPAL SCROLLEABLE */}
      <main className="relative z-20">

        {/* =================================================================
            HERO SECTION — EXACTA ESTRUCTURA DE LA IMAGEN DE REFERENCIA
            ================================================================= */}
        <section id="hero" className="min-h-[calc(100vh-80px)] flex flex-col items-center justify-center text-center px-6 py-16">
          <div className="max-w-4xl mx-auto flex flex-col items-center">
            
            {/* Cartel Neón Tubular Doble Realista Aislado */}
            <div className="relative mb-6">
              <img 
                src="/assets/neon_cosme_isolated.png" 
                alt="Cartel tubular de neón rojo COSME provisto por el usuario"
                className="max-w-[580px] w-full h-auto drop-shadow-[0_0_35px_rgba(255,30,39,0.85)] drop-shadow-[0_0_14px_rgba(255,30,39,0.95)]"
              />
            </div>

            {/* Titular Principal: El Corazón de Zona Norte */}
            <h1 className="font-['Anton',sans-serif] text-4xl sm:text-5xl md:text-6xl uppercase tracking-tight text-[#F5EEE6] max-w-3xl leading-[1.08] drop-shadow-xl mt-3">
              EL CORAZÓN DE ZONA NORTE
            </h1>

            {/* Subtítulo de Autor */}
            <p className="mt-5 text-base sm:text-lg text-neutral-300 max-w-xl font-normal leading-relaxed">
              El punto de encuentro entre la calidez de un clásico de barrio y la fiesta que no duerme. Desde las 8 am al cierre.
            </p>

            {/* Fila Inferior: Chapa Enamel Postal con Margen Más Amplio y Alineación Equilibrada */}
            <div className="w-full mt-14 flex flex-col lg:flex-row items-center justify-center relative gap-6">
              
              {/* Chapa Enamel Postal con Dirección (Left Anchor) */}
              <div className="lg:absolute lg:left-0 lg:bottom-0">
                <div className="inline-flex flex-col items-start bg-[#F8F6F0] text-[#141414] px-4 py-2 rounded-md border-2 border-[#141414] shadow-[0_6px_18px_rgba(0,0,0,0.6)] transform -rotate-3 hover:rotate-0 transition-transform">
                  <div className="flex items-center gap-1.5 font-['Anton',sans-serif] text-sm tracking-wide uppercase border-b border-[#141414] pb-0.5 w-full">
                    <svg className="w-3.5 h-3.5 fill-black" viewBox="0 0 24 24">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/>
                    </svg>
                    BV. RONDEAU 1602 ·
                  </div>
                  <div className="font-['Anton',sans-serif] text-xs tracking-wider uppercase pt-0.5 text-neutral-800">
                    BARRIO ALBERDI, ROSARIO
                  </div>
                </div>
              </div>

              {/* Botones de Acción con Texturas Fieles a la Referencia */}
              <div className="flex flex-wrap items-center justify-center gap-5">
                
                {/* Botón Kraft con Recorte Rasgado Auténtico */}
                <a
                  href="#menu"
                  className="px-9 py-4 font-extrabold text-sm tracking-wider uppercase text-[#1B120B] bg-cover bg-center drop-shadow-[0_4px_10px_rgba(0,0,0,0.6)] hover:scale-105 transition-transform"
                  style={{ backgroundImage: `url('/assets/torn_kraft_btn.png')` }}
                >
                  EXPLORAR LAS CARTAS
                </a>

                {/* Botón Neón Rojo WhatsApp Rectangular 8px */}
                <a
                  href="https://wa.me/5493416802275?text=Hola%20Cosme%20Alberdi!%20Quiero%20reservar%20una%20mesa."
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-7 py-3.5 rounded-lg font-bold text-sm tracking-wider uppercase text-white bg-[#0E0C10] border-2 border-[#FF1E27] shadow-[0_0_18px_rgba(255,30,39,0.8),inset_0_0_10px_rgba(255,30,39,0.35)] hover:bg-[#1B0F10] hover:shadow-[0_0_28px_rgba(255,30,39,0.95)] hover:-translate-y-0.5 transition-all"
                >
                  RESERVAR EN WHATSAPP
                </a>

              </div>

            </div>

          </div>
        </section>

        {/* =================================================================
            SECCIÓN 1: BENTO GRID ("EL ESPACIO") — Asimétrico 4 Tarjetas
            ================================================================= */}
        <section id="el-lugar" className="py-24 max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <span className="font-mono text-xs uppercase tracking-[0.25em] text-[#FFAA00] font-bold">
              Atmósfera &amp; Arquitectura
            </span>
            <h2 className="font-['Anton',sans-serif] text-4xl sm:text-5xl uppercase tracking-wide text-white mt-2">
              El Espacio
            </h2>
            <p className="mt-3 text-neutral-400 max-w-xl mx-auto text-base">
              Cuatro rincones donde la madera curada, el hierro crudo y el neón rojo definen la mística de Alberdi.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 auto-rows-[290px]">
            
            {/* Card 1: Neón & Ladrillo (Col Span 7, Row Span 2) */}
            <article className="md:col-span-7 md:row-span-2 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-white/10 shadow-2xl transition-all duration-300 hover:scale-105 hover:z-20 hover:border-red-500/70 hover:shadow-[0_0_35px_rgba(255,30,39,0.45)] cursor-pointer">
              <img 
                src="/assets/cartel-neon-clean.jpg" 
                alt="Neón y ladrillo visto en Cosme Alberdi" 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent flex flex-col justify-end p-8">
                <span className="font-mono text-xs uppercase tracking-widest text-[#FF1E27] font-bold mb-1">01 / ÍCONO</span>
                <h3 className="font-['Anton',sans-serif] text-2xl sm:text-3xl uppercase tracking-wide text-white">
                  Neón &amp; Ladrillo
                </h3>
                <p className="text-neutral-300 text-sm mt-2 max-w-md leading-relaxed">
                  Paredes centenarias de ladrillo macizo coronadas por el fulgor carmesí de tubos de gas neón hechos a mano.
                </p>
              </div>
            </article>

            {/* Card 2: Barra de Cemento (Col Span 5, Row Span 1) */}
            <article className="md:col-span-5 md:row-span-1 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-white/10 shadow-2xl transition-all duration-300 hover:scale-105 hover:z-20 hover:border-red-500/70 hover:shadow-[0_0_35px_rgba(255,30,39,0.45)] cursor-pointer">
              <img 
                src="/assets/barra-edison.jpg" 
                alt="Barra de cemento alisado con canillas de cerveza" 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent flex flex-col justify-end p-6">
                <span className="font-mono text-xs uppercase tracking-widest text-[#FFAA00] font-bold mb-1">02 / CANILLAS</span>
                <h3 className="font-['Anton',sans-serif] text-2xl uppercase tracking-wide text-white">
                  Barra de Cemento
                </h3>
                <p className="text-neutral-300 text-xs sm:text-sm mt-1 leading-relaxed">
                  Bloque macizo de hormigón pulido, lámparas Edison y 12 canillas artesanales tiradas al instante.
                </p>
              </div>
            </article>

            {/* Card 3: Salón Terracota (Col Span 5, Row Span 1) */}
            <article className="md:col-span-5 md:row-span-1 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-white/10 shadow-2xl transition-all duration-300 hover:scale-105 hover:z-20 hover:border-red-500/70 hover:shadow-[0_0_35px_rgba(255,30,39,0.45)] cursor-pointer">
              <img 
                src="/assets/salon-dia-tolix.jpg" 
                alt="Salón terracota cálido de día con mesas de madera" 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent flex flex-col justify-end p-6">
                <span className="font-mono text-xs uppercase tracking-widest text-[#D5C2AA] font-bold mb-1">03 / CALIDEZ</span>
                <h3 className="font-['Anton',sans-serif] text-2xl uppercase tracking-wide text-white">
                  Salón Terracota
                </h3>
                <p className="text-neutral-300 text-xs sm:text-sm mt-1 leading-relaxed">
                  Luz natural matutina, sillas Tolix y mesas de petiribí para brunchear sin apuro entre amigos.
                </p>
              </div>
            </article>

            {/* Card 4: Mural Doodle (Col Span 12, Row Span 1) */}
            <article className="md:col-span-12 md:row-span-1 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-white/10 shadow-2xl transition-all duration-300 hover:scale-105 hover:z-20 hover:border-red-500/70 hover:shadow-[0_0_35px_rgba(255,30,39,0.45)] cursor-pointer">
              <div 
                className="absolute inset-0 opacity-25 mix-blend-screen bg-repeat-x bg-contain"
                style={{ backgroundImage: `url('/assets/doodles-left.png')` }}
              />
              <img 
                src="/assets/cosme-mascot-amber.png" 
                alt="Isotipo Cosme Alberdi" 
                className="absolute right-12 top-1/2 -translate-y-1/2 h-3/4 object-contain drop-shadow-[0_0_20px_rgba(255,170,0,0.6)]"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent flex flex-col justify-end p-8">
                <span className="font-mono text-xs uppercase tracking-widest text-[#FF1E27] font-bold mb-1">04 / IDENTIDAD</span>
                <h3 className="font-['Anton',sans-serif] text-2xl sm:text-3xl uppercase tracking-wide text-white">
                  Mural Doodle
                </h3>
                <p className="text-neutral-300 text-sm mt-1 max-w-2xl leading-relaxed">
                  Trazos a mano alzada de street art que narran la historia del barrio, la cerveza de autor y el espíritu libre de Cosme.
                </p>
              </div>
            </article>

          </div>
        </section>

        {/* =================================================================
            SECCIÓN 2: MENÚ (TABS INTERACTIVAS DÍA & NOCHE)
            ================================================================= */}
        <section id="menu" className="py-24 max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <span className="font-mono text-xs uppercase tracking-[0.25em] text-[#FF1E27] font-bold">
              Gastronomía &amp; Canillas
            </span>
            <h2 className="font-['Anton',sans-serif] text-4xl sm:text-5xl uppercase tracking-wide text-white mt-2">
              Nuestras Cartas
            </h2>
            <p className="mt-3 text-neutral-400 max-w-xl mx-auto text-base">
              De mañana cafetería de especialidad y brunch de autor; de noche smash burgers, milanesas en torre y birra artesanal.
            </p>
          </div>

          {/* Selector de Tabs Centrado */}
          <div className="flex justify-center gap-4 mb-12">
            <button
              onClick={() => setActiveMenuTab('day')}
              className={`px-7 py-3.5 rounded-full font-bold text-sm uppercase tracking-wider transition-all duration-300 ${
                activeMenuTab === 'day'
                  ? 'bg-[#FAF5EE] text-[#241A14] border-2 border-[#D5C2AA] shadow-[0_4px_20px_rgba(201,178,153,0.5)] scale-105'
                  : 'bg-neutral-900/80 text-neutral-400 border border-neutral-700 hover:text-white'
              }`}
            >
              ☀️ Menú de Día
            </button>

            <button
              onClick={() => setActiveMenuTab('night')}
              className={`px-7 py-3.5 rounded-full font-bold text-sm uppercase tracking-wider transition-all duration-300 ${
                activeMenuTab === 'night'
                  ? 'bg-[#181113] text-white border-2 border-[#FF1E27] shadow-[0_0_25px_rgba(255,30,39,0.5)] scale-105'
                  : 'bg-neutral-900/80 text-neutral-400 border border-neutral-700 hover:text-white'
              }`}
            >
              🌙 Menú de Noche
            </button>
          </div>

          {/* Grilla Día extraída de Google Maps (Con más aire y títulos generosos) */}
          {activeMenuTab === 'day' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <article className="bg-[#FAF5EE] text-[#241A14] border border-[#D5C2AA]/50 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:-translate-y-1.5 hover:shadow-2xl transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#8F5227] font-bold">Clásico de Mañana</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-[#1A120D] leading-tight">Infusión + Medialunas</h4>
                  <p className="text-sm text-[#5C4B40] mt-3 leading-relaxed">
                    Café o infusión de 240cc acompañado de dos medialunas de manteca recién horneadas, suaves y esponjosas.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#9E5B2D]">$6.000</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-[#E8DDD0] text-[#7A451F]">Promo 1</span>
                </div>
              </article>

              <article className="bg-[#FAF5EE] text-[#241A14] border border-[#D5C2AA]/50 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:-translate-y-1.5 hover:shadow-2xl transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#8F5227] font-bold">Brunch de Especialidad</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-[#1A120D] leading-tight">Tostada Avocado</h4>
                  <p className="text-sm text-[#5C4B40] mt-3 leading-relaxed">
                    Palta hass fresca, huevo poché cremoso y mix de semillas tostadas sobre rodaja de pan de campo de masa madre.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#9E5B2D]">$12.000</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-[#E8DDD0] text-[#7A451F]">Favorito</span>
                </div>
              </article>

              <article className="bg-[#FAF5EE] text-[#241A14] border border-[#D5C2AA]/50 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:-translate-y-1.5 hover:shadow-2xl transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#8F5227] font-bold">Especial de la Casa</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-[#1A120D] leading-tight">Tostado en Pan de Chipá</h4>
                  <p className="text-sm text-[#5C4B40] mt-3 leading-relaxed">
                    Crujiente tostado horneado en masa de chipá con abundante jamón cocido y queso muzzarella derretido.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#9E5B2D]">$10.800</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-[#E8DDD0] text-[#7A451F]">Recomendado</span>
                </div>
              </article>

              <article className="bg-[#FAF5EE] text-[#241A14] border border-[#D5C2AA]/50 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:-translate-y-1.5 hover:shadow-2xl transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#8F5227] font-bold">Pastelería &amp; Dulce</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-[#1A120D] leading-tight">Torta Matilda / Rogel</h4>
                  <p className="text-sm text-[#5C4B40] mt-3 leading-relaxed">
                    Porciones individuales de pastelería: Matilda húmeda de puro chocolate, auténtico Rogel con dulce de leche o Cheesecake.
                  </p>
                </div>
                <span className="font-mono text-lg font-bold text-[#9E5B2D] mt-8 block">$9.900</span>
              </article>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Tarjetas de Noche con fondo zinc-900/94, borde sutil y hover neón */}
              <article className="bg-zinc-900/94 backdrop-blur-md text-white border border-white/10 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:border-red-500/60 hover:shadow-[0_0_20px_rgba(255,30,39,0.35)] hover:-translate-y-1.5 transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#FF1E27] font-bold">Burger Insignia</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-white leading-tight">Cosme Burger Doble</h4>
                  <p className="text-sm text-neutral-300 mt-3 leading-relaxed">
                    Doble blend de carne vacuna 110g, cebolla crispy, doble panceta crocante y doble cheddar en pan Brioche con papas.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#FF1E27]">$22.800</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-red-950/80 text-red-300 border border-red-500/30">La Estrella</span>
                </div>
              </article>

              <article className="bg-zinc-900/94 backdrop-blur-md text-white border border-white/10 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:border-red-500/60 hover:shadow-[0_0_20px_rgba(255,30,39,0.35)] hover:-translate-y-1.5 transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#FF1E27] font-bold">Para Compartir</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-white leading-tight">Pizzanesa Del 10 (Para 2)</h4>
                  <p className="text-sm text-neutral-300 mt-3 leading-relaxed">
                    La reina de Alberdi: milanesa suprema de ternera napolitana a caballo con dos huevos de campo fritos y guarnición de papas.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#FF1E27]">$66.000</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-red-950/80 text-red-300 border border-red-500/30">Comen 2</span>
                </div>
              </article>

              <article className="bg-zinc-900/94 backdrop-blur-md text-white border border-white/10 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:border-red-500/60 hover:shadow-[0_0_20px_rgba(255,30,39,0.35)] hover:-translate-y-1.5 transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#FFAA00] font-bold">Cervecería &amp; Barra</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-white leading-tight">Birra Tirada &amp; Gin Frutos</h4>
                  <p className="text-sm text-neutral-300 mt-3 leading-relaxed">
                    Canillas frías de cerveza artesanal (IPA, Golden, Irish Red) o trago de autor con Gin nacional, tónica y frutos rojos.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#FFAA00]">Canillas Frías</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-amber-950/80 text-amber-300 border border-amber-500/30">12 Taps</span>
                </div>
              </article>

              <article className="bg-zinc-900/94 backdrop-blur-md text-white border border-white/10 rounded-2xl p-8 shadow-xl flex flex-col justify-between hover:border-red-500/60 hover:shadow-[0_0_20px_rgba(255,30,39,0.35)] hover:-translate-y-1.5 transition-all duration-300">
                <div>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#FF1E27] font-bold">Tapeo &amp; Minutas</span>
                  <h4 className="font-['Anton',sans-serif] text-2xl tracking-wide uppercase mt-2 text-white leading-tight">Ribs Barbacoa / Tabla Previa</h4>
                  <p className="text-sm text-neutral-300 mt-3 leading-relaxed">
                    Costillas de cerdo a la barbacoa con guarnición, o tabla con muzzarellitas, rabas crocantes, empanaditas y nachos cheddar.
                  </p>
                </div>
                <div className="flex items-center justify-between mt-8">
                  <span className="font-mono text-lg font-bold text-[#FF1E27]">$24.000</span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-red-950/80 text-red-300 border border-red-500/30">Tapeo</span>
                </div>
              </article>
            </div>
          )}
              </article>
            </div>
          )}
        </section>

        {/* =================================================================
            SECCIÓN 3: FESTEJOS & DJ
            ================================================================= */}
        <section id="festejos" className="py-24 max-w-7xl mx-auto px-6">
          <div className="bg-[#0E0F14]/90 border border-red-500/25 rounded-3xl p-8 sm:p-12 shadow-2xl backdrop-blur-md grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-[#FFAA00]/10 border border-[#FFAA00]/40 text-[#FFAA00] px-4 py-2 rounded-full font-mono text-xs font-bold mb-6">
                🎉 Cumpleaños &amp; Eventos Privados
              </div>
              <h2 className="font-['Anton',sans-serif] text-3xl sm:text-4xl uppercase tracking-wide text-white leading-tight">
                Festejos &amp; DJ en Vivo
              </h2>
              <p className="mt-4 text-neutral-300 text-base leading-relaxed">
                Cumples, recibidas, despedidas o juntadas de amigos. Tenemos promociones especiales de pizza libre, canillas abiertas y cabina con DJ en vivo para que tu noche sea legendaria.
              </p>
              <div className="mt-8">
                <a
                  href="https://wa.me/5493416802275?text=Hola%20Cosme!%20Quiero%20consultar%20por%20promos%20de%20cumplea%C3%B1os."
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-7 py-3.5 rounded-lg font-bold text-xs uppercase tracking-wider text-white bg-[#0E0C10] border-2 border-[#FF1E27] shadow-[0_0_18px_rgba(255,30,39,0.8)] hover:bg-[#1B0F10] transition-all"
                >
                  Consultar Promos Cumpleaños
                </a>
              </div>
            </div>
            <div className="w-full h-72 rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
              <img src="/assets/brindis-cerveza-noche.jpg" alt="Festejos en Cosme" className="w-full h-full object-cover" />
            </div>
          </div>
        </section>

        {/* =================================================================
            SECCIÓN 4: UBICACIÓN & HORARIOS
            ================================================================= */}
        <section id="ubicacion" className="py-24 max-w-7xl mx-auto px-6">
          <div className="bg-[#121319]/85 border border-white/10 rounded-3xl p-8 sm:p-12 shadow-2xl backdrop-blur-md grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-[#FF1E27]/15 border border-[#FF1E27]/40 text-[#FF555B] px-4 py-2 rounded-full font-mono text-xs font-bold mb-6">
                📍 Boulevard Rondeau 1602, Barrio Alberdi, Rosario
              </div>

              <h2 className="font-['Anton',sans-serif] text-3xl sm:text-4xl uppercase tracking-wide text-white leading-tight">
                En el corazón de Zona Norte
              </h2>

              <p className="mt-4 text-neutral-300 text-base leading-relaxed">
                Fácil acceso, estacionamiento cómodo sobre el bulevar y la mejor esquina iluminada para tus tardes de café y tus noches de cerveza y amigos.
              </p>

              <div className="flex items-center gap-3.5 bg-white/[0.04] border border-[#FFAA00]/30 rounded-xl px-4 py-3 my-5">
                <div className="bg-[#FFAA00]/15 border border-[#FFAA00] rounded-lg px-2.5 py-1 font-mono font-extrabold text-base text-[#FFE082] flex items-center gap-1">
                  <span>★</span><span>4.5</span>
                </div>
                <div className="text-xs sm:text-sm text-neutral-300">
                  <strong className="text-white block font-medium">+5.600 opiniones en Google Maps</strong>
                  <span>"Comida abundante, carnes a la parrilla y excelentes birras tiradas"</span>
                </div>
              </div>

              <div className="mt-6 flex flex-col gap-2 font-mono text-neutral-300 text-xs sm:text-sm">
                <div className="flex justify-between border-b border-white/5 pb-1.5">
                  <span className="text-white font-sans font-semibold">Lunes a Miércoles:</span>
                  <span>08:00 — 01:00 hs</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-1.5">
                  <span className="text-white font-sans font-semibold">Jueves:</span>
                  <span>08:00 — 02:00 hs</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-1.5">
                  <span className="text-white font-sans font-semibold">Viernes:</span>
                  <span>08:00 — 02:30 hs</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-1.5">
                  <span className="text-white font-sans font-semibold">Sábados:</span>
                  <span>08:30 — 02:30 hs</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white font-sans font-semibold">Domingos:</span>
                  <span>08:30 — 01:00 hs</span>
                </div>
              </div>

              <div className="mt-8 flex flex-wrap gap-4">
                <a
                  href="https://maps.app.goo.gl/W9TCWVtSw7zirDs66"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 rounded-lg font-bold text-xs uppercase tracking-wider text-white bg-[#0E0C10] border-2 border-[#FF1E27] shadow-[0_0_15px_rgba(255,30,39,0.4)] hover:bg-[#1B0F10] transition-all"
                >
                  Ver en Google Maps
                </a>

                <a
                  href="https://wa.me/5493416802275?text=Hola%20Cosme!%20Quiero%20hacer%20una%20consulta."
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 rounded-lg font-bold text-xs uppercase tracking-wider bg-neutral-800 text-white border border-neutral-700 hover:bg-neutral-700 transition-all"
                >
                  WhatsApp Directo
                </a>
              </div>
            </div>

            <div className="w-full h-80 rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
              <iframe
                title="Mapa de Cosme Alberdi"
                width="100%"
                height="100%"
                style={{ border: 0, filter: 'contrast(1.1) brightness(0.85) invert(0.92) hue-rotate(180deg)' }}
                loading="lazy"
                allowFullScreen=""
                referrerPolicy="no-referrer-when-downgrade"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3349.539871578345!2d-60.6976602!3d-32.9099955!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95b65345791350e9%3A0x6b4998982363b821!2sBv.%20Gral.%20Rondeau%201602%2C%20S2013HGJ%20Rosario%2C%20Santa%20Fe!5e0!3m2!1ses!2sar!4v1700000000000!5m2!1ses!2sar"
              />
            </div>
          </div>
        </section>

      </main>

      {/* 4. FOOTER OSCURO CON ISOTIPO CENTRADO */}
      <footer className="relative z-20 border-t border-white/10 bg-[#090A0D] py-14 text-center">
        <div className="max-w-7xl mx-auto px-6 flex flex-col items-center gap-4">
          <img 
            src="/assets/cosme-mascot-amber.png" 
            alt="Isotipo original El Cosme" 
            className="w-14 h-16 object-contain drop-shadow-[0_0_15px_rgba(255,170,0,0.7)] hover:scale-110 transition-transform cursor-pointer"
          />
          <h3 className="font-['Alfa_Slab_One',serif] text-2xl tracking-wider text-white">
            COSME ALBERDI
          </h3>
          <p className="text-neutral-400 font-medium text-base">
            Cosme Alberdi — El corazón de Zona Norte
          </p>
          <p className="font-mono text-xs text-neutral-600 mt-2">
            &copy; 2026 Cosme Alberdi Gastrobar &amp; Cervecería. Todos los derechos reservados. Bv. Rondeau 1602, Rosario, Argentina.
          </p>
        </div>
      </footer>

    </div>
  );
}
