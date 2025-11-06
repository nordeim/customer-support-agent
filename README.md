# Customer Support AI Agent

<div align="center">

![Customer Support AI Agent](https://img.shields.io/badge/Customer%20Support-AI%20Agent-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-109989?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=for-the-badge&logo=postgresql)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Intelligent customer support automation powered by Microsoft Agent Framework and RAG**

[![Deploy to Production](https://img.shields.io/badge/Deploy-Production Ready-success?style=for-the-badge)](https://github.com/nordeim/customer-support-agent/deploy)
[![API Documentation](https://img.shields.io/badge/API-Documented-blue?style=for-the-badge)](docs/api.md)
[![Architecture Guide](https://img.shields.io/badge/Architecture-Documented-purple?style=for-the-badge)](docs/architecture.md)

</div>

---

## 🚀 Features

### Core Capabilities
- **🤖 Intelligent Conversations**: Context-aware dialogue management using Microsoft Agent Framework
- **📚 Knowledge Base Integration**: RAG implementation with Chroma vector database and EmbeddingGemma-300m
- **📎 Attachment Processing**: Support for document uploads with Markitdown parsing
- **🧠 Memory System**: SQLite-based persistent memory for conversation context
- **⚡ Escalation Mechanism**: Automatic escalation to human agents when needed
- **🌐 Multi-Channel Support**: RESTful API with WebSocket support for real-time communication
- **📊 Comprehensive Monitoring**: Prometheus metrics and Grafana dashboards
- **🚀 Production-Ready**: Docker containerization with CI/CD pipeline

### Business Value
- **⏱️ Reduced Response Time**: Instant responses to common queries
- **🌙 24/7 Availability**: Round-the-clock support without human intervention
- **📈 Consistent Quality**: Standardized responses regardless of agent availability
- **💰 Cost Efficiency**: Reduced operational costs through automation
- **📈 Scalability**: Handle increasing customer volumes without additional resources
- **📊 Data Insights**: Analytics on customer queries and satisfaction

---

## 🛠 Technology Stack

<div align="center">

### Frontend
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react) 
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript) 
![CSS Modules](https://img.shields.io/badge/CSS%20Modules-Latest-000000?style=flat-square)

### Backend  
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-109989?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python)
![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-Latest-0078D4?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Latest-FF6B6B?style=flat-square)

### Database & Storage
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat-square&logo=postgresql)
![SQLite](https://img.shields.io/badge/SQLite-Latest-003B57?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-Latest-DC382D?style=flat-square&logo=redis)
![Chroma](https://img.shields.io/badge/Chroma-Latest-8B5CF6?style=flat-square)

### AI/ML Components
![EmbeddingGemma-300m](https://img.shields.io/badge/EmbeddingGemma--300m-Google-4285F4?style=flat-square)
![Markitdown](https://img.shields.io/badge/Markitdown-Latest-FF6B6B?style=flat-square)

### Infrastructure & Monitoring
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Latest-2088FF?style=flat-square&logo=github)
![Prometheus](https://img.shields.io/badge/Prometheus-Latest-E6522C?style=flat-square&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Latest-F46800?style=flat-square&logo=grafana)

</div>

---

## 🏗 Architecture Overview

The Customer Support AI Agent implements a **microservices architecture** with clear separation of concerns, ensuring scalability, maintainability, and reliability. The system consists of:

- **React Frontend**: Modern, responsive user interface with real-time communication
- **FastAPI Backend**: High-performance API server with async capabilities  
- **Microsoft Agent Framework**: Intelligent agent orchestration and tool management
- **PostgreSQL**: Primary database for user data and conversation persistence
- **SQLite**: Development database for lightweight operations
- **Redis**: High-performance caching and session management
- **ChromaDB**: Vector database for semantic search and RAG implementation
- **Prometheus + Grafana**: Comprehensive monitoring and observability stack

---

## 📁 Application Architecture

### Complete File Structure

```
customer-support-agent/
├── .github/                          # GitHub Actions CI/CD workflows
│   └── workflows/                    # Automated testing and deployment pipelines
├── backend/                          # FastAPI backend application
│   ├── app/                          # Main application code
│   │   ├── agents/                   # AI agent implementations
│   │   │   ├── agent_factory.py      # Factory for creating different agent types
│   │   │   └── chat_agent.py         # Core chat agent with AI orchestration
│   │   ├── api/                      # API layer and middleware
│   │   │   ├── dependencies.py       # FastAPI dependency injection
│   │   │   ├── middleware.py         # Request/response middleware
│   │   │   └── routes/               # API endpoint definitions
│   │   │       ├── chat.py           # Chat session and message endpoints
│   │   │       ├── health.py         # Health check and status endpoints
│   │   │       └── metrics.py        # Prometheus metrics endpoints
│   │   ├── core/                     # Core application infrastructure
│   │   │   ├── cache.py              # Redis caching implementation
│   │   │   ├── config.py             # Application configuration management
│   │   │   ├── logging.py            # Structured logging setup
│   │   │   └── security.py           # JWT authentication and security
│   │   ├── db/                       # Database layer
│   │   │   ├── database.py           # SQLAlchemy database connection
│   │   │   ├── migrations/           # Alembic database migrations
│   │   │   └── models.py             # Database schema models
│   │   ├── tools/                    # Agent tools and utilities
│   │   │   ├── attachment_tool.py    # Document attachment processing
│   │   │   ├── escalation_tool.py    # Human agent escalation mechanism
│   │   │   ├── memory_tool.py        # Conversation memory management
│   │   │   └── rag_tool.py           # Retrieval-Augmented Generation
│   │   ├── vector_store/             # Vector database integration
│   │   │   ├── chroma_client.py      # ChromaDB client for vector search
│   │   │   └── embeddings.py         # EmbeddingGemma-300m integration
│   │   └── main.py                   # FastAPI application entry point
│   ├── scripts/                      # Deployment and utility scripts
│   │   ├── deploy.sh                 # Production deployment automation
│   │   ├── init_db.py                # Database initialization
│   │   ├── populate_kb.py            # Knowledge base population
│   │   └── rollback.sh               # Deployment rollback procedures
│   ├── tests/                        # Comprehensive test suite
│   │   ├── unit/                     # Unit tests for individual components
│   │   ├── integration/              # Integration tests for API endpoints
│   │   └── e2e/                      # End-to-end testing scenarios
│   ├── Dockerfile                    # Backend containerization configuration
│   ├── docker-compose.yml            # Development Docker Compose setup
│   └── requirements.txt              # Python dependencies specification
├── frontend/                         # React TypeScript frontend
│   ├── public/                       # Static assets
│   │   └── index.html                # Main HTML template
│   ├── src/                          # Source code
│   │   ├── components/               # React UI components
│   │   │   ├── AttachmentUpload/     # File upload component
│   │   │   ├── ChatWindow/           # Main chat interface
│   │   │   ├── EscalationNotice/     # Human agent escalation UI
│   │   │   ├── Message/              # Individual message component
│   │   │   ├── MessageInput/         # Message input interface
│   │   │   ├── SourceCitation/       # AI response citation display
│   │   │   └── TypingIndicator/      # Real-time typing status
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useChat.ts            # Chat state management
│   │   │   ├── useLocalStorage.ts    # Local storage persistence
│   │   │   └── useWebSocket.ts       # WebSocket connection management
│   │   ├── services/                 # API and external service clients
│   │   │   ├── api.ts                # REST API client
│   │   │   ├── storage.ts            # Local storage service
│   │   │   └── websocket.ts          # WebSocket communication
│   │   ├── types/                    # TypeScript type definitions
│   │   │   ├── api.ts                # API response types
│   │   │   ├── chat.ts               # Chat-related types
│   │   │   └── index.ts              # Main type exports
│   │   ├── utils/                    # Utility functions
│   │   │   ├── constants.ts          # Application constants
│   │   │   ├── helpers.ts            # General helper functions
│   │   │   └── validation.ts         # Input validation utilities
│   │   ├── App.tsx                   # Main React application component
│   │   └── index.tsx                 # Application entry point
│   ├── Dockerfile                    # Frontend containerization
│   ├── package.json                  # Node.js dependencies and scripts
│   └── tsconfig.json                 # TypeScript configuration
├── monitoring/                       # Observability and monitoring stack
│   ├── prometheus/                   # Metrics collection configuration
│   │   ├── prometheus.yml            # Main Prometheus configuration
│   │   └── rules/                    # Alert and recording rules
│   ├── grafana/                      # Visualization and dashboards
│   │   ├── provisioning/             # Grafana provisioning configuration
│   │   └── dashboards/               # Pre-configured dashboards
│   └── alertmanager/                 # Alert management
│       └── alertmanager.yml          # Alert routing configuration
├── docs/                             # Comprehensive documentation
│   ├── api.md                        # API endpoint documentation
│   ├── architecture.md               # Detailed architecture documentation
│   └── deployment.md                 # Deployment guide
├── scripts/                          # Root-level utility scripts
├── .env.example                      # Environment variables template
├── .env.prod                         # Production environment configuration
├── .gitignore                        # Git ignore patterns
├── CLAUDE.md                         # AI development guidelines
├── DB_initialization_examples.txt    # Database setup examples
├── Deployment_Checklist.md           # Production deployment checklist
├── Design_Decisions_Document.md      # Architecture decision records
├── GEMINI.md                         # Gemini model documentation
├── KB_loading_examples.txt           # Knowledge base loading examples
├── Minor_Discrepancies_and_Areas_for_Refinement.md # Known issues
├── Project_Architecture_Document.md  # Complete architecture documentation
├── README.md                         # This comprehensive README
├── Runbook.md                        # Operations runbook
├── codebase_review.md                # Code quality review
├── docker-compose.prod.yml           # Production Docker Compose
├── docker-compose.yml                # Development Docker Compose
├── file_structure.txt                # This file structure documentation
└── grafana_dashboard.json            # Pre-configured Grafana dashboards
```

---

## 🔄 User-Application Interaction Flow

### Complete User Journey

```mermaid
flowchart TD
    %% User Entry Points
    User[👤 User] --> WebApp[🌐 Chat Interface]
    
    %% Session Management
    WebApp --> SessionCheck{📋 Session Exists?}
    SessionCheck -->|No| CreateSession[🔄 Create New Session]
    CreateSession --> StoreSession[💾 Store in PostgreSQL]
    SessionCheck -->|Yes| SendMessage[💬 Send Message]
    StoreSession --> SendMessage
    
    %% Message Submission
    SendMessage --> WebSocketCheck{🔌 WebSocket Available?}
    WebSocketCheck -->|Yes| WebSocket[📡 Real-time WebSocket]
    WebSocketCheck -->|No| RESTAPI[📡 REST API]
    WebSocket --> Backend[⚡ FastAPI Backend]
    RESTAPI --> Backend
    
    %% Attachment Processing
    Backend --> AttachmentCheck{📎 Attachments?}
    AttachmentCheck -->|Yes| ProcessAttachment[📄 Process with Markitdown]
    AttachmentCheck -->|No| ContextRetrieval[🔍 Retrieve Context]
    ProcessAttachment --> ContextRetrieval
    
    %% Context & Memory
    ContextRetrieval --> RedisCache{⚡ Redis Cache Hit?}
    RedisCache -->|Yes| GetCachedContext[📦 Get Cached Context]
    RedisCache -->|No| GetDBContext[📊 Get from PostgreSQL]
    GetCachedContext --> AgentContext[🧠 Prepare Agent Context]
    GetDBContext --> AgentContext
    
    %% AI Agent Orchestration
    AgentContext --> EmbeddingCheck{🔤 Need Embeddings?}
    EmbeddingCheck -->|Yes| GenerateEmbedding[🧮 Generate EmbeddingGemma-300m]
    EmbeddingCheck -->|No| VectorSearch[🔍 Chroma Vector Search]
    GenerateEmbedding --> VectorSearch
    
    %% Vector Database Search
    VectorSearch --> ChromaDB[(🗄️ Chroma Vector DB)]
    ChromaDB --> SimilaritySearch[🎯 Similarity Search]
    SimilaritySearch --> TopKCheck{📊 Top-K Results?}
    TopKCheck -->|Yes| RetrieveDocs[📑 Retrieve Documents]
    TopKCheck -->|No| NoResults[🚫 No Relevant Docs]
    
    %% Agent Framework Processing
    RetrieveDocs --> AgentFramework[🤖 Microsoft Agent Framework]
    NoResults --> AgentFramework
    
    %% Decision Points
    AgentFramework --> EscalationCheck{❗ Escalation Needed?}
    
    %% Escalation Path
    EscalationCheck -->|Yes| EscalationTicket[🎫 Create Escalation Ticket]
    EscalationTicket --> HumanAgent[👨‍💼 Human Agent]
    HumanAgent --> EscalationResponse[📝 Manual Response]
    EscalationResponse --> StoreResponse[💾 Store Response]
    
    %% AI Response Path
    EscalationCheck -->|No| AIResponse[🤖 Generate AI Response]
    AIResponse --> GenerateCitations[📚 Generate Citations]
    GenerateCitations --> StoreResponse
    
    %% Response Storage
    StoreResponse --> MemoryUpdate[🔄 Update Conversation Memory]
    MemoryUpdate --> CacheUpdate[⚡ Update Redis Cache]
    CacheUpdate --> MetricsUpdate[📊 Update Prometheus Metrics]
    MetricsUpdate --> LogInteraction[📝 Structured Logging]
    
    %% Response Delivery
    LogInteraction --> ResponseCheck{📡 Response Channel?}
    ResponseCheck -->|WebSocket| WebSocketSend[📡 Send via WebSocket]
    ResponseCheck -->|REST| HTTPReturn[📡 HTTP Response]
    WebSocketSend --> WebApp
    HTTPReturn --> WebApp
    
    %% Display Response
    WebApp --> DisplayCheck{🎨 Response Type?}
    DisplayCheck -->|Citation| ShowCitation[📚 Display Sources]
    DisplayCheck -->|Escalation| ShowEscalation[🎫 Show Escalation Notice]
    DisplayCheck -->|Regular| ShowMessage[💬 Show AI Message]
    
    ShowCitation --> User
    ShowEscalation --> User
    ShowMessage --> User
    
    %% Monitoring & Analytics
    LogInteraction --> MonitoringStack[📊 Monitoring Stack]
    MonitoringStack --> Prometheus[(📈 Prometheus Metrics)]
    MonitoringStack --> Grafana[📉 Grafana Dashboards]
    
    %% Styling
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef frontendClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef backendClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef databaseClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef aiClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef decisionClass fill:#fff8e1,stroke:#f57f17,stroke-width:2px
    
    class User userClass
    class WebApp,SendMessage,DisplayCheck frontendClass
    class Backend,AgentFramework,ProcessAttachment backendClass
    class PostgreSQL,RedisCache,ChromaDB,StoreResponse databaseClass
    class AIResponse,AgentContext,GenerateEmbedding,VectorSearch aiClass
    class SessionCheck,WebSocketCheck,AttachmentCheck,EscalationCheck,ResponseCheck decisionClass
```

### Interaction Flow Description

#### 1. **Session Initialization**
- User accesses chat interface
- System checks for existing session
- Creates new session if none exists
- Stores session in PostgreSQL database

#### 2. **Message Submission**
- User sends message with optional attachments
- Frontend checks for WebSocket availability
- Falls back to REST API if WebSocket unavailable
- Sends message to FastAPI backend

#### 3. **Context Retrieval & RAG**
- System retrieves conversation history from PostgreSQL
- Generates embeddings using EmbeddingGemma-300m
- Performs similarity search in Chroma vector database
- Retrieves top-K most relevant documents

#### 4. **AI Agent Processing**
- Microsoft Agent Framework processes the query
- Uses retrieved context and documents
- Considers conversation history and user intent

#### 5. **Response Generation**
- **Escalation Path**: If escalation needed, creates ticket for human agent
- **AI Response Path**: Generates AI-powered response with citations
- Both paths store responses in database for conversation continuity

#### 6. **Response Delivery**
- Response sent back via WebSocket or REST API
- Frontend displays appropriate interface (citations, escalation notice, or message)
- User receives real-time or immediate response

---

## 🧠 Application Logic Flow

### Internal Processing Pipeline

```mermaid
flowchart TD
    %% Input Processing
    ReceiveMessage[📨 Receive User Message] --> ValidateInput[✅ Validate Input]
    ValidateInput --> RateLimitCheck{⚡ Rate Limited?}
    RateLimitCheck -->|Yes| RejectRequest[🚫 Reject Request]
    RateLimitCheck -->|No| Authenticate[🔐 Authenticate User]
    
    %% Authentication & Session
    Authenticate --> JWTVerify[🛡️ Verify JWT Token]
    JWTVerify --> SessionLookup[📋 Lookup Session]
    SessionLookup --> SessionCheck{📊 Session Valid?}
    SessionCheck -->|No| CreateNewSession[🔄 Create New Session]
    SessionCheck -->|Yes| RetrieveHistory[📚 Retrieve Conversation History]
    CreateNewSession --> RetrieveHistory
    
    %% Message Processing
    RetrieveHistory --> ProcessAttachments{📎 Attachments?}
    ProcessAttachments -->|Yes| MarkitdownParse[📄 Parse with Markitdown]
    ProcessAttachments -->|No| ContextPreparation[🧠 Prepare Context]
    MarkitdownParse --> ContextPreparation
    
    %% Context Building
    ContextPreparation --> HistoricalContext[📖 Historical Context]
    HistoricalContext --> UserContext[👤 User Context]
    UserContext --> AttachmentContext[📎 Attachment Context]
    AttachmentContext --> SystemContext[⚙️ System Context]
    SystemContext --> CombineContext[🔗 Combine All Context]
    
    %% RAG Implementation
    CombineContext --> GenerateQueryEmbed[🧮 Generate Query Embedding]
    GenerateQueryEmbed --> ChromaConnection[🔌 Connect to ChromaDB]
    ChromaConnection --> VectorSimilarity[🎯 Vector Similarity Search]
    VectorSimilarity --> RelevanceFilter[📊 Filter by Relevance]
    RelevanceFilter --> DocumentRetrieval[📑 Retrieve Documents]
    DocumentRetrieval --> DocumentRanking[🏆 Rank by Relevance]
    
    %% Agent Framework Preparation
    DocumentRanking --> ToolPreparation[🛠️ Prepare Agent Tools]
    ToolPreparation --> InstructionTemplate[📝 Load Instruction Template]
    InstructionTemplate --> ContextWindow[🪟 Build Context Window]
    ContextWindow --> AgentInit[🤖 Initialize Agent Framework]
    
    %% Agent Execution
    AgentInit --> ToolExecution[⚡ Execute Agent Tools]
    ToolExecution --> RAGToolCall[🔍 Call RAG Tool]
    ToolExecution --> MemoryToolCall[🧠 Call Memory Tool]
    ToolExecution --> EscalationToolCall[⚠️ Call Escalation Tool]
    ToolExecution --> AttachmentToolCall[📎 Call Attachment Tool]
    
    %% Decision Logic
    RAGToolCall --> EscalationCheck{❗ Escalation Required?}
    MemoryToolCall --> EscalationCheck
    EscalationToolCall --> EscalationCheck
    AttachmentToolCall --> EscalationCheck
    
    %% Escalation Path
    EscalationCheck -->|Yes| CreateEscalation[🎫 Create Escalation Ticket]
    CreateEscalation --> TicketAssignment[👤 Assign to Human Agent]
    TicketAssignment --> EscalationResponse[📝 Generate Escalation Response]
    EscalationResponse --> ResponseFormatting[🎨 Format Response]
    
    %% AI Response Path
    EscalationCheck -->|No| ProcessRAGResults[🔍 Process RAG Results]
    ProcessRAGResults --> ResponseGeneration[🤖 Generate AI Response]
    ResponseGeneration --> SourceCitation[📚 Add Source Citations]
    SourceCitation --> ResponseValidation[✅ Validate Response]
    ResponseValidation --> ResponseFormatting
    
    %% Response Processing
    ResponseFormatting --> ResponseOptimization[⚡ Optimize for Delivery]
    ResponseOptimization --> CacheResponse[💾 Cache Response]
    CacheResponse --> DatabaseUpdate[📊 Update Database]
    
    %% Database Operations
    DatabaseUpdate --> StoreConversation[💬 Store Conversation]
    StoreConversation --> UpdateSession[🔄 Update Session]
    UpdateSession --> RecordMetrics[📊 Record Metrics]
    RecordMetrics --> UpdateMemory[🧠 Update Memory]
    
    %% Monitoring & Logging
    UpdateMemory --> StructuredLogging[📝 Structured Logging]
    StructuredLogging --> PerformanceMetrics[⏱️ Performance Metrics]
    PerformanceMetrics --> ErrorHandling{⚠️ Errors?}
    ErrorHandling -->|Yes| ErrorLogging[🚨 Log Errors]
    ErrorHandling -->|No| SuccessMetrics[✅ Success Metrics]
    ErrorLogging --> HealthCheck[💓 Update Health Status]
    SuccessMetrics --> HealthCheck
    
    %% Response Delivery
    HealthCheck --> ResponseDelivery[📡 Prepare Response Delivery]
    ResponseDelivery --> WebSocketCheck{🔌 WebSocket?}
    WebSocketCheck -->|Yes| SendWebSocket[📡 Send via WebSocket]
    WebSocketCheck -->|No| SendHTTP[📡 Send via HTTP]
    SendWebSocket --> End[🏁 End]
    SendHTTP --> End
    
    %% Rejection Path
    RejectRequest --> RateLimitResponse[⏰ Rate Limit Response]
    RateLimitResponse --> End
    
    %% Styling
    classDef inputClass fill:#e3f2fd,stroke:#0277bd,stroke-width:2px
    classDef authClass fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef contextClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef ragClass fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef agentClass fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef decisionClass fill:#fff8e1,stroke:#ffa000,stroke-width:2px
    classDef responseClass fill:#f1f8e9,stroke:#689f38,stroke-width:2px
    classDef databaseClass fill:#fce4ec,stroke:#d32f2f,stroke-width:2px
    classDef monitoringClass fill:#e0f2f1,stroke:#00796b,stroke-width:2px
    classDef errorClass fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class ReceiveMessage,ValidateInput,Authenticate inputClass
    class JWTVerify,SessionLookup,CreateNewSession authClass
    class ContextPreparation,CombineContext,ContextWindow contextClass
    class GenerateQueryEmbed,VectorSimilarity,DocumentRetrieval ragClass
    class AgentInit,ToolExecution,ResponseGeneration agentClass
    class EscalationCheck,WebSocketCheck,ProcessAttachments decisionClass
    class ResponseFormatting,ResponseDelivery responseClass
    class StoreConversation,UpdateSession,DatabaseUpdate databaseClass
    class StructuredLogging,PerformanceMetrics,HealthCheck monitoringClass
    class ErrorLogging,RateLimitResponse,RejectRequest errorClass
```

### Key Technical Components

1. **Embedding Generation**: EmbeddingGemma-300m model integration
2. **Vector Database**: ChromaDB for similarity search and retrieval
3. **Agent Orchestration**: Microsoft Agent Framework for tool management
4. **Memory System**: SQLite-based conversation memory with PostgreSQL persistence
5. **Caching Layer**: Redis for performance optimization
6. **Document Processing**: Markitdown for attachment parsing
7. **Authentication**: JWT-based security with session management
8. **Monitoring**: Prometheus metrics collection and Grafana visualization

---

## ⚡ Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4GB+ RAM available
- 10GB+ disk space

### Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/nordeim/customer-support-agent.git
cd customer-support-agent

# 2. Environment setup
cp .env.example .env
# Edit .env with your configuration

# 3. Start all services
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python scripts/init_db.py

# 5. Populate knowledge base (optional)
docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base

# 6. Verify deployment
curl http://localhost:8000/health
```

### Production Deployment

```bash
# 1. Set production environment
export VERSION=1.0.0
export POSTGRES_PASSWORD=your_secure_password
export SECRET_KEY=your_secure_secret_key

# 2. Deploy using automation script
./scripts/deploy.sh

# 3. Check deployment status
./scripts/deploy.sh health
```

---

## 🏭 Production Deployment

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 20GB SSD | 50GB+ SSD |
| **Network** | 100 Mbps | 1 Gbps |

### Environment Configuration

#### Production Environment Variables

```bash
# Core Application
VERSION=1.0.0
DEBUG=false
SECRET_KEY=your-production-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=customer_support
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-postgres-password

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-secure-redis-password

# AI Configuration
EMBEDDING_MODEL_PATH=/app/models/embeddinggemma-300m
CHROMA_PERSIST_DIRECTORY=/app/data/chroma

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ADMIN_PASSWORD=your-grafana-password

# External APIs
OPENAI_API_KEY=your-openai-api-key
MICROSOFT_AGENT_FRAMEWORK_KEY=your-agent-framework-key

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### Deployment Checklist

- [ ] System requirements met
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database initialized and migrated
- [ ] Knowledge base populated
- [ ] Monitoring stack configured
- [ ] Backup procedures tested
- [ ] Security hardening applied
- [ ] Load testing completed
- [ ] Rollback procedures verified

---

## 📊 Monitoring & Observability

### Prometheus Metrics

```bash
# Access Prometheus dashboard
open http://localhost:9090

# Check key metrics
curl 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])'
```

### Grafana Dashboards

```bash
# Access Grafana (admin/admin)
open http://localhost:3000

# Key performance indicators:
# - Response time percentiles
# - Conversation success rate
# - Escalation frequency
# - System resource usage
# - Error rates and types
```

### Key Monitoring Metrics

```yaml
# Application Metrics
- response_time_seconds
- http_requests_total
- active_sessions
- conversation_count
- escalation_rate

# System Metrics
- cpu_usage_percent
- memory_usage_percent
- disk_usage_percent
- network_io_bytes

# AI/ML Metrics
- embedding_generation_time
- vector_search_latency
- agent_framework_latency
- knowledge_base_hits
```

---

## 🔧 Configuration

### Database Configuration

```python
# Database settings in .env
DATABASE_URL=postgresql://user:password@localhost:5432/customer_support
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
```

### AI Model Configuration

```python
# AI/ML settings
EMBEDDING_MODEL_PATH=/app/models/embeddinggemma-300m
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### Security Configuration

```python
# JWT settings
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

---

## 📚 API Documentation

### Authentication

All API requests require JWT authentication:

```bash
# Get JWT token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### Core Endpoints

#### Chat Sessions

```bash
# Create session
curl -X POST http://localhost:8000/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# Send message
curl -X POST http://localhost:8000/chat/sessions/{session_id}/messages \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my password?"}'
```

#### Health Check

```bash
# System health
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/status
```

#### Metrics

```bash
# Prometheus metrics
curl http://localhost:8000/metrics
```

### WebSocket Connection

```javascript
// Frontend WebSocket example
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Response:', data);
};

ws.send(JSON.stringify({
  session_id: 'session123',
  message: 'Hello, I need help'
}));
```

---

## 🧪 Development

### Local Development Setup

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend development
cd frontend
npm install
npm run dev
```

### Testing

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Load testing
artillery run load-test.yml
```

### Code Quality

```bash
# Python linting
docker-compose exec backend flake8 app/
docker-compose exec backend black app/
docker-compose exec backend isort app/

# TypeScript linting
cd frontend
npm run lint
npm run type-check
```

---

## 🔒 Security

### Security Features

- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Protection against abuse and DDoS
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: ORM-based database queries
- **CORS Configuration**: Proper cross-origin resource sharing
- **HTTPS/TLS**: Encrypted communication
- **Environment Variables**: Secure configuration management

### Security Checklist

- [ ] Change all default passwords
- [ ] Use strong JWT secrets
- [ ] Enable SSL/TLS in production
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up security monitoring
- [ ] Regular security updates
- [ ] Access logging enabled
- [ ] Vulnerability scanning
- [ ] Security audit completed

---

## 🚨 Troubleshooting

### Common Issues

#### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common solutions:
# 1. Database connection
docker-compose exec backend python -c "from app.db.database import engine; print('DB OK')"

# 2. Environment variables
docker-compose exec backend env | grep DATABASE_URL
```

#### High Memory Usage

```bash
# Monitor container usage
docker stats

# Clear ChromaDB cache
docker-compose exec backend python -c "from app.vector_store.chroma_client import clear_cache; clear_cache()"

# Restart backend
docker-compose restart backend
```

#### Knowledge Base Issues

```bash
# Verify ChromaDB setup
docker-compose exec backend python -c "
from app.vector_store.chroma_client import chroma_client
collections = chroma_client.list_collections()
print(f'Collections: {collections}')
"

# Re-index documents
docker-compose exec backend python scripts/populate_kb.py --force-reindex
```

---

## 🔄 Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres customer_support > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U postgres customer_support | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 30 backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### Knowledge Base Backup

```bash
# ChromaDB backup
docker run --rm -v customer-support-agent_chroma_data:/data -v $(pwd):/backup alpine tar czf /backup/chroma-backup-$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# Restore ChromaDB
docker run --rm -v customer-support-agent_chroma_data:/data -v $(pwd):/backup alpine tar xzf /backup/chroma-backup-YYYYMMDD_HHMMSS.tar.gz -C /data
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- **Python**: Follow PEP 8, use type hints, docstrings
- **TypeScript**: Follow ESLint configuration, use strict mode
- **Testing**: Maintain >90% test coverage
- **Documentation**: Update docs for new features
- **Security**: Follow security best practices

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Customer Support AI Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Microsoft Agent Framework**: For intelligent agent orchestration
- **Google EmbeddingGemma-300m**: For high-quality embeddings
- **ChromaDB**: For vector database capabilities
- **FastAPI**: For the excellent web framework
- **React**: For the modern frontend framework
- **Docker**: For containerization and deployment
- **Prometheus & Grafana**: For monitoring and observability

---

## 📚 References

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- [EmbeddingGemma Model](https://huggingface.co/google/embeddinggemma-300m)
- [Chroma Vector Database](https://www.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)

---

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/nordeim/customer-support-agent?style=social)](https://github.com/nordeim/customer-support-agent)
[![GitHub forks](https://img.shields.io/github/forks/nordeim/customer-support-agent?style=social)](https://github.com/nordeim/customer-support-agent/fork)
[![GitHub issues](https://img.shields.io/github/issues/nordeim/customer-support-agent)](https://github.com/nordeim/customer-support-agent/issues)
[![GitHub license](https://img.shields.io/github/license/nordeim/customer-support-agent)](https://github.com/nordeim/customer-support-agent/blob/main/LICENSE)

**Built with ❤️ by the Customer Support AI Team**

[Website](https://github.com/nordeim/customer-support-agent) • 
[Documentation](docs/) • 
[API Reference](docs/api.md) • 
[Deployment Guide](docs/deployment.md) • 
[Architecture](docs/architecture.md)

</div>
