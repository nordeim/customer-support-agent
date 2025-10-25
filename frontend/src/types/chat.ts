// frontend/src/types/chat.ts
export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
  attachments?: Attachment[];
  sources?: SourceCitation[];
  requires_escalation?: boolean;
}

export interface Attachment {
  id: string;
  filename: string;
  content_type: string;
  file_path: string;
  processed_text?: string;
}

export interface SourceCitation {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance?: number;
}

export interface ChatSession {
  id: string;
  user_id?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface EscalationInfo {
  ticket_id: string;
  message: string;
  estimated_wait_time: string;
}
