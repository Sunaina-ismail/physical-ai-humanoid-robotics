import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './MobileNavigation.module.css';

const MobileNavigation: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  // Sample book modules - in a real implementation, these would come from the site's documentation structure
  const bookModules = [
    { title: 'Introduction', path: '/docs/intro' },
    { title: 'Robotics Fundamentals', path: '/docs/robotics-fundamentals' },
    { title: 'AI Perception', path: '/docs/ai-perception' },
    { title: 'Motion Planning', path: '/docs/motion-planning' },
    { title: 'Control Systems', path: '/docs/control-systems' },
    { title: 'Humanoid Design', path: '/docs/humanoid-design' },
  ];

  return (
    <div className={styles.mobileNavContainer}>
      <button
        className={`${styles.menuButton} ${isOpen ? styles.menuButtonOpen : ''}`}
        onClick={toggleMenu}
        aria-label={isOpen ? 'Close navigation menu' : 'Open navigation menu'}
      >
        <span className={styles.hamburgerLine}></span>
        <span className={styles.hamburgerLine}></span>
        <span className={styles.hamburgerLine}></span>
      </button>

      {isOpen && (
        <nav className={styles.mobileMenu} role="navigation" aria-label="Main navigation">
          <ul className={styles.navList}>
            {bookModules.map((module, index) => (
              <li key={index} className={styles.navItem}>
                <Link
                  to={module.path}
                  className={styles.navLink}
                  onClick={() => setIsOpen(false)}
                >
                  {module.title}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
};

export default MobileNavigation;