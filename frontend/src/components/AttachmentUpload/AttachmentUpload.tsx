// frontend/src/components/AttachmentUpload/AttachmentUpload.tsx
import React, { useRef } from 'react';
import styles from './AttachmentUpload.module.css';

interface AttachmentUploadProps {
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
  maxFiles?: number;
  maxSize?: number;
  acceptedTypes?: string[];
}

const AttachmentUpload: React.FC<AttachmentUploadProps> = ({
  onFilesSelected,
  disabled = false,
  maxFiles = 3,
  maxSize = 10 * 1024 * 1024, // 10MB
  acceptedTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf',
    'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ],
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    
    if (files.length === 0) return;

    // Validate files
    const validFiles = files.filter(file => {
      if (!acceptedTypes.includes(file.type)) {
        alert(`File type ${file.type} is not supported`);
        return false;
      }
      
      if (file.size > maxSize) {
        alert(`File ${file.name} is too large (max ${maxSize / 1024 / 1024}MB)`);
        return false;
      }
      
      return true;
    });

    if (validFiles.length > 0) {
      onFilesSelected(validFiles);
    }

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClick = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className={styles.attachmentUpload}>
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={acceptedTypes.join(',')}
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />
      
      <button
        type="button"
        onClick={handleClick}
        disabled={disabled}
        className={styles.uploadButton}
        title="Attach files"
      >
        📎
      </button>
    </div>
  );
};

export default AttachmentUpload;
