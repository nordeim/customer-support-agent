// frontend/src/components/MessageInput/MessageInput.tsx
import React, { useState, useRef, useEffect } from 'react';
import AttachmentUpload from '../AttachmentUpload';
import styles from './MessageInput.module.css';

interface MessageInputProps {
  onSendMessage: (message: string, attachments?: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
}

const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = 'Type your message...',
}) => {
  const [message, setMessage] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (message.trim() || attachments.length > 0) {
      onSendMessage(message.trim(), attachments);
      setMessage('');
      setAttachments([]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleAttachmentAdd = (files: File[]) => {
    setAttachments(prev => [...prev, ...files]);
  };

  const handleAttachmentRemove = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <form className={styles.messageInput} onSubmit={handleSubmit}>
      <div className={styles.inputContainer}>
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className={styles.textarea}
          rows={1}
        />
        
        <AttachmentUpload
          onFilesSelected={handleAttachmentAdd}
          disabled={disabled}
          maxFiles={3}
          maxSize={10 * 1024 * 1024} // 10MB
        />
      </div>

      {attachments.length > 0 && (
        <div className={styles.attachmentsPreview}>
          {attachments.map((file, index) => (
            <div key={index} className={styles.attachmentPreview}>
              <span className={styles.fileName}>{file.name}</span>
              <button
                type="button"
                className={styles.removeButton}
                onClick={() => handleAttachmentRemove(index)}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      <button
        type="submit"
        disabled={disabled || (!message.trim() && attachments.length === 0)}
        className={styles.sendButton}
      >
        Send
      </button>
    </form>
  );
};

export default MessageInput;
