import React from 'react';
import { Beer, Flame, Gauge } from 'lucide-react';

/**
 * BeerCard — Shadcn UI / Tailwind CSS Component para Cosme Alberdi
 * Props:
 * - tapNumber: string | number (ej: '01')
 * - name: string (ej: 'IPA Alberdi')
 * - styleTag: string (ej: 'Lupulada & Aromática')
 * - abv: string (ej: '6.2%')
 * - ibu: string | number (ej: '55')
 * - description: string
 * - onOrder: () => void
 */
export const BeerCard = ({
  tapNumber = '01',
  name = 'IPA Alberdi',
  styleTag = 'Lupulada & Aromática',
  abv = '6.2%',
  ibu = '55',
  description = 'Explosión de lúpulos patagónicos con notas a pomelo rosado y resina.',
  onOrder
}) => {
  return (
    <article className="group relative flex flex-col justify-between rounded-xl border border-white/10 bg-zinc-950/80 p-6 backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-amber-500/50 hover:shadow-2xl hover:shadow-amber-500/10 dark:bg-zinc-950/90">
      <div>
        {/* Top Header: Style + Tap # */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-[11px] font-bold uppercase tracking-wider text-amber-400/90">
            {styleTag}
          </span>
          <span className="rounded-md border border-amber-500/30 bg-amber-500/10 px-2 py-0.5 font-mono text-[11px] font-bold text-amber-300">
            TAP #{tapNumber}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-heading text-2xl font-bold tracking-wide uppercase text-neutral-100 group-hover:text-amber-200 transition-colors">
          {name}
        </h3>

        {/* Technical Specs: ABV & IBU */}
        <div className="mt-3 mb-4 flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 font-mono text-xs font-semibold text-neutral-300">
            <Gauge className="h-3.5 w-3.5 text-amber-400" />
            ABV {abv}
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-2.5 py-1 font-mono text-xs font-semibold text-neutral-300">
            <Flame className="h-3.5 w-3.5 text-red-400" />
            IBU {ibu}
          </span>
        </div>

        {/* Tasting Notes */}
        <p className="text-sm leading-relaxed text-neutral-400 mb-6 line-clamp-3">
          {description}
        </p>
      </div>

      {/* Action CTA */}
      <button
        onClick={onOrder}
        className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-amber-500/30 bg-amber-500/10 px-4 py-2.5 text-xs font-bold uppercase tracking-wide text-amber-400 transition-all duration-200 hover:bg-amber-500 hover:text-zinc-950 hover:shadow-lg hover:shadow-amber-500/25 active:scale-95"
      >
        <Beer className="h-4 w-4" />
        Pedir Pinta
      </button>
    </article>
  );
};

export default BeerCard;
