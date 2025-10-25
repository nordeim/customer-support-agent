// frontend/src/components/Message/Message.tsx
import React from 'react';
import { ChatMessage } from '../../types/chat';
import SourceCitation from '../SourceCitation';
import AttachmentList from '../AttachmentList';
import styles from './Message.module.css';

interface MessageProps {
  message: ChatMessage;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const formattedTime = new Date(message.timestamp).toLocaleTimeString();

  return (
    <div className={`${styles.message} ${styles[message.role]}`}>
      <div className={styles.messageContent}>
        <div className={styles.messageHeader}>
          <span className={styles.sender}>
            {isUser ? 'You' : 'Support Agent'}
          </span>
          <span className={styles.timestamp}>{formattedTime}</span>
        </div>
        
        <div className={styles.messageText}>
          {message.content.split('\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>

        {message.attachments && message.attachments.length > 0 && (
          <AttachmentList attachments={message.attachments} />
        )}

        {message.sources && message.sources.length > 0 && (
          <div className={styles.sources}>
            <h4>Sources:</h4>
            {message.sources.map((source, index) => (
              <SourceCitation key={index} source={source} />
            ))}
          </div>
        )}

        {message.requires_escalation && (
          <div className={styles.escalationNotice}>
            <p>This conversation has been escalated to a human agent.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
