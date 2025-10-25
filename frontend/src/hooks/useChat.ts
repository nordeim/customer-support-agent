// frontend/src/hooks/useChat.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { ChatMessage, ChatSession, EscalationInfo } from '../types/chat';
import { apiService } from '../services/api';
import { useLocalStorage } from './useLocalStorage';

interface UseChatOptions {
  onEscalation?: (escalationInfo: EscalationInfo) => void;
  onError?: (error: Error) => void;
}

export const useChat = (options: UseChatOptions = {}) => {
  const [session, setSession] = useState<ChatSession | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { onEscalation, onError } = options;
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [currentSessionId, setCurrentSessionId] = useLocalStorage('chat_session_id', null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Initialize or restore session
  useEffect(() => {
    const initializeSession = async () => {
      try {
        if (currentSessionId) {
          // Try to restore existing session
          const historyResponse = await apiService.getChatHistory(currentSessionId);
          if (historyResponse.data) {
            setMessages(historyResponse.data.messages);
            setSession({
              id: historyResponse.data.session_id,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              is_active: true,
            });
            return;
          }
        }

        // Create new session
        const sessionResponse = await apiService.createSession();
        if (sessionResponse.data) {
          const newSession = {
            id: sessionResponse.data.session_id,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            is_active: true,
          };
          setSession(newSession);
          setCurrentSessionId(newSession.id);
        }
      } catch (err) {
        const error = err as Error;
        setError(error.message);
        onError?.(error);
      }
    };

    initializeSession();
  }, [currentSessionId, setCurrentSessionId, onError]);

  const sendMessage = useCallback(async (
    content: string,
    attachments?: File[]
  ) => {
    if (!session || !content.trim()) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      content: content.trim(),
      role: 'user',
      timestamp: new Date().toISOString(),
      attachments: attachments?.map(file => ({
        id: `attachment-${Date.now()}`,
        filename: file.name,
        content_type: file.type,
        file_path: '', // Will be set by backend
      })),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setIsTyping(true);
    setError(null);

    try {
      const response = await apiService.sendMessage(
        session.id,
        content,
        attachments
      );

      if (response.data) {
        const assistantMessage: ChatMessage = {
          id: `assistant-${Date.now()}`,
          content: response.data.message,
          role: 'assistant',
          timestamp: new Date().toISOString(),
          sources: response.data.sources,
          requires_escalation: response.data.requires_escalation,
        };

        setMessages(prev => [...prev, assistantMessage]);

        // Handle escalation if needed
        if (response.data.requires_escalation) {
          onEscalation?.({
            ticket_id: 'generated-ticket-id', // Would come from response
            message: response.data.message,
            estimated_wait_time: '15 minutes',
          });
        }
      }
    } catch (err) {
      const error = err as Error;
      setError(error.message);
      onError?.(error);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  }, [session, onEscalation, onError]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const resetSession = useCallback(async () => {
    try {
      const sessionResponse = await apiService.createSession();
      if (sessionResponse.data) {
        const newSession = {
          id: sessionResponse.data.session_id,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          is_active: true,
        };
        setSession(newSession);
        setCurrentSessionId(newSession.id);
        clearMessages();
      }
    } catch (err) {
      const error = err as Error;
      setError(error.message);
      onError?.(error);
    }
  }, [setCurrentSessionId, clearMessages, onError]);

  return {
    session,
    messages,
    isLoading,
    isTyping,
    error,
    sendMessage,
    clearMessages,
    resetSession,
    messagesEndRef,
  };
};
