// frontend/src/services/api.ts
import { ApiResponse, SessionResponse, MessageResponse, ChatHistoryResponse, HealthCheckResponse } from '../types/api';
import { ChatMessage, Attachment } from '../types/chat';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return { data };
  }

  async createSession(userId?: string): Promise<ApiResponse<SessionResponse>> {
    return this.request<SessionResponse>('/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  }

  async sendMessage(
    sessionId: string,
    message: string,
    attachments?: File[]
  ): Promise<ApiResponse<MessageResponse>> {
    const formData = new FormData();
    formData.append('message', message);
    
    if (attachments) {
      attachments.forEach((file) => {
        formData.append('attachments', file);
      });
    }

    return this.request<MessageResponse>(`/chat/sessions/${sessionId}/messages`, {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
  }

  async getChatHistory(sessionId: string): Promise<ApiResponse<ChatHistoryResponse>> {
    return this.request<ChatHistoryResponse>(`/chat/sessions/${sessionId}/history`);
  }

  async healthCheck(): Promise<ApiResponse<HealthCheckResponse>> {
    return this.request<HealthCheckResponse>('/health/');
  }

  async detailedHealthCheck(): Promise<ApiResponse<HealthCheckResponse>> {
    return this.request<HealthCheckResponse>('/health/detailed');
  }
}

export const apiService = new ApiService();
