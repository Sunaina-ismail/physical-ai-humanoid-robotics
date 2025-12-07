import React from 'react';
import RoboticLogo from './RoboticLogo';
import styles from './RoboticHeading.module.css';

interface RoboticHeadingProps {
  text: string;
  colorMode?: 'light' | 'dark';
}

const RoboticHeading: React.FC<RoboticHeadingProps> = ({ text, colorMode = 'dark' }) => {
  return (
    <div className={`${styles.roboticHeadingContainer} ${styles[colorMode]}`}>
      <h1 className={styles.roboticMainTitle}>
        <RoboticLogo />
      </h1>
    </div>
  );
};

export default RoboticHeading;