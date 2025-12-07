import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import { useTheme } from './ThemeContext';
import useIsMobile from './useIsMobile';
import { measureAssetLoadTime, logPerformanceMetrics } from './performanceMonitor';
import ParticleBackground from '@site/src/components/ParticleBackground/ParticleBackground';
import styles from './HeroSection.module.css';

interface HeroSectionProps {
  titleLine1?: string;
  titleLine2?: string;
  author?: string;
  ctaText?: string;
  ctaLink?: string;
  robotImageUrl?: string;
  bgImageUrl?: string;
  themeMode?: 'light' | 'dark';
}

const HeroSection: React.FC<HeroSectionProps> = ({
  titleLine1 = "PHYSICAL AI",
  titleLine2 = "HUMANOID ROBOTICS",
  author = "SUNAINA ISMAIL",
  ctaText = "Start Reading",
  ctaLink = "/docs",
  robotImageUrl = "/img/home.png",
  bgImageUrl,
  themeMode
}) => {
  // Safely attempt to get theme context, with fallback to 'dark' theme
  const themeContext = useTheme();
  const effectiveTheme = themeMode || (themeContext ? themeContext.theme : 'dark');
  const isMobile = useIsMobile();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  // Preload image for faster loading
  useEffect(() => {
    const img = new Image();
    img.src = robotImageUrl;
    img.onload = () => setImageLoaded(true);
    img.onerror = () => setImageError(true);
  }, [robotImageUrl]);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  return (
    <div className={`${styles.heroBgLayered} ${styles[effectiveTheme]}`}>
      {/* Particle background animation */}
      <ParticleBackground />

      {/* Code overlay background effect */}
      <div className={styles.codeOverlay}>
        <div className={styles.codeBlock}>
          {`// Initialize Physical AI System
import { PhysicalAI, HumanoidRobot } from '@robotics/core';

const humanoid = new HumanoidRobot({
  sensors: ['camera', 'lidar', 'imu'],
  actuators: ['motors', 'servos'],
  ai: new PhysicalAI({
    vision: true,
    navigation: true,
    manipulation: true
  })
});

humanoid.initialize();
humanoid.connect();`}
        </div>
      </div>

      <div className={styles.heroSectionContainer}>
        {/* Left column - Text & Action */}
        <div className={styles.heroContent}>
          <div className={styles.titleContainer}>
            <h1 className="futuristic-title">{titleLine1}</h1>
            <div className="title-connector">AND</div>
            <h1 className="futuristic-title">{titleLine2}</h1>
          </div>

          <Link
            to={ctaLink}
            className={styles.heroCtaButton}
          >
            {ctaText}
          </Link>

          <div className={styles.heroAuthor}>
            {author}
          </div>
        </div>

        {/* Right column - Visual with robotic animations */}
        <div className={styles.heroVisual}>
          {/* Circuit board animation behind the robot */}
          <div className={styles.circuitBackground}>
            <svg className={styles.circuitSvg} viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
              {/* Animated circuit paths */}
              <g className={styles.circuitLines}>
                <line x1="50" y1="50" x2="150" y2="50" stroke="rgba(100, 200, 255, 0.5)" strokeWidth="2" />
                <line x1="150" y1="50" x2="150" y2="150" stroke="rgba(100, 200, 255, 0.5)" strokeWidth="2" />
                <line x1="250" y1="100" x2="350" y2="100" stroke="rgba(138, 43, 226, 0.5)" strokeWidth="2" />
                <line x1="100" y1="200" x2="300" y2="200" stroke="rgba(100, 200, 255, 0.5)" strokeWidth="2" />
                <line x1="200" y1="250" x2="200" y2="350" stroke="rgba(138, 43, 226, 0.5)" strokeWidth="2" />
              </g>

              {/* Animated circuit nodes */}
              <g className={styles.circuitNodes}>
                <circle cx="50" cy="50" r="4" fill="rgba(100, 200, 255, 0.8)" />
                <circle cx="150" cy="50" r="4" fill="rgba(100, 200, 255, 0.8)" />
                <circle cx="150" cy="150" r="4" fill="rgba(100, 200, 255, 0.8)" />
                <circle cx="250" cy="100" r="4" fill="rgba(138, 43, 226, 0.8)" />
                <circle cx="350" cy="100" r="4" fill="rgba(138, 43, 226, 0.8)" />
                <circle cx="100" cy="200" r="4" fill="rgba(100, 200, 255, 0.8)" />
                <circle cx="300" cy="200" r="4" fill="rgba(100, 200, 255, 0.8)" />
                <circle cx="200" cy="250" r="4" fill="rgba(138, 43, 226, 0.8)" />
                <circle cx="200" cy="350" r="4" fill="rgba(138, 43, 226, 0.8)" />
              </g>
            </svg>
          </div>

          {!imageError ? (
            <>
              {!imageLoaded && (
                <div className={styles.imageLoader}>
                  <div className={styles.loaderSpinner}></div>
                </div>
              )}
              <img
                src={robotImageUrl}
                alt="Humanoid Robot"
                className={`${styles.robotImage} ${imageLoaded ? styles.imageLoaded : styles.imageLoading}`}
                onLoad={handleImageLoad}
                onError={() => setImageError(true)}
                loading="eager"
                fetchPriority="high"
              />
            </>
          ) : (
            <div className={styles.imagePlaceholder}>
              <p>Robot Image</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HeroSection;