// frontend/src/components/EscalationNotice/EscalationNotice.tsx
import React from 'react';
import { EscalationInfo } from '../../types/chat';
import styles from './EscalationNotice.module.css';

interface EscalationNoticeProps {
  escalationInfo: EscalationInfo;
  onClose?: () => void;
}

const EscalationNotice: React.FC<EscalationNoticeProps> = ({
  escalationInfo,
  onClose,
}) => {
  return (
    <div className={styles.escalationNotice}>
      <div className={styles.noticeContent}>
        <h3>🎫 Escalated to Human Agent</h3>
        <p>{escalationInfo.message}</p>
        <div className={styles.ticketInfo}>
          <strong>Ticket ID:</strong> {escalationInfo.ticket_id}
        </div>
        <div className={styles.waitTime}>
          <strong>Estimated wait time:</strong> {escalationInfo.estimated_wait_time}
        </div>
      </div>
      
      {onClose && (
        <button className={styles.closeButton} onClick={onClose}>
          ×
        </button>
      )}
    </div>
  );
};

export default EscalationNotice;
