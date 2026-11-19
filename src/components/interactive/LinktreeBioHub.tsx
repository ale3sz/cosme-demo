import React from 'react';
import { Ticket, FileText, MessageCircle, Instagram, ExternalLink, Sparkles, Flame, Eye, Download, Folder } from '../ui/Icons';
import { openPdfModal } from './PdfModal';

export const LinktreeBioHub: React.FC = () => {
  return (
    <section id="bio-hub" className="scroll-mt-24 py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
      {/* Header Stamp */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-bold uppercase bg-cosme-red/10 text-cosme-red border border-cosme-red/20 mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          Hub de Enlaces Oficiales (Reemplazo Linktree)
        </div>
        <h2 className="font-display text-2xl sm:text-4xl font-black uppercase text-textPrimary tracking-tight">
          Todos los Accesos en un Solo Lugar
        </h2>
        <p className="text-textSecondary text-xs sm:text-sm max-w-md mx-auto mt-1">
          Comprá entradas para las próximas fiestas, mirá las cartas completas en PDF o reservá tu mesa por WhatsApp sin salir de acá.
        </p>
      </div>

      {/* Stack of Cards */}
      <div className="space-y-4">
        {/* 1. ENTRADAS EVENTOS (Primary conversion target) */}
        <div className="relative p-5 sm:p-6 rounded-3xl bg-gradient-to-r from-[#2B1015] via-surface-card to-[#1E110A] border-2 border-cosme-red shadow-[0_0_35px_rgba(255,30,39,0.3)] transition-all duration-300 hover:shadow-[0_0_50px_rgba(255,30,39,0.5)]">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start sm:items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-cosme-red/20 border border-cosme-red/50 flex items-center justify-center text-cosme-red shrink-0 shadow-lg">
                <Ticket className="w-7 h-7" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-1">
                  <span className="font-display text-lg sm:text-xl font-black text-white">
                    ENTRADAS EVENTOS & FIESTAS
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-cosme-red text-white animate-pulse">
                    En Venta Online
                  </span>
                </div>
                <p className="text-xs sm:text-sm text-[#FFAA00] font-bold flex items-center gap-1.5">
                  <Flame className="w-4 h-4 shrink-0 text-cosme-red" />
                  <span>Barley Fest en Cosme · Domingo 22/11 (Víspera de Feriado)</span>
                </p>
                <span className="block text-[11px] text-textSecondary font-mono mt-0.5">
                  Ticketera oficial: compras.evento-simple.com/cosme
                </span>
              </div>
            </div>

            <a
              href="https://compras.evento-simple.com/cosme"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl font-display font-extrabold text-xs uppercase tracking-wider text-white bg-cosme-red hover:bg-cosme-redDark shadow-[0_0_20px_rgba(255,30,39,0.4)] transition-all shrink-0 hover:scale-105 active:scale-95 text-center"
            >
              <span>Comprar Entradas</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>

        {/* 2. CARTA GENERAL, NOCHE & SALÓN (PDF OFICIAL) */}
        <div className="p-5 sm:p-6 rounded-3xl bg-surface-card border border-surface-border hover:border-cosme-red/50 shadow-xl transition-all duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start sm:items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-cosme-red/15 border border-cosme-red/30 flex items-center justify-center text-cosme-red shrink-0">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-1">
                  <h3 className="font-display text-base sm:text-lg font-black text-textPrimary">
                    CARTA GENERAL, NOCHE & SALÓN
                  </h3>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-cosme-red/10 text-cosme-red border border-cosme-red/20">
                    PDF Oficial 2026
                  </span>
                </div>
                <p className="text-xs text-textSecondary">
                  Parrilla libre, smash burgers bañadas en cheddar caliente, Carlitos de vacío, tablas y 12 canillas artesanales.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto pt-2 sm:pt-0">
              <button
                type="button"
                onClick={() => openPdfModal('noche')}
                className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-xs font-display font-bold uppercase tracking-wider text-white bg-cosme-red hover:bg-cosme-redDark transition-all shadow-md"
              >
                <Eye className="w-4 h-4" />
                <span>Ver Carta PDF</span>
              </button>

              <a
                href="https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/view?usp=sharing"
                target="_blank"
                rel="noopener noreferrer"
                title="Abrir en Google Drive"
                className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-textSecondary hover:text-white border border-white/10 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>

        {/* 3. DESAYUNOS, CAFETERÍA & MERIENDAS (PDF OFICIAL) */}
        <div className="p-5 sm:p-6 rounded-3xl bg-surface-card border border-surface-border hover:border-cosme-hop/50 shadow-xl transition-all duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start sm:items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-cosme-hop/15 border border-cosme-hop/30 flex items-center justify-center text-cosme-hop shrink-0">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-1">
                  <h3 className="font-display text-base sm:text-lg font-black text-textPrimary">
                    CARTA DE DESAYUNOS & MERIENDAS
                  </h3>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-cosme-hop/10 text-cosme-hop border border-cosme-hop/20">
                    PDF Oficial Diurno
                  </span>
                </div>
                <p className="text-xs text-textSecondary">
                  Torres de merienda de 3 pisos, café de especialidad, tostones de masa madre, pastelería artesanal y chipás calientes.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto pt-2 sm:pt-0">
              <button
                type="button"
                onClick={() => openPdfModal('dia')}
                className="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-xs font-display font-bold uppercase tracking-wider text-white bg-cosme-hop hover:bg-emerald-800 transition-all shadow-md"
              >
                <Eye className="w-4 h-4" />
                <span>Ver Carta PDF</span>
              </button>

              <a
                href="https://drive.google.com/file/d/1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N/view?usp=sharing"
                target="_blank"
                rel="noopener noreferrer"
                title="Abrir en Google Drive"
                className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-textSecondary hover:text-white border border-white/10 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>

        {/* 4. WHATSAPP RESERVAS & CARPETA GOOGLE DRIVE */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* WhatsApp */}
          <a
            href="https://wa.me/5493416802275?text=Hola%20Cosme%20Alberdi!%20Vengo%20desde%20su%20web%20para%20hacer%20una%20reserva."
            target="_blank"
            rel="noopener noreferrer"
            className="group p-5 rounded-3xl bg-surface-card border border-surface-border hover:border-[#25D366]/60 shadow-lg transition-all duration-300 hover:scale-[1.01]"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-[#25D366]/15 border border-[#25D366]/30 flex items-center justify-center text-[#25D366]">
                <MessageCircle className="w-5 h-5" />
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-[#25D366]/20 text-[#25D366]">
                WhatsApp Oficial
              </span>
            </div>
            <h4 className="font-display text-base font-bold text-textPrimary group-hover:text-[#25D366] transition-colors mb-1">
              Reservar Mesa o Cumpleaños
            </h4>
            <p className="text-xs text-textSecondary">
              Atención directa por WhatsApp: +54 9 341 680-2275
            </p>
          </a>

          {/* Carpeta Drive Oficial */}
          <a
            href="https://drive.google.com/drive/folders/1nQJKftaSDtPjgDU_UEiqetQnh72M2eEz"
            target="_blank"
            rel="noopener noreferrer"
            className="group p-5 rounded-3xl bg-surface-card border border-surface-border hover:border-cosme-amber/60 shadow-lg transition-all duration-300 hover:scale-[1.01]"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-cosme-amber/15 border border-cosme-amber/30 flex items-center justify-center text-cosme-amber">
                <Folder className="w-5 h-5" />
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-cosme-amber/15 text-cosme-amber">
                Google Drive
              </span>
            </div>
            <h4 className="font-display text-base font-bold text-textPrimary group-hover:text-cosme-amber transition-colors mb-1">
              Carpeta Completa de Menús
            </h4>
            <p className="text-xs text-textSecondary">
              Accedé a todos los archivos y cartas oficiales en Drive.
            </p>
          </a>
        </div>
      </div>
    </section>
  );
};
