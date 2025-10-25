Great — here are the **remaining frontend files** for the project skeleton, styled according to an “Apple-brand” inspired UI/UX (minimal, clean, high-contrast, San Francisco font, ample whitespace, touch-friendly). You can copy these into your frontend codebase and refine further.
Confidence for these artifacts: **Medium** (basic skeleton + styling; may need UI tweaking & browser testing).

---

### `frontend/src/api/chatService.ts`

```ts
// chatService.ts
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export interface ChatRequestPayload {
  session_id: string;
  message: string;
  stream?: boolean;
}

export interface ChatResponse {
  session_id: string;
  response: string;
}

export interface AttachmentUploadResponse {
  session_id: string;
  file_url: string;
}

export async function sendMessage(
  payload: ChatRequestPayload
): Promise<ChatResponse> {
  const resp = await axios.post<ChatResponse>(
    `${API_BASE}/chat/message`,
    payload,
    {
      headers: { "Content-Type": "application/json" },
      timeout: 30000,
    }
  );
  return resp.data;
}

export function sendMessageStream(
  payload: ChatRequestPayload,
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: any) => void
): EventSource {
  const url = `${API_BASE}/chat/message`;
  const evt = new EventSource(
    `${url}?session_id=${encodeURIComponent(payload.session_id)}&message=${encodeURIComponent(payload.message)}&stream=true`
  );
  evt.onmessage = (e) => {
    if (e.data === "[DONE]") {
      onDone();
      evt.close();
    } else {
      onChunk(e.data);
    }
  };
  evt.onerror = (err) => {
    onError(err);
    evt.close();
  };
  return evt;
}

export async function uploadAttachment(
  sessionId: string,
  file: File
): Promise<AttachmentUploadResponse> {
  const form = new FormData();
  form.append("session_id", sessionId);
  form.append("file", file);
  const resp = await axios.post<AttachmentUploadResponse>(
    `${API_BASE}/chat/upload-attachment`,
    form,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return resp.data;
}
```

---

### `frontend/src/utils/session.ts`

```ts
// session.ts
export function getSessionId(): string {
  const key = "csai_session_id";
  let sid = localStorage.getItem(key);
  if (!sid) {
    sid = crypto.randomUUID();
    localStorage.setItem(key, sid);
  }
  return sid;
}

export function resetSession(): void {
  const key = "csai_session_id";
  localStorage.removeItem(key);
}
```

---

### `frontend/src/context/ChatContext.tsx`

```tsx
// ChatContext.tsx
import React, { createContext, useContext, useReducer, ReactNode } from "react";
import { getSessionId } from "../utils/session";
import { ChatResponse } from "../api/chatService";

export interface Message {
  id: string;
  sender: "user" | "agent";
  content: string;
  timestamp: number;
}

interface ChatState {
  sessionId: string;
  messages: Message[];
  loading: boolean;
  error?: string;
}

type ChatAction =
  | { type: "INIT" }
  | { type: "SEND_USER"; payload: Message }
  | { type: "RECEIVE_AGENT"; payload: Message }
  | { type: "CLEAR_CHAT" }
  | { type: "SET_ERROR"; payload: string }
  | { type: "SET_LOADING"; payload: boolean };

const initialState: ChatState = {
  sessionId: getSessionId(),
  messages: [],
  loading: false,
  error: undefined,
};

function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "INIT":
      return { ...initialState, sessionId: getSessionId() };
    case "SEND_USER":
      return { ...state, messages: [...state.messages, action.payload] };
    case "RECEIVE_AGENT":
      return {
        ...state,
        messages: [...state.messages, action.payload],
        loading: false,
      };
    case "CLEAR_CHAT":
      return {
        sessionId: getSessionId(),
        messages: [],
        loading: false,
        error: undefined,
      };
    case "SET_ERROR":
      return { ...state, error: action.payload, loading: false };
    case "SET_LOADING":
      return { ...state, loading: action.payload, error: undefined };
    default:
      return state;
  }
}

const ChatContext = createContext<{
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
}>({
  state: initialState,
  dispatch: () => {},
});

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
};

export function useChat() {
  return useContext(ChatContext);
}
```

---

### `frontend/src/hooks/useChat.ts`

```ts
// useChat.ts
import { useChat } from "../context/ChatContext";
import {
  sendMessage,
  sendMessageStream,
  uploadAttachment,
  ChatRequestPayload,
} from "../api/chatService";

export function useChatActions() {
  const { state, dispatch } = useChat();

  async function sendUserMessage(message: string, stream = false) {
    dispatch({ type: "SET_LOADING", payload: true });
    const msgId = crypto.randomUUID();
    const userMsg = { id: msgId, sender: "user", content: message, timestamp: Date.now() };
    dispatch({ type: "SEND_USER", payload: userMsg });

    try {
      if (stream) {
        let combined = "";
        const onChunk = (chunk: string) => {
          combined += chunk;
          // Optionally update incremental agent message
          const agentMsg = {
            id: msgId + "-agent",
            sender: "agent",
            content: combined,
            timestamp: Date.now(),
          };
          dispatch({ type: "RECEIVE_AGENT", payload: agentMsg });
        };
        await new Promise<void>((resolve, reject) => {
          const evt = sendMessageStream(
            { session_id: state.sessionId, message, stream: true },
            onChunk,
            () => resolve(),
            (err) => reject(err)
          );
        });
      } else {
        const resp = await sendMessage({ session_id: state.sessionId, message, stream });
        const agentMsg = {
          id: crypto.randomUUID(),
          sender: "agent",
          content: resp.response,
          timestamp: Date.now(),
        };
        dispatch({ type: "RECEIVE_AGENT", payload: agentMsg });
      }
    } catch (err: any) {
      dispatch({ type: "SET_ERROR", payload: err?.message || "Unknown error" });
    }
  }

  async function sendAttachment(file: File) {
    try {
      const resp = await uploadAttachment(state.sessionId, file);
      // Optionally send a message referencing the file
      await sendUserMessage(`Uploaded attachment: ${file.name}`);
    } catch (err: any) {
      dispatch({ type: "SET_ERROR", payload: err?.message || "Attachment upload failed" });
    }
  }

  async function clearChat() {
    dispatch({ type: "CLEAR_CHAT" });
  }

  return {
    state,
    sendUserMessage,
    sendAttachment,
    clearChat,
  };
}
```

---

### `frontend/src/components/ChatWindow/ChatWindow.tsx`

```tsx
// ChatWindow.tsx
import React, { useEffect, useRef } from "react";
import { useChat, useChatActions } from "../../context/ChatContext";
import MessageList from "../MessageList/MessageList";
import MessageInput from "../MessageInput/MessageInput";
import AttachmentUploader from "../AttachmentUploader/AttachmentUploader";
import ClearChatButton from "../ClearChatButton/ClearChatButton";
import TypingIndicator from "../TypingIndicator/TypingIndicator";

const ChatWindow: React.FC = () => {
  const { state } = useChat();
  const { sendUserMessage, sendAttachment, clearChat } = useChatActions();
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto scroll to bottom when messages update
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [state.messages]);

  return (
    <div className="chat-window">
      <header className="chat-header">
        <h1 className="chat-title">Support Assistant</h1>
        <ClearChatButton onClear={clearChat} />
      </header>
      <div ref={listRef} className="chat-body">
        <MessageList messages={state.messages} />
        {state.loading && <TypingIndicator />}
      </div>
      <footer className="chat-input-area">
        <AttachmentUploader onUpload={sendAttachment} />
        <MessageInput onSend={(msg) => sendUserMessage(msg, true)} disabled={state.loading} />
      </footer>
      {state.error && <div className="chat-error">{state.error}</div>}
    </div>
  );
};

export default ChatWindow;
```

---

### `frontend/src/components/MessageList/MessageList.tsx`

```tsx
// MessageList.tsx
import React from "react";
import { Message } from "../../context/ChatContext";
import MessageItem from "./MessageItem";

interface Props {
  messages: Message[];
}

const MessageList: React.FC<Props> = ({ messages }) => {
  return (
    <ul className="message-list" aria-label="Chat history">
      {messages.map((m) => (
        <MessageItem key={m.id} message={m} />
      ))}
    </ul>
  );
};

export default MessageList;
```

### `frontend/src/components/MessageList/MessageItem.tsx`

```tsx
// MessageItem.tsx
import React from "react";
import { Message } from "../../context/ChatContext";

interface Props {
  message: Message;
}

const MessageItem: React.FC<Props> = ({ message }) => {
  const isUser = message.sender === "user";
  return (
    <li className={`message-item ${isUser ? "user" : "agent"}`}>
      <div className="bubble">
        <p>{message.content}</p>
      </div>
      <time className="timestamp" dateTime={new Date(message.timestamp).toISOString()}>
        {new Date(message.timestamp).toLocaleTimeString()}
      </time>
    </li>
  );
};

export default MessageItem;
```

---

### `frontend/src/components/MessageInput/MessageInput.tsx`

```tsx
// MessageInput.tsx
import React, { useState } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const MessageInput: React.FC<Props> = ({ onSend, disabled }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      onSend(text.trim());
      setText("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (!disabled && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="message-input">
      <textarea
        className="input-field"
        placeholder="Type your message"
        value={text}
        disabled={disabled}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
      />
      <button className="send-button" onClick={handleSend} disabled={disabled}>
        Send
      </button>
    </div>
  );
};

export default MessageInput;
```

---

### `frontend/src/components/AttachmentUploader/AttachmentUploader.tsx`

```tsx
// AttachmentUploader.tsx
import React, { ChangeEvent, useRef } from "react";

interface Props {
  onUpload: (file: File) => void;
}

const AttachmentUploader: React.FC<Props> = ({ onUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="attachment-uploader">
      <button className="upload-button" onClick={handleClick}>
        📎
      </button>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleChange}
        accept=".pdf,.docx,.png,.jpg"
        style={{ display: "none" }}
      />
    </div>
  );
};

export default AttachmentUploader;
```

---

### `frontend/src/components/TypingIndicator/TypingIndicator.tsx`

```tsx
// TypingIndicator.tsx
import React from "react";

const TypingIndicator: React.FC = () => {
  return (
    <div className="typing-indicator">
      <div className="dot dot1" />
      <div className="dot dot2" />
      <div className="dot dot3" />
    </div>
  );
};

export default TypingIndicator;
```

---

### `frontend/src/components/ClearChatButton/ClearChatButton.tsx`

```tsx
// ClearChatButton.tsx
import React from "react";

interface Props {
  onClear: () => void;
}

const ClearChatButton: React.FC<Props> = ({ onClear }) => {
  return (
    <button className="clear-chat-button" onClick={() => {
      if (window.confirm("Clear chat and start new session?")) {
        onClear();
      }
    }}>
      Clear Chat
    </button>
  );
};

export default ClearChatButton;
```

---

### `frontend/src/styles/index.css`

```css
/* index.css – Apple-brand style */
:root {
  --font-system: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", sans-serif;
  --bg-color: #ffffff;
  --text-color: #1d1d1f;
  --agent-bubble: #f2f2f7;
  --user-bubble: #0a84ff;
  --user-bubble-text: #ffffff;
  --bubble-radius: 18px;
  --spacing-base: 16px;
}

body {
  margin: 0;
  padding: 0;
  font-family: var(--font-system);
  background-color: var(--bg-color);
  color: var(--text-color);
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: var(--spacing-base);
  font-size: 20pt;
  font-weight: 600;
  border-bottom: 1px solid #e0e0e0;
}

.chat-body {
  flex: 1;
  padding: var(--spacing-base);
  overflow-y: auto;
  background: #f9f9fb;
}

.message-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.message-item {
  margin-bottom: var(--spacing-base);
  display: flex;
  flex-direction: column;
}

.message-item.user {
  align-items: flex-end;
}

.message-item.agent {
  align-items: flex-start;
}

.bubble {
  max-width: 70%;
  padding: var(--spacing-base);
  border-radius: var(--bubble-radius);
  line-height: 1.4;
}

.message-item.agent .bubble {
  background: var(--agent-bubble);
  color: var(--text-color);
}

.message-item.user .bubble {
  background: var(--user-bubble);
  color: var(--user-bubble-text);
}

.timestamp {
  margin-top: 4px;
  font-size: 10pt;
  color: #8e8e93;
}

.chat-input-area {
  padding: var(--spacing-base);
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}

.message-input {
  flex: 1;
  display: flex;
  align-items: center;
}

.input-field {
  flex: 1;
  padding: var(--spacing-base);
  border: 1px solid #d1d1d6;
  border-radius: var(--bubble-radius);
  font-size: 14pt;
  resize: none;
  font-family: var(--font-system);
}

.send-button {
  margin-left: var(--spacing-base);
  padding: var(--spacing-base);
  background: var(--user-bubble);
  border: none;
  color: var(--user-bubble-text);
  border-radius: var(--bubble-radius);
  font-size: 14pt;
  cursor: pointer;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: default;
}

.attachment-uploader .upload-button {
  margin-right: var(--spacing-base);
  padding: var(--spacing-base);
  background: transparent;
  border: none;
  font-size: 20pt;
  cursor: pointer;
}

.typing-indicator {
  display: flex;
  align-items: center;
  margin-top: var(--spacing-base)/2;
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
  background-color: #8e8e93;
  animation: blink 1.4s infinite both;
}

.typing-indicator .dot1 { animation-delay: 0s; }
.typing-indicator .dot2 { animation-delay: 0.2s; }
.typing-indicator .dot3 { animation-delay: 0.4s; }

@keyframes blink {
  0%, 80%, 100% { opacity: 0.2; }
  40% { opacity: 1; }
}

.clear-chat-button {
  background: transparent;
  border: none;
  color: var(--text-color);
  font-size: 14pt;
  cursor: pointer;
}

@media (max-width: 600px) {
  .bubble { max-width: 90%; }
  .chat-header { font-size: 18pt; }
  .send-button { font-size: 12pt; padding: 12px; }
}
```

---

### `frontend/src/App.tsx`

```tsx
// App.tsx
import React from "react";
import { ChatProvider } from "./context/ChatContext";
import ChatWindow from "./components/ChatWindow/ChatWindow";

const App: React.FC = () => {
  return (
    <ChatProvider>
      <div className="app-container">
        <ChatWindow />
      </div>
    </ChatProvider>
  );
};

export default App;
```

### `frontend/src/index.tsx`

```tsx
// index.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
```

---

### `frontend/README.md`

````markdown
# Frontend – Customer Support AI Agent

This is the React (TypeScript) frontend application for the Customer Support AI Agent.

## Apple-Brand Style UI/UX  
The UI is designed with inspiration from Apple’s Human Interface Guidelines: minimal, high-contrast, generous spacing, San Francisco system font. :contentReference[oaicite:0]{index=0}  

## Getting Started  
### Prerequisites  
- Node.js (16.x or higher)  
- npm or yarn  
- Backend service running (see root README)  

### Install  
```bash
cd frontend
npm install
````

### Run in development

```bash
npm run dev
```

### Build for production

```bash
npm run build
```

### Configure API Base URL

Set `VITE_API_BASE_URL` in `.env` file (e.g., `VITE_API_BASE_URL=http://localhost:8000`)

## Folder Structure

```
src/
├── api/             # HTTP and SSE client for backend
├── components/      # UI components: ChatWindow, MessageList, etc.
├── context/         # React Context for chat state
├── hooks/           # Custom hooks
├── styles/          # Global styles (Apple-style theme)
├── utils/           # Utility functions (session management, etc.)
└── App.tsx, index.tsx
```

## Testing

```bash
npm test
```

(Uses Jest + React Testing Library)

## Contributing

* Use `eslint` + `prettier`.
* Follow TypeScript strict typing.
* Create feature branches, include tests.

```

---

::contentReference[oaicite:1]{index=1}
```
