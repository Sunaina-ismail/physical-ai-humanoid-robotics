import React from 'react';
import styles from './RoboticLogo.module.css';

const RoboticLogo: React.FC = () => {
  return (
    <div className={styles.logoContainer}>
      <svg
        className={styles.roboticLogo}
        viewBox="0 0 200 80"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Physical AI & Humanoid Robotics Logo"
      >
        {/* Main Head/CPU Unit */}
        <rect
          x="50"
          y="15"
          width="100"
          height="50"
          rx="10"
          fill="none"
          stroke="#d4af37"
          strokeWidth="2"
          className={styles.metallicStroke}
        />

        {/* Circuit Pattern Inside Head */}
        <g className={styles.circuitPattern}>
          <circle cx="70" cy="30" r="3" fill="#d4af37" opacity="0.7" />
          <circle cx="90" cy="25" r="2" fill="#d4af37" opacity="0.7" />
          <circle cx="110" cy="35" r="2.5" fill="#d4af37" opacity="0.7" />
          <circle cx="130" cy="30" r="3" fill="#d4af37" opacity="0.7" />

          <line x1="60" y1="40" x2="75" y2="40" stroke="#d4af37" strokeWidth="1" opacity="0.5" />
          <line x1="80" y1="45" x2="95" y2="45" stroke="#d4af37" strokeWidth="1" opacity="0.5" />
          <line x1="100" y1="40" x2="115" y2="40" stroke="#d4af37" strokeWidth="1" opacity="0.5" />
          <line x1="120" y1="45" x2="135" y2="45" stroke="#d4af37" strokeWidth="1" opacity="0.5" />
        </g>

        {/* Eyes/Sensors */}
        <circle cx="85" cy="35" r="6" fill="none" stroke="#a67c52" strokeWidth="2" className={styles.glowingElement} />
        <circle cx="85" cy="35" r="3" fill="#a67c52" className={styles.pupil} />
        <circle cx="115" cy="35" r="6" fill="none" stroke="#a67c52" strokeWidth="2" className={styles.glowingElement} />
        <circle cx="115" cy="35" r="3" fill="#a67c52" className={styles.pupil} />

        {/* Decorative Antenna */}
        <line x1="100" y1="15" x2="100" y2="5" stroke="#d4af37" strokeWidth="2" />
        <circle cx="100" cy="3" r="3" fill="#a67c52" className={styles.glowingElement} />

        {/* Neck/Connection */}
        <rect x="90" y="65" width="20" height="10" fill="#1a1445" className={styles.metallicFill} />

        {/* Futuristic Brackets */}
        <path d="M55,20 L50,15 L55,10 L60,15 Z" fill="#d4af37" opacity="0.8" />
        <path d="M145,20 L150,15 L145,10 L140,15 Z" fill="#d4af37" opacity="0.8" />

        {/* Status Indicator Lights */}
        <circle cx="60" cy="25" r="2" fill="#4CAF50" className={styles.statusLight} />
        <circle cx="140" cy="25" r="2" fill="#2196F3" className={styles.statusLight} />

        {/* Geometric Accent Lines */}
        <line x1="55" y1="55" x2="65" y2="55" stroke="#d4af37" strokeWidth="1.5" />
        <line x1="135" y1="55" x2="145" y2="55" stroke="#d4af37" strokeWidth="1.5" />

        {/* Glowing Effect Overlay */}
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
          <feColorMatrix in="blur" type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 20 -8" />
          <feBlend in="SourceGraphic" in2="blur" mode="screen" />
        </filter>

        {/* Text Placeholder */}
        <text
          x="100"
          y="75"
          textAnchor="middle"
          fill="#e0e0e0"
          fontSize="8"
          fontFamily="'Playfair Display', 'Cinzel', 'Trajan', serif"
          fontWeight="bold"
          className={styles.logoText}
        >
          PHYSICAL AI & HUMANOID ROBOTICS
        </text>
      </svg>
    </div>
  );
};

export default RoboticLogo;