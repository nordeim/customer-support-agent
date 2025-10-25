

# Customer Support AI Agent

![Customer Support AI Agent](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)

A production-ready customer support AI agent that combines the power of Microsoft Agent Framework with Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware customer support.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Customer Support AI Agent is a comprehensive solution designed to automate and enhance customer support interactions. It leverages advanced AI technologies to understand customer queries, retrieve relevant information from a knowledge base, and provide accurate, helpful responses.

### Key Features

- **Intelligent Conversations**: Context-aware dialogue management using Microsoft Agent Framework
- **Knowledge Base Integration**: RAG implementation with Chroma vector database and embeddinggemma-300m model
- **Attachment Processing**: Support for document uploads with markitdown parsing
- **Memory System**: SQLite-based persistent memory for conversation context
- **Escalation Mechanism**: Automatic escalation to human agents when needed
- **Multi-Channel Support**: RESTful API with WebSocket support for real-time communication
- **Comprehensive Monitoring**: Prometheus metrics and Grafana dashboards
- **Production-Ready**: Docker containerization with CI/CD pipeline

### Business Value

- **Reduced Response Time**: Instant responses to common queries
- **24/7 Availability**: Round-the-clock support without human intervention
- **Consistent Quality**: Standardized responses regardless of agent availability
- **Cost Efficiency**: Reduced operational costs through automation
- **Scalability**: Handle increasing customer volumes without additional resources
- **Data Insights**: Analytics on customer queries and satisfaction

## Technology Stack

### Frontend
- **React 18.2.0**: Modern UI framework with hooks and context
- **TypeScript 5.0**: Type-safe JavaScript for better code quality
- **CSS Modules**: Scoped styling for component isolation
- **Axios**: HTTP client for API communication

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12**: Latest stable Python version
- **Microsoft Agent Framework**: AI agent orchestration and tool management
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration tool

### Database and Storage
- **PostgreSQL**: Primary database for production
- **SQLite**: Lightweight database for development and memory
- **Redis**: In-memory caching for performance optimization
- **Chroma**: Vector database for RAG implementation

### AI/ML Components
- **EmbeddingGemma-300m**: Google's embedding model for text vectorization
- **Markitdown**: Document parsing and text extraction
- **RAG Pipeline**: Retrieval-Augmented Generation for knowledge integration

### Monitoring and Observability
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboarding
- **Docker**: Containerization for deployment
- **GitHub Actions**: CI/CD pipeline for automated testing and deployment

## Architecture

### High-Level Architecture

The Customer Support AI Agent follows a microservices architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │  FastAPI Backend│    │  Agent Framework│
│                 │    │                 │    │                 │
│ - Chat Interface│◄──►│ - REST API      │◄──►│ - Tool Execution│
│ - File Upload   │    │ - WebSocket     │    │ - Context Mgmt  │
│ - Message Display│   │ - Authentication│    │ - Reasoning     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   PostgreSQL    │    │     Chroma      │
│                 │    │                 │    │                 │
│ - Load Balancing│    │ - User Data     │    │ - Vector Store  │
│ - SSL Termination│   │ - Conversations │    │ - Embeddings    │
│ - Static Files  │    │ - Memory        │    │ - Similarity    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Redis       │    │   Prometheus    │    │     Grafana     │
│                 │    │                 │    │                 │
│ - Session Cache │    │ - Metrics       │    │ - Dashboards    │
│ - Query Cache   │    │ - Alerting      │    │ - Visualization│
│ - Rate Limiting │    │ - Monitoring    │    │ - Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### File Hierarchy

```
customer-support-agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── chat_agent.py          # Main agent implementation
│   │   │   └── agent_factory.py       # Factory for creating agents
│   │   ├── api/
│   │   │   ├── dependencies.py        # FastAPI dependencies
│   │   │   ├── routes/
│   │   │   │   ├── chat.py            # Chat endpoints
│   │   │   │   ├── health.py          # Health check endpoints
│   │   │   │   └── metrics.py         # Metrics endpoints
│   │   │   └── middleware.py          # Custom middleware
│   │   ├── core/
│   │   │   ├── config.py              # Configuration management
│   │   │   ├── logging.py             # Logging configuration
│   │   │   ├── security.py            # Security utilities
│   │   │   └── cache.py               # Redis caching
│   │   ├── db/
│   │   │   ├── models.py              # SQLAlchemy models
│   │   │   ├── database.py            # Database connection
│   │   │   └── migrations/            # Alembic migration scripts
│   │   ├── tools/
│   │   │   ├── memory_tool.py         # Memory management tool
│   │   │   ├── rag_tool.py            # RAG implementation tool
│   │   │   ├── attachment_tool.py     # Attachment processing tool
│   │   │   └── escalation_tool.py     # Human escalation tool
│   │   ├── vector_store/
│   │   │   ├── chroma_client.py       # ChromaDB client
│   │   │   └── embeddings.py          # Embedding model wrapper
│   │   └── main.py                    # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/                      # Unit tests
│   │   ├── integration/               # Integration tests
│   │   └── e2e/                       # End-to-end tests
│   ├── scripts/
│   │   ├── init_db.py                 # Database initialization
│   │   ├── populate_kb.py             # Knowledge base population
│   │   ├── deploy.sh                  # Deployment script
│   │   └── rollback.sh                # Rollback script
│   ├── Dockerfile                     # Docker configuration
│   ├── requirements.txt               # Python dependencies
│   └── docker-compose.yml             # Docker Compose configuration
├── frontend/
│   ├── public/
│   │   └── index.html                 # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow/            # Chat interface component
│   │   │   ├── Message/               # Message display component
│   │   │   ├── MessageInput/          # Input component
│   │   │   ├── AttachmentUpload/      # File upload component
│   │   │   ├── TypingIndicator/       # Typing indicator component
│   │   │   ├── SourceCitation/        # Source citation component
│   │   │   └── EscalationNotice/      # Escalation notice component
│   │   ├── hooks/
│   │   │   ├── useChat.ts             # Chat state management
│   │   │   ├── useWebSocket.ts        # WebSocket connection
│   │   │   └── useLocalStorage.ts     # Local storage management
│   │   ├── services/
│   │   │   ├── api.ts                 # API client
│   │   │   ├── websocket.ts           # WebSocket client
│   │   │   └── storage.ts             # Storage utilities
│   │   ├── types/
│   │   │   ├── api.ts                 # API type definitions
│   │   │   ├── chat.ts                # Chat type definitions
│   │   │   └── index.ts               # Type exports
│   │   ├── utils/
│   │   │   ├── constants.ts           # Application constants
│   │   │   ├── helpers.ts             # Helper functions
│   │   │   └── validation.ts          # Input validation
│   │   ├── App.tsx                    # Main application component
│   │   └── index.tsx                  # Application entry point
│   ├── package.json                   # NPM configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   └── Dockerfile                     # Docker configuration
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml             # Prometheus configuration
│   │   └── rules/                     # Alerting rules
│   ├── grafana/
│   │   ├── provisioning/              # Grafana provisioning
│   │   └── dashboards/                # Dashboard definitions
│   └── alertmanager/
│       └── alertmanager.yml           # AlertManager configuration
├── docs/
│   ├── api.md                         # API documentation
│   ├── deployment.md                  # Deployment guide
│   └── architecture.md                # Architecture documentation
├── .github/
│   └── workflows/                     # GitHub Actions workflows
├── docker-compose.prod.yml            # Production Docker Compose
├── .env.example                       # Environment variables example
└── README.md                          # This file
```

### User and Application Interaction

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AgentFramework
    participant VectorDB
    participant Database
    participant HumanAgent

    User->>Frontend: Access chat interface
    Frontend->>Backend: Create session
    Backend->>Database: Store session
    Backend-->>Frontend: Return session ID
    
    User->>Frontend: Send message with optional attachments
    Frontend->>Backend: Submit message
    Backend->>Database: Retrieve conversation history
    Backend->>AgentFramework: Process message with context
    
    AgentFramework->>VectorDB: Search for relevant documents
    VectorDB-->>AgentFramework: Return relevant documents
    AgentFramework->>AgentFramework: Generate response with citations
    
    alt Escalation needed
        AgentFramework->>HumanAgent: Create escalation ticket
        AgentFramework-->>Backend: Return escalation response
    else Normal response
        AgentFramework-->>Backend: Return AI response
    end
    
    Backend->>Database: Store conversation
    Backend-->>Frontend: Return response
    Frontend-->>User: Display response with citations
```

### Application Logic Flow

```mermaid
flowchart TD
    A[Receive User Message] --> B[Validate Input]
    B --> C[Retrieve Session Context]
    C --> D[Process Attachments]
    D --> E[Generate Query Embedding]
    E --> F[Search Vector Database]
    F --> G[Retrieve Relevant Documents]
    G --> H[Prepare Agent Context]
    H --> I[Execute Agent Framework]
    I --> J{Escalation Needed?}
    J -->|Yes| K[Create Escalation Ticket]
    J -->|No| L[Generate AI Response]
    K --> M[Store Conversation]
    L --> M
    M --> N[Return Response with Citations]
    N --> O[Update Metrics]
    O --> P[Log Interaction]
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nordeim/customer-support-agent.git
   cd customer-support-agent
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**:
   ```bash
   docker-compose exec backend python scripts/init_db.py
   ```

5. **Populate the knowledge base** (optional):
   ```bash
   docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
   ```

### Running the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Dashboard**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

### Basic Usage Example

```python
import requests

# Create a session
response = requests.post("http://localhost:8000/chat/sessions", 
                         json={"user_id": "user123"})
session_id = response.json()["session_id"]

# Send a message
response = requests.post(f"http://localhost:8000/chat/sessions/{session_id}/messages",
                         data={"message": "How do I reset my password?"})

# Get the response
data = response.json()
print(f"Agent: {data['message']}")
print(f"Sources: {data['sources']}")
```

## Deployment

### Development Deployment

For development, use the provided Docker Compose configuration:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

For production deployment, use the production Docker Compose configuration:

```bash
# Set environment variables
export VERSION=1.0.0
export POSTGRES_PASSWORD=your_secure_password
export SECRET_KEY=your_secure_secret_key

# Deploy
./scripts/deploy.sh

# Check deployment status
./scripts/deploy.sh health
```

### Environment Variables

Key environment variables for production:

```bash
# Application
VERSION=1.0.0
SECRET_KEY=your_very_secure_secret_key
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/customer_support

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Agent Framework
AGENT_FRAMEWORK_ENDPOINT=https://your-agent-framework.com
AGENT_FRAMEWORK_API_KEY=your_api_key

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=your_grafana_password
```

### Docker Deployment

Build and deploy with Docker:

```bash
# Build images
docker build -t customer-support-backend:latest ./backend
docker build -t customer-support-frontend:latest ./frontend

# Run with production configuration
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment Options

#### AWS

1. **ECS/EKS**: Deploy containers to Amazon ECS or EKS
2. **RDS**: Use Amazon RDS for PostgreSQL
3. **ElastiCache**: Use Amazon ElastiCache for Redis
4. **Application Load Balancer**: For load balancing and SSL termination

#### Azure

1. **Container Instances**: Deploy to Azure Container Instances
2. **Azure Database for PostgreSQL**: Managed PostgreSQL service
3. **Azure Cache for Redis**: Managed Redis service
4. **Application Gateway**: For load balancing and SSL termination

#### Google Cloud

1. **Cloud Run**: Deploy containers to Cloud Run
2. **Cloud SQL**: Use Cloud SQL for PostgreSQL
3. **Memorystore**: Use Memorystore for Redis
4. **Cloud Load Balancing**: For load balancing and SSL termination

### Scaling Considerations

- **Horizontal Scaling**: Add more backend instances behind a load balancer
- **Database Scaling**: Use read replicas for read-heavy workloads
- **Caching**: Implement Redis caching for frequently accessed data
- **CDN**: Use a CDN for static assets
- **Auto-scaling**: Configure auto-scaling based on CPU/memory metrics

## API Documentation

### Authentication

The API uses JWT tokens for authentication:

```python
# Get a token
response = requests.post("http://localhost:8000/auth/login", 
                         json={"username": "user", "password": "password"})
token = response.json()["access_token"]

# Use the token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/protected", headers=headers)
```

### Endpoints

#### Chat Sessions

- `POST /chat/sessions`: Create a new chat session
- `GET /chat/sessions/{session_id}/history`: Get chat history
- `POST /chat/sessions/{session_id}/messages`: Send a message

#### Health Checks

- `GET /health/`: Basic health check
- `GET /health/detailed`: Detailed health check
- `GET /health/readiness`: Readiness check for Kubernetes
- `GET /health/liveness`: Liveness check for Kubernetes

#### Metrics

- `GET /metrics`: Prometheus metrics endpoint

### Request/Response Examples

#### Create Session

```bash
curl -X POST "http://localhost:8000/chat/sessions" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123"}'
```

Response:
```json
{
  "session_id": "uuid-string",
  "thread_id": "thread-uuid",
  "message": "Session created successfully"
}
```

#### Send Message

```bash
curl -X POST "http://localhost:8000/chat/sessions/uuid-string/messages" \
     -F "message=How do I reset my password?" \
     -F "attachments=@document.pdf"
```

Response:
```json
{
  "message": "To reset your password, follow these steps...",
  "sources": [
    {
      "id": "doc1",
      "content": "Password reset instructions...",
      "metadata": {"source": "password-reset.pdf"},
      "distance": 0.15
    }
  ],
  "requires_escalation": false
}
```

### Error Handling

The API returns appropriate HTTP status codes and error messages:

```json
{
  "detail": "Session not found"
}
```

### Rate Limiting

The API implements rate limiting to prevent abuse:

- Session creation: 5 requests per minute
- Message sending: 30 requests per minute
- Health checks: 60 requests per minute

## Configuration

### Environment Variables

See the [Deployment](#deployment) section for a list of environment variables.

### Configuration Files

- `backend/app/core/config.py`: Backend configuration
- `frontend/src/config.ts`: Frontend configuration
- `monitoring/prometheus/prometheus.yml`: Prometheus configuration
- `monitoring/grafana/provisioning/`: Grafana configuration

### Customization Options

#### Agent Behavior

Customize the agent's behavior by modifying the instruction template in `backend/app/agents/chat_agent.py`:

```python
assistant_instructions = """
You are a helpful customer support agent. Your goal is to assist customers with their inquiries and issues.

Guidelines:
1. Be polite, professional, and empathetic
2. Use the memory tool to remember important information about the customer
3. Use the rag_search tool to find relevant information from the knowledge base
4. Process attachments if the customer uploads any documents
5. Escalate to a human agent if the issue requires human intervention
6. Always cite your sources when using information from the knowledge base
7. If you don't know the answer, be honest and try to help the customer find the right resource
"""
```

#### UI Customization

Customize the UI by modifying the React components in `frontend/src/components/` and the CSS modules.

#### Knowledge Base

Update the knowledge base by adding documents to the `docs/knowledge-base/` directory and running:

```bash
docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
```

### Security Settings

- Use strong, unique passwords for all services
- Enable SSL/TLS for all communications
- Implement proper authentication and authorization
- Regularly update dependencies
- Use security scanning tools

## Monitoring and Maintenance

### Health Checks

The application provides multiple health check endpoints:

- `GET /health/`: Basic health check
- `GET /health/detailed`: Detailed health check with component status
- `GET /health/readiness`: Readiness check for Kubernetes
- `GET /health/liveness`: Liveness check for Kubernetes

### Logging

The application uses structured JSON logging with the following log levels:

- `DEBUG`: Detailed information for debugging
- `INFO`: General information about application operation
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures
- `CRITICAL`: Critical errors that may cause the application to stop

Logs are written to stdout and can be viewed with:

```bash
docker-compose logs -f backend
```

### Metrics

The application exposes Prometheus metrics at `/metrics`. Key metrics include:

- `chat_messages_total`: Total number of chat messages
- `chat_message_duration_seconds`: Time spent processing messages
- `chat_escalations_total`: Total number of escalations
- `rag_queries_total`: Total number of RAG queries
- `attachment_processing_total`: Total number of attachments processed
- `active_sessions`: Number of active chat sessions
- `errors_total`: Total number of errors

### Troubleshooting

#### Common Issues

1. **High Response Times**:
   - Check Redis cache is working
   - Verify database connection pool settings
   - Monitor resource usage

2. **High Error Rates**:
   - Check application logs
   - Verify Agent Framework connectivity
   - Check Chroma vector database status

3. **Database Issues**:
   - Check connection pool settings
   - Monitor slow queries
   - Verify disk space

4. **Memory Issues**:
   - Monitor memory usage
   - Check for memory leaks
   - Adjust container memory limits

#### Debug Mode

Enable debug mode by setting `DEBUG=true` in the environment variables:

```bash
docker-compose exec backend env DEBUG=true python -m app.main
```

### Backup and Recovery

#### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres customer_support > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U postgres customer_support < backup.sql
```

#### Knowledge Base Backup

```bash
# Backup Chroma data
docker run --rm -v customer-support-agent_chroma_data:/data -v $(pwd):/backup alpine tar czf /backup/chroma-backup.tar.gz -C /data .

# Restore Chroma data
docker run --rm -v customer-support-agent_chroma_data:/data -v $(pwd):/backup alpine tar xzf /backup/chroma-backup.tar.gz -C /data
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style Guidelines

- Python: Follow PEP 8
- TypeScript/React: Follow ESLint rules
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation
3. Ensure your PR passes all CI checks
4. Request a review from the maintainers

### Testing Guidelines

- Write unit tests for new functionality
- Write integration tests for API endpoints
- Write end-to-end tests for user flows
- Ensure test coverage is at least 80%

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Microsoft Agent Framework for providing the AI agent orchestration
- Google for the EmbeddingGemma model
- Chroma for the vector database
- The open-source community for the tools and libraries used in this project

## References

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- [EmbeddingGemma Model](https://huggingface.co/google/embeddinggemma-300m)
- [Chroma Vector Database](https://www.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
