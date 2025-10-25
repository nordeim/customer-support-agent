// frontend/src/components/TypingIndicator/TypingIndicator.tsx
import React from 'react';
import styles from './TypingIndicator.module.css';

const TypingIndicator: React.FC = () => {
  return (
    <div className={styles.typingIndicator}>
      <div className={styles.typingDots}>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className={styles.typingText}>Support agent is typing...</span>
    </div>
  );
};

export default TypingIndicator;
