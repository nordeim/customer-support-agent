// frontend/src/types/api.ts
export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface SessionResponse {
  session_id: string;
  thread_id: string;
  message: string;
}

export interface MessageResponse {
  message: string;
  sources: SourceCitation[];
  requires_escalation: boolean;
}

export interface ChatHistoryResponse {
  session_id: string;
  messages: ChatMessage[];
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  version: string;
  components: {
    database: string;
    agent_framework: string;
    chroma: string;
  };
}

export interface AttachmentUploadResponse {
  success: boolean;
  attachment_id?: string;
  processed_text?: string;
  error?: string;
}
