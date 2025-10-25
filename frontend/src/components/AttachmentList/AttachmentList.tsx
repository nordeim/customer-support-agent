// frontend/src/components/AttachmentList/AttachmentList.tsx
import React from 'react';
import { Attachment } from '../../types/chat';
import styles from './AttachmentList.module.css';

interface AttachmentListProps {
  attachments: Attachment[];
}

const AttachmentList: React.FC<AttachmentListProps> = ({ attachments }) => {
  const getFileIcon = (contentType: string) => {
    if (contentType.startsWith('image/')) return '🖼️';
    if (contentType === 'application/pdf') return '📄';
    if (contentType.includes('word')) return '📝';
    if (contentType === 'text/plain') return '📄';
    return '📎';
  };

  return (
    <div className={styles.attachmentList}>
      {attachments.map((attachment) => (
        <div key={attachment.id} className={styles.attachment}>
          <span className={styles.fileIcon}>
            {getFileIcon(attachment.content_type)}
          </span>
          <span className={styles.fileName}>{attachment.filename}</span>
        </div>
      ))}
    </div>
  );
};

export default AttachmentList;
