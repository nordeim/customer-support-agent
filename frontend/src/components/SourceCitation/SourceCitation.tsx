// frontend/src/components/SourceCitation/SourceCitation.tsx
import React, { useState } from 'react';
import { SourceCitation as SourceCitationType } from '../../types/chat';
import styles from './SourceCitation.module.css';

interface SourceCitationProps {
  source: SourceCitationType;
}

const SourceCitation: React.FC<SourceCitationProps> = ({ source }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const getSourceTitle = () => {
    return source.metadata?.source || source.id;
  };

  return (
    <div className={styles.sourceCitation}>
      <div className={styles.sourceHeader} onClick={toggleExpanded}>
        <span className={styles.sourceTitle}>📄 {getSourceTitle()}</span>
        <button className={styles.toggleButton}>
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>
      
      {isExpanded && (
        <div className={styles.sourceContent}>
          <p>{source.content}</p>
          {source.distance !== undefined && (
            <div className={styles.relevance}>
              Relevance: {Math.round((1 - source.distance) * 100)}%
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SourceCitation;
