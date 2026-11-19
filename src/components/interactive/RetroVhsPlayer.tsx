import React, { useState, useEffect } from 'react';
import { Play, Pause, Disc3 } from '../ui/Icons';

interface Tape {
  id: string;
  label: string;
  src: string;
  alt: string;
  date: string;
  status: string;
}

const TAPES: Tape[] = [
  {
    id: 'dj',
    label: 'CINTA 01 · DJ PIONEER EN VIVO',
    src: '/assets/dj-pioneer-vhs.jpg',
    alt: 'DJ tocando en vivo con consola Pioneer CDJ durante la Fiesta Retro de Cosme Alberdi',
    date: 'AUG 28 2026',
    status: 'PLAY ▶ · SP',
  },
  {
    id: 'pista',
    label: 'CINTA 02 · SALÓN, PISTA & CAJA NEÓN',
    src: '/assets/noche-fiesta-caja.jpg',
    alt: 'Salón repleto de fiesta nocturna con carteles CAJA y COSME en neón rojo',
    date: 'ALBERDI LIVE',
    status: 'CLUB ▶ · SLP',
  },
];

export const RetroVhsPlayer: React.FC = () => {
  const [activeTape, setActiveTape] = useState<Tape>(TAPES[0]);
  const [seconds, setSeconds] = useState<number>(5049); // Starts at 01:24:09
  const [isPaused, setIsPaused] = useState<boolean>(false);

  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [isPaused]);

  const formatTimecode = (totalSec: number) => {
    const h = String(Math.floor(totalSec / 3600) % 24).padStart(2, '0');
    const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
    const s = String(totalSec % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  return (
    <div className="w-full rounded-3xl bg-[#090A0D] border border-[#2D2E38] p-5 sm:p-6 shadow-2xl overflow-hidden flex flex-col justify-between">
      {/* VHS Camcorder Screen */}
      <div className="relative aspect-[16/10] sm:aspect-[16/9] w-full rounded-2xl overflow-hidden bg-black border border-white/10 group">
        <img
          src={activeTape.src}
          alt={activeTape.alt}
          className="w-full h-full object-cover filter contrast-125 saturate-110 group-hover:scale-105 transition-transform duration-700"
          width={800}
          height={500}
        />

        {/* Scanlines Overlay */}
        <div className="absolute inset-0 scanlines pointer-events-none opacity-40"></div>

        {/* Retro Camcorder OSD UI */}
        <div className="absolute inset-0 p-4 sm:p-6 flex flex-col justify-between pointer-events-none font-mono text-white select-none">
          {/* Top Row: REC indicator + Status */}
          <div className="flex items-center justify-between text-xs sm:text-sm font-bold tracking-widest drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]">
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full bg-[#FF1E27] ${isPaused ? 'opacity-30' : 'animate-ping'}`}></span>
              <span className="text-[#FF1E27] font-black tracking-wider">
                {isPaused ? 'PAUSE' : 'REC ●'}
              </span>
              <span className="text-white/60 ml-2 hidden sm:inline">ALBERDI CAM 01</span>
            </div>
            <div className="text-[#FFAA00] tracking-widest font-black">
              {isPaused ? 'PAUSE ⏸ · SP' : activeTape.status}
            </div>
          </div>

          {/* Center Subtle Crosshair */}
          <div className="self-center opacity-25">
            <div className="w-6 h-6 border-t border-l border-white"></div>
          </div>

          {/* Bottom Row: Date + Live Timecode */}
          <div className="flex items-end justify-between text-xs sm:text-sm font-bold tracking-widest drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]">
            <div className="text-white/80">
              {activeTape.date}
            </div>
            <div className="font-mono text-lg sm:text-xl text-[#00FF66] tracking-widest">
              TC {formatTimecode(seconds)}
            </div>
          </div>
        </div>
      </div>

      {/* VHS Player Physical Controls */}
      <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-white/10">
        {/* Tape Selector Buttons */}
        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          {TAPES.map((tape) => (
            <button
              key={tape.id}
              type="button"
              onClick={() => setActiveTape(tape)}
              className={`py-2 px-3.5 rounded-xl text-xs font-mono font-bold tracking-wider uppercase transition-all flex items-center gap-2 ${
                activeTape.id === tape.id
                  ? 'bg-[#FF1E27] text-white shadow-[0_0_15px_rgba(255,30,39,0.35)]'
                  : 'bg-white/5 text-textSecondary hover:text-white hover:bg-white/10 border border-white/5'
              }`}
            >
              <Disc3 className="w-3.5 h-3.5" />
              <span>{tape.label}</span>
            </button>
          ))}
        </div>

        {/* Pause / Play Button */}
        <button
          type="button"
          onClick={() => setIsPaused(!isPaused)}
          className="w-full sm:w-auto py-2 px-4 rounded-xl text-xs font-mono font-bold tracking-wider uppercase bg-white/5 hover:bg-white/10 text-white/80 hover:text-white border border-white/10 transition-all flex items-center justify-center gap-2"
        >
          {isPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
          <span>{isPaused ? 'Reanudar OSD' : 'Pausar OSD'}</span>
        </button>
      </div>
    </div>
  );
};
