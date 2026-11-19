import React, { useState, useEffect } from 'react';
import { X, ExternalLink, Download, FileText, Coffee, Beer } from '../ui/Icons';

export interface PdfDocument {
  id: string;
  title: string;
  subtitle: string;
  driveId: string;
  badge: string;
  iconType: 'night' | 'day';
}

export const PDF_DOCS: Record<string, PdfDocument> = {
  noche: {
    id: 'noche',
    title: 'Carta General, Noche & Salón',
    subtitle: 'Comida libre, smash burgers, parrilla, cerveza tirada y cócteles',
    driveId: '1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt',
    badge: 'CARTA SALÓN 2026',
    iconType: 'night',
  },
  dia: {
    id: 'dia',
    title: 'Desayunos, Cafetería & Meriendas',
    subtitle: 'Café de especialidad, torres de 3 pisos, tostadas masa madre y brunch',
    driveId: '1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N',
    badge: 'DESAYUNOS & MERIENDAS',
    iconType: 'day',
  },
};

export const PdfModal: React.FC = () => {
  const [activeDoc, setActiveDoc] = useState<PdfDocument | null>(null);

  useEffect(() => {
    const handleOpenPdf = (e: any) => {
      const docKey = e.detail?.docKey;
      if (docKey && PDF_DOCS[docKey]) {
        setActiveDoc(PDF_DOCS[docKey]);
      }
    };

    window.addEventListener('cosme-open-pdf', handleOpenPdf);
    return () => window.removeEventListener('cosme-open-pdf', handleOpenPdf);
  }, []);

  useEffect(() => {
    if (activeDoc) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [activeDoc]);

  if (!activeDoc) return null;

  const previewUrl = `https://drive.google.com/file/d/${activeDoc.driveId}/preview`;
  const fullDriveUrl = `https://drive.google.com/file/d/${activeDoc.driveId}/view?usp=sharing`;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 md:p-6 bg-black/85 backdrop-blur-md animate-in fade-in duration-200"
      onClick={() => setActiveDoc(null)}
      role="dialog"
      aria-modal="true"
      aria-label={activeDoc.title}
    >
      <div 
        className="relative w-full max-w-4xl h-[92vh] max-h-[850px] bg-surface-card border border-surface-border rounded-3xl overflow-hidden shadow-2xl flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-surface-border bg-black/40">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
              activeDoc.iconType === 'night' 
                ? 'bg-cosme-red/15 text-cosme-red border border-cosme-red/30' 
                : 'bg-cosme-hop/15 text-cosme-hop border border-cosme-hop/30'
            }`}>
              {activeDoc.iconType === 'night' ? <Beer className="w-5 h-5" /> : <Coffee className="w-5 h-5" />}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-display font-bold text-base sm:text-lg text-textPrimary">
                  {activeDoc.title}
                </h3>
                <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-white/10 text-textSecondary">
                  {activeDoc.badge}
                </span>
              </div>
              <p className="text-xs text-textSecondary hidden sm:block">
                {activeDoc.subtitle}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <a
              href={fullDriveUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="py-2 px-3 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-mono font-bold uppercase text-textPrimary border border-white/10 transition-colors flex items-center gap-1.5"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Abrir en Drive</span>
            </a>
            <button
              type="button"
              onClick={() => setActiveDoc(null)}
              className="p-2 rounded-xl text-textSecondary hover:text-white hover:bg-white/10 transition-colors"
              aria-label="Cerrar visor de PDF"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Embedded PDF Viewer */}
        <div className="relative flex-1 w-full bg-black/60 overflow-hidden">
          <iframe
            src={previewUrl}
            title={activeDoc.title}
            className="w-full h-full border-0"
            allow="autoplay"
          ></iframe>
        </div>

        {/* Modal Footer */}
        <div className="p-3 sm:p-4 border-t border-surface-border bg-black/40 flex items-center justify-between text-xs font-mono text-textSecondary">
          <span>Menú oficial de Cosme Alberdi en Google Drive</span>
          <a
            href={fullDriveUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-cosme-amber hover:underline flex items-center gap-1"
          >
            <span>Descargar PDF</span>
            <Download className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
};

// Helper function to dispatch event from anywhere
export const openPdfModal = (docKey: 'noche' | 'dia') => {
  window.dispatchEvent(new CustomEvent('cosme-open-pdf', { detail: { docKey } }));
};
