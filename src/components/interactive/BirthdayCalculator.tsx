import React, { useState } from 'react';
import { birthdayPromos, guestOptions, type BirthdayPromo } from '../../data/birthdayData';
import { PartyPopper, Check, Users, MessageSquareText } from '../ui/Icons';
import confetti from 'canvas-confetti';

export const BirthdayCalculator: React.FC = () => {
  const [selectedPromo, setSelectedPromo] = useState<BirthdayPromo>(birthdayPromos[1]); // Default to Promo 2
  const [guests, setGuests] = useState<number>(12);

  const formatARS = (val: number) => {
    return '$' + val.toLocaleString('es-AR');
  };

  const totalPrice = selectedPromo.pricePerPerson * guests;
  const guestLabel = guests === 30 ? '30+ personas' : `${guests} personas`;

  const triggerConfetti = () => {
    try {
      confetti({
        particleCount: 70,
        spread: 60,
        origin: { y: 0.8 },
        colors: ['#FF1E27', '#FFAA00', '#F5B727', '#FFFFFF'],
      });
    } catch (e) {
      // safe fallback if canvas-confetti is not loaded
    }
  };

  const handlePromoSelect = (promo: BirthdayPromo) => {
    setSelectedPromo(promo);
    triggerConfetti();
  };

  const waMessage = `Hola Cosme Alberdi! Quiero cotizar y reservar mi cumpleaños para ${guestLabel} con la ${selectedPromo.name} (${formatARS(selectedPromo.pricePerPerson)} por persona — total estimado ${formatARS(totalPrice)}). ¿Tienen disponibilidad?`;
  const waUrl = `https://wa.me/5493416802275?text=${encodeURIComponent(waMessage)}`;

  return (
    <div className="rounded-3xl bg-surface-card border border-surface-border p-6 sm:p-8 shadow-2xl relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute -top-24 -right-24 w-72 h-72 bg-[#FF1E27]/10 rounded-full blur-3xl pointer-events-none"></div>

      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-bold uppercase bg-[#FF1E27]/10 text-[#FF666C] border border-[#FF1E27]/20 mb-2">
            <PartyPopper className="w-3.5 h-3.5 text-[#FF1E27]" />
            Cotizador Oficial en Vivo
          </div>
          <h3 className="font-display text-2xl sm:text-3xl font-extrabold">
            Calculá tu Festejo o Cumpleaños
          </h3>
          <p className="text-textSecondary text-sm">
            Elegí tu menú libre favorito y la cantidad aproximada de amigos.
          </p>
        </div>
      </div>

      {/* Promo Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8" role="radiogroup" aria-label="Opciones de menú libre">
        {birthdayPromos.map((promo) => {
          const isSelected = selectedPromo.id === promo.id;
          return (
            <button
              key={promo.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => handlePromoSelect(promo)}
              className={`relative text-left p-5 rounded-2xl border transition-all duration-300 flex flex-col justify-between ${
                isSelected
                  ? 'bg-gradient-to-b from-[#1E1517] to-[#141418] border-[#FF1E27] shadow-[0_0_25px_rgba(255,30,39,0.25)] ring-1 ring-[#FF1E27]'
                  : 'bg-black/20 border-surface-border hover:border-white/20'
              }`}
            >
              {promo.recommended && (
                <span className="absolute -top-3 right-4 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-[#FF1E27] text-white shadow-md">
                  Más Elegida
                </span>
              )}

              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-display font-bold text-base text-textPrimary">
                    {promo.name}
                  </h4>
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center border ${
                    isSelected ? 'bg-[#FF1E27] border-[#FF1E27]' : 'border-white/20'
                  }`}>
                    {isSelected && <Check className="w-3 h-3 text-white" />}
                  </div>
                </div>

                <div className="mb-3">
                  <span className="font-display text-2xl font-black text-[#FFAA00]">
                    {formatARS(promo.pricePerPerson)}
                  </span>
                  <span className="text-xs text-textSecondary font-mono ml-1">/ persona</span>
                </div>

                <p className="text-xs text-textSecondary leading-relaxed mb-4">
                  {promo.description}
                </p>
              </div>

              <ul className="space-y-1.5 pt-3 border-t border-white/5 text-[11px] text-textSecondary">
                {promo.included.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-[#FF1E27] font-bold">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </button>
          );
        })}
      </div>

      {/* Guest Selector & Total Summary */}
      <div className="p-6 rounded-2xl bg-black/40 border border-surface-border flex flex-col lg:flex-row items-center justify-between gap-6">
        {/* Guest Pills */}
        <div className="w-full lg:w-auto">
          <label className="block text-xs font-mono font-bold uppercase text-textSecondary mb-2 flex items-center gap-1.5">
            <Users className="w-3.5 h-3.5 text-[#FFAA00]" />
            ¿Cuántos amigos vienen?
          </label>
          <div className="flex flex-wrap gap-2">
            {guestOptions.map((n) => (
              <button
                key={n}
                type="button"
                onClick={() => setGuests(n)}
                className={`py-2 px-4 rounded-xl text-sm font-display font-bold transition-all ${
                  guests === n
                    ? 'bg-[#FFAA00] text-black shadow-lg scale-105'
                    : 'bg-white/5 text-textSecondary hover:text-white hover:bg-white/10 border border-white/5'
                }`}
              >
                {n === 30 ? '30+' : n}
              </button>
            ))}
          </div>
        </div>

        {/* Pricing Summary & WA CTA */}
        <div className="w-full lg:w-auto flex flex-col sm:flex-row items-start sm:items-center gap-5 justify-between">
          <div>
            <span className="block text-xs text-textSecondary font-mono">
              Total estimado ({guestLabel} · {selectedPromo.name.split('·')[0].trim()}):
            </span>
            <div className="font-display text-3xl sm:text-4xl font-black text-white glow-amber">
              {formatARS(totalPrice)}
            </div>
          </div>

          <a
            href={waUrl}
            target="_blank"
            rel="noopener noreferrer"
            onClick={triggerConfetti}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 py-4 px-6 rounded-xl font-display font-extrabold text-sm uppercase tracking-wider text-white bg-[#FF1E27] hover:bg-[#D9121A] transition-all duration-300 shadow-[0_0_25px_rgba(255,30,39,0.4)] hover:shadow-[0_0_35px_rgba(255,30,39,0.6)] hover:scale-[1.02] active:scale-[0.98]"
          >
            <MessageSquareText className="w-4 h-4" />
            <span>Reservar Promo por WhatsApp</span>
          </a>
        </div>
      </div>
    </div>
  );
};
