import React from 'react';

interface CosmeLogoProps {
  className?: string;
  size?: number;
}

export const CosmeLogo: React.FC<CosmeLogoProps> = ({ className = 'w-10 h-12', size }) => {
  return (
    <svg 
      className={className} 
      viewBox="0 0 120 144" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      style={size ? { width: `${size}px`, height: `${size * 1.2}px` } : undefined}
      aria-hidden="true"
    >
      {/* Gorra snapback hacia atrás */}
      <path 
        className="stroke-current text-cosme-red" 
        d="M24 38C24 19 40 10 60 10C80 10 96 19 96 38Z" 
        strokeWidth="3.2" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-red" 
        d="M18 42C38 35 82 35 102 42" 
        strokeWidth="3.5" 
        strokeLinecap="round"
      />
      <path 
        className="stroke-current text-cosme-red" 
        d="M44 36C44 26 76 26 76 36" 
        strokeWidth="2.2"
      />
      <text 
        x="60" 
        y="25" 
        textAnchor="middle" 
        fill="#FFF7E0" 
        fontFamily="sans-serif" 
        fontWeight="900" 
        fontSize="10" 
        letterSpacing="1"
      >
        ·COSME·
      </text>

      {/* Orejas y expansores */}
      <path 
        className="stroke-current text-cosme-amber" 
        d="M25 50C17 50 16 67 24 68" 
        strokeWidth="2.8" 
        strokeLinecap="round"
      />
      <circle 
        className="stroke-current text-cosme-amber" 
        cx="22" 
        cy="61" 
        r="3.5" 
        strokeWidth="2.2"
      />
      <path 
        className="stroke-current text-cosme-amber" 
        d="M95 50C103 50 104 67 96 68" 
        strokeWidth="2.8" 
        strokeLinecap="round"
      />
      <circle 
        className="stroke-current text-cosme-amber" 
        cx="98" 
        cy="61" 
        r="3.5" 
        strokeWidth="2.2"
      />

      {/* Gafas retro con reflejo zigzag */}
      <rect 
        className="stroke-current text-cosme-red" 
        x="28" 
        y="47" 
        width="27" 
        height="17" 
        rx="4" 
        strokeWidth="3"
      />
      <rect 
        className="stroke-current text-cosme-red" 
        x="65" 
        y="47" 
        width="27" 
        height="17" 
        rx="4" 
        strokeWidth="3"
      />
      <path 
        className="stroke-current text-cosme-red" 
        d="M55 53H65" 
        strokeWidth="3"
      />
      <path 
        d="M33 58L41 51L43 56L50 50" 
        stroke="#FFFFFF" 
        strokeWidth="2.2" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />
      <path 
        d="M70 58L78 51L80 56L87 50" 
        stroke="#FFFFFF" 
        strokeWidth="2.2" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />

      {/* Bigote y barba tejida en flor de lúpulo */}
      <path 
        className="stroke-current text-cosme-amber" 
        d="M36 74C45 68 55 71 60 76C65 71 75 68 84 74C81 84 68 84 60 79C52 84 39 84 36 74Z" 
        strokeWidth="2.6" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-hop" 
        d="M31 76C27 90 36 104 46 105C44 95 47 86 54 83Z" 
        strokeWidth="2.6" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-hop" 
        d="M89 76C93 90 84 104 74 105C76 95 73 86 66 83Z" 
        strokeWidth="2.6" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-amber" 
        d="M47 93C46 106 53 116 60 120C67 116 74 106 73 93C66 87 54 87 47 93Z" 
        strokeWidth="2.6" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-hop" 
        d="M43 108C45 121 53 130 60 135C67 130 75 121 77 108C68 115 52 115 43 108Z" 
        strokeWidth="2.6" 
        strokeLinejoin="round"
      />
      <path 
        className="stroke-current text-cosme-amber" 
        d="M53 121C55 130 60 137 60 137C60 137 65 130 67 121" 
        strokeWidth="2.4" 
        strokeLinecap="round"
      />
    </svg>
  );
};
