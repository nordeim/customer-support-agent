// frontend/src/components/ChatWindow/ChatWindow.tsx
import React from 'react';
import { useChat } from '../../hooks/useChat';
import Message from '../Message';
import MessageInput from '../MessageInput';
import TypingIndicator from '../TypingIndicator';
import EscalationNotice from '../EscalationNotice';
import { EscalationInfo } from '../../types/chat';
import styles from './ChatWindow.module.css';

interface ChatWindowProps {
  onEscalation?: (escalationInfo: EscalationInfo) => void;
  onError?: (error: Error) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onEscalation, onError }) => {
  const {
    messages,
    isLoading,
    isTyping,
    error,
    sendMessage,
    resetSession,
    messagesEndRef,
  } = useChat({
    onEscalation,
    onError,
  });

  const handleSendMessage = async (message: string, attachments?: File[]) => {
    await sendMessage(message, attachments);
  };

  const handleResetSession = () => {
    resetSession();
  };

  return (
    <div className={styles.chatWindow}>
      <div className={styles.header}>
        <h2>Customer Support</h2>
        <button
          className={styles.resetButton}
          onClick={handleResetSession}
          title="Start new conversation"
        >
          New Chat
        </button>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        
        {isTyping && <TypingIndicator />}
        
        {error && (
          <div className={styles.errorMessage}>
            <p>Error: {error}</p>
            <button onClick={handleResetSession}>Try Again</button>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputContainer}>
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={isLoading}
          placeholder="Type your message..."
        />
      </div>
    </div>
  );
};

export default ChatWindow;
