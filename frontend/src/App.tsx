// frontend/src/App.tsx
import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import { EscalationInfo } from './types/chat';
import './App.css';

const App: React.FC = () => {
  const [escalationInfo, setEscalationInfo] = useState<EscalationInfo | null>(null);

  const handleEscalation = (info: EscalationInfo) => {
    setEscalationInfo(info);
  };

  const handleError = (error: Error) => {
    console.error('Chat error:', error);
  };

  const closeEscalationNotice = () => {
    setEscalationInfo(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Customer Support Agent</h1>
      </header>
      
      <main className="App-main">
        <ChatWindow
          onEscalation={handleEscalation}
          onError={handleError}
        />
      </main>

      {escalationInfo && (
        <div className="escalation-overlay">
          <div className="escalation-modal">
            <EscalationNotice
              escalationInfo={escalationInfo}
              onClose={closeEscalationNotice}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
