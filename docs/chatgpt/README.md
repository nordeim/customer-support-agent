# 🧠 Customer Support AI Agent  
*A friendly, smart, and knowledge-powered chatbot for customer support scenarios.*

[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/support-ai/ci.yml?branch=main)](https://github.com/your-org/support-ai/actions)  
[![Version](https://img.shields.io/github/v/tag/your-org/support-ai)](https://github.com/your-org/support-ai/releases)  
[![License](https://img.shields.io/github/license/your-org/support-ai)](LICENSE)  
[![Coverage](https://img.shields.io/codecov/c/github/your-org/support-ai)](https://codecov.io/gh/your-org/support-ai)  

## Table of Contents  
- [Introduction](#introduction)  
- [Technology Stack](#technology-stack)  
- [Architecture](#architecture)  
- [Quick Start](#quick-start)  
- [Deployment](#deployment)  
- [API Documentation](#api-documentation)  
- [Configuration](#configuration)  
- [Monitoring & Maintenance](#monitoring-maintenance)  
- [Contributing](#contributing)  
- [License & Acknowledgments](#license-acknowledgments)  

---

## Introduction  
### Project Overview and Purpose  
The Customer Support AI Agent is a production-ready chatbot solution designed to assist customers, answer questions from a support knowledge base, handle attachments, and seamlessly escalate to human agents when needed. It combines advanced AI-agent frameworks, retrieval-augmented generation (RAG), memory persistence, and a friendly front-end chatbot UI.

### Key Features & Capabilities  
- Conversational chat interface for customer support.  
- Persistent memory of threads and sessions via SQLite.  
- Knowledge-base powered responses using document embeddings and vector search (Chroma + EmbeddingGemma-300m).  
- Attachment ingestion (PDFs, docs, images) and conversion to searchable content.  
- Integration with the Microsoft Agent Framework (Python) for tool-based agent workflows, streaming responses, and human-in-the-loop escalation.  
- Observability: structured JSON logging, Prometheus metrics, health endpoints.  
- Dockerised and CI-gated for reliable deployment.

### Business Value & Use Cases  
- Automate first-level customer support, reducing human agent load.  
- Provide consistent, documented answers from internal knowledge bases.  
- Handle attachments from customers (screenshots, logs, PDFs) and extract insights.  
- Escalate to human agents when necessary, enhancing customer experience.  
- Deliver measurable SLAs: faster responses, lower cost, improved customer satisfaction.

### High-Level Architecture Summary  
The system consists of a React frontend chat UI, a FastAPI Python backend powered by the Microsoft Agent Framework, a lightweight SQLite memory store, and a Chroma vector store for document retrieval. The backend orchestrates conversation state, memory, tools, and knowledge retrieval to deliver informed responses.

---

## Technology Stack  
### Frontend  
- React (TypeScript) chat application  
- WebSocket/REST interface to backend  
- File-upload component for attachments  

### Backend  
- Python 3.11, FastAPI  
- Agent orchestration via Microsoft Agent Framework (Python) :contentReference[oaicite:0]{index=0}  
- Tooling layer for memory, RAG retrieval, attachment processing  

### Database & Storage  
- SQLite for session and memory persistence (zero-ops, file-based)  
- Chroma vector database for embeddings and retrieval of knowledge base content  

### AI/ML Components  
- Embedding model: `google/embeddinggemma-300m` (via Hugging Face)  
- RAG retrieval pipeline: embeddings → Chroma → agent input  
- Microsoft Agent Framework for chat & tool workflows :contentReference[oaicite:1]{index=1}  

### Monitoring & Observability  
- Prometheus metrics (`/metrics` endpoint)  
- Structured JSON logging with request-IDs  
- Health endpoint (`/healthz`)  
- CI pipeline: linting, type checking (mypy), unit/integration tests, coverage  

---

## Architecture  
### File Hierarchy  
```

/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Settings & environment variables
│   │   ├── logging_config.py      # Structured logging
│   │   ├── metrics.py             # Prometheus metrics setup
│   │   ├── db/
│   │   │   ├── sqlite.py          # SQLAlchemy engine
│   │   │   └── models.py          # SQLite ORM models
│   │   ├── tools/
│   │   │   ├── memory_tool.py     # Session/memory persistence
│   │   │   ├── rag_tool.py        # Retrieval tool
│   │   │   ├── attachment_tool.py # Attachment processing
│   │   │   └── escalation_tool.py # Escalation to human agent
│   │   ├── knowledge_base/
│   │   │   ├── preprocessor.py    # Document chunking & embedding prep
│   │   │   └── indexer.py         # Chroma indexing & query
│   │   └── agents.py              # Agent setup & chat endpoint
│   ├── migrations/                # DB migration scripts
│   ├── Dockerfile                 # Container build
│   └── docker-compose.yml         # Local orchestration
├── frontend/                      # React chat UI
└── README.md                      # This documentation

````

### Interaction Diagram  
```mermaid
sequenceDiagram
  participant U as User  
  participant FE as Frontend (React)  
  participant BE as Backend (FastAPI)  
  participant KB as VectorDB (Chroma)  
  U->>FE: Sends chat message  
  FE->>BE: HTTP POST /chat/message  
  BE->>BE: Persist user message → retrieve memory  
  BE->>KB: Query relevant docs via embeddings  
  KB-->>BE: Return top K docs  
  BE->>Agent: Construct prompt with memory + docs  
  Agent-->>BE: Generate response (stream or non-stream)  
  BE->>BE: Persist agent response  
  BE-->>FE: Return or stream response  
  FE-->>U: Display response  
````

### Application Logic Flow

```mermaid
flowchart TD
    A[Receive request /chat/message] --> B[Load session & memory]
    B --> C{Is stream flag set?}
    C -->|Yes| D[Retrieve docs via RAG]
    D --> E[Invoke agent.run_stream(...) for streaming output]
    E --> F[Persist response chunks]
    F --> G[Return SSE stream to frontend]
    C -->|No| H[Retrieve docs via RAG]
    H --> I[Invoke agent.run(...) for full response]
    I --> J[Persist response]
    J --> K[Return JSON response]
    K --> L{Response suggests escalation?}
    L -->|Yes| M[Trigger escalation tool → create ticket]
    L -->|No| N[End]
```

### Component Relationships

* **MemoryTool**: Reads/writes conversation and memory entries to SQLite.
* **RAGTool**: Coordinates embeddings and Chroma vector search.
* **AttachmentTool**: Parses uploads and creates searchable content.
* **EscalationTool**: Handles triggering hand-off to human.
* **Agent (via Microsoft Agent Framework)**: Coordinates chat, tools, streaming.
* **Frontend**: Chat UI interacts with backend API.

---

## Quick Start

### Prerequisites

* Docker & Docker Compose installed
* Node.js & npm (for frontend)
* Python 3.11+
* Git repository cloned

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-org/support-ai.git
   cd support-ai
   ```
2. Navigate to backend and install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Build and start services (backend + vector DB placeholder):

   ```bash
   docker-compose up --build
   ```

### Configuration

Create a `.env` file in `backend/` with required variables:

```
OPENAI_API_KEY=your-key
OPENAI_CHAT_MODEL_ID=gpt-4o-mini
SQLITE_URL=sqlite:///./data/agent_memory.db
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
CHROMA_COLLECTION_NAME=support_kb
ENVIRONMENT=development
```

### Running the Application

* Backend will be available at `http://localhost:8000`.
* Health check: `http://localhost:8000/healthz` → `{ "status": "ok" }`
* Metrics: `http://localhost:8000/metrics`

### Basic Usage Example

```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{ "session_id": "1234", "message": "How do I return a damaged product?" }'
```

Response:

```json
{
  "session_id": "1234",
  "response": "You can return a damaged product within 30 days… [reference source]"
}
```

---

## Deployment

### Development Deployment

* Use `docker-compose up` as above for local dev.
* Run tests:

  ```bash
  pytest --cov=backend/app
  ```
* Ensure linting & typing:

  ```bash
  black --check backend/app
  flake8 backend/app
  mypy backend/app
  ```

### Production Deployment

* Build and push Docker image, tag with version.
* Use orchestration platform (Kubernetes, ECS, etc) with volume mounts for SQLite & Chroma persistence.
* Ensure environment variables are injected via secure vault.
* Scale as needed: here are considerations…

  * **Scaling memory DB**: SQLite is file-based; for high concurrency consider PostgreSQL.
  * **Vector DB**: Chroma supports persistence but may require clustering; for large scale consider Weaviate or Pinecone.
  * **Stateless backend**: Keep containers stateless (persist only memory DB and vector store externally).
  * **Streaming mode**: If front-end uses SSE / WebSocket, ensure load-balancer supports sticky sessions or handle reconnects.

### Environment Variables (major ones)

| Name                       | Description                                         |
| -------------------------- | --------------------------------------------------- |
| `OPENAI_API_KEY`           | API key for OpenAI service                          |
| `OPENAI_CHAT_MODEL_ID`     | Model ID (e.g., `gpt-4o-mini`)                      |
| `SQLITE_URL`               | Connection string for SQLite memory store           |
| `CHROMA_PERSIST_DIRECTORY` | File‐path for Chroma vector persistence             |
| `CHROMA_COLLECTION_NAME`   | Name of the vector collection in Chroma             |
| `ENVIRONMENT`              | Deployment environment (`development`/`production`) |

---

## API Documentation

### Authentication

The API currently uses session IDs to track user threads. API keys or JWTs for user authentication can be added in future releases.

### Endpoints

| Method | Path            | Description                      | Request Body                                                 | Response Body                                |
| ------ | --------------- | -------------------------------- | ------------------------------------------------------------ | -------------------------------------------- |
| POST   | `/chat/message` | Send a user message to the agent | `{ "session_id": "...", "message": "...", "stream": false }` | `{ "session_id": "...", "response": "..." }` |
| GET    | `/healthz`      | Health check                     | —                                                            | `{ "status": "ok" }`                         |
| GET    | `/metrics`      | Prometheus metrics endpoint      | —                                                            | Plain text metrics                           |

### Streaming Example

```bash
curl -N -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{ "session_id": "1234", "message": "Tell me about return policy", "stream": true }'
```

The response will be a Server-Sent Events (SSE) stream with incremental `data:` chunks followed by `[DONE]`.

### Error Handling

* 400 Bad Request: malformed input.
* 500 Internal Server Error: agent or tool failure (check logs).
* Example response:

```json
{
  "detail": "Internal server error"
}
```

### Rate Limiting

Currently not enforced in this version. A future release may introduce rate-limiting middleware in the agent framework.

---

## Configuration

### Environment Variables

Refer to the table above in the *Deployment* section.

### Configuration Files

* `backend/app/config.py`: loads and validates settings.
* `docker-compose.yml`: orchestrates backend + vectordb placeholder.
* `migrations/run_migrations.sh`: idempotent SQLite schema.

### Customization Options

* Change embedding model (`EMBEDDING_MODEL_ID`) for higher fidelity.
* Tune chunk size (`KB_CHUNK_SIZE_SENTENCES`) for knowledge-base ingestion.
* Adjust retrieval top-K (`KB_TOP_K`) for balancing performance vs relevance.
* Switch memory DB to PostgreSQL by replacing SQLite dialect.

### Security Settings

* Ensure secrets (API keys) are not in version control.
* Validate attachments via `AttachmentTool` and sanitize stored data.
* Monitor tools usage (`agent_tool_invocations_total`) for anomalous activity.

---

## Monitoring & Maintenance

### Health Checks

* `/healthz`: basic status endpoint.
* Metrics pipeline: `/metrics` (Prometheus).

### Logging

* Structured JSON logging with `request_id` to correlate sessions.
* Log levels configurable via `LOG_LEVEL` environment variable.

### Metrics

* `agent_request_count_total` – total chat requests.
* `agent_request_latency_seconds` – latency of non-stream requests.
* `agent_stream_request_latency_seconds` – latency of streaming responses.
* `agent_tool_invocations_total` – number of tool calls (memory, RAG, attachments).

### Troubleshooting

* *Slow responses*: Investigate model latency or vector store performance.
* *“database locked” error*: SQLite concurrency limit — consider switching to PostgreSQL.
* *Zero results from RAG*: Check embeddings generation and Chroma persistence.
* *Agent keeps escalating unnecessarily*: Adjust prompt or tool logic in `EscalationTool`.

### Backup & Recovery

* Backup SQLite `.db` file periodically.
* Backup Chroma persistence directory (`CHROMA_PERSIST_DIRECTORY`).
* Rollback script: `deploy/rollback.sh` (see runbook)

---

## Contributing

### Development Setup

```bash
git clone https://github.com/your-org/support-ai.git
cd support-ai/backend
pip install -r requirements.txt
```

### Code Style Guidelines

* Follows `black`, `flake8`, `mypy` for formatting, linting, typing.
* Typing declarations mandatory for public APIs.
* Single responsibility per module, clear docstrings.

### Pull Request Process

1. Create a feature branch (`feature/your-feature`).
2. Write code, include unit + integration tests.
3. Ensure linting and tests pass locally.
4. Open a PR, link the issue, describe changes.
5. CI will run lint/tests.
6. After review and approval, merge into `main`.

### Testing Guidelines

* Unit tests: `tests/unit/` (fast, isolated).
* Integration tests: `tests/integration/` (covers real flow, slower).
* Use deterministic seeds where non-determinism exists (e.g., memory ordering).
* Coverage target: ≥ 80%.

---

## License & Acknowledgments

**License:** [MIT](LICENSE)
**Contributors:** Thanks to all developers and reviewers who contributed to this version.
**Third-Party Attributions:**

* Microsoft Agent Framework (Python) – Agent orchestration framework. ([Microsoft Learn][1])
* Embedding model: `google/embeddinggemma-300m` (Hugging Face)
* Vector store: Chroma (open source)
* Attachment processor: MarkItDown
* Frontend: React community libraries

**References:**

* Microsoft Agent Framework documentation – [Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/)
* GitHub repo – [microsoft/agent-framework](https://github.com/microsoft/agent-framework)

---

Thank you for exploring the Customer Support AI Agent. We look forward to your feedback and contributions!

[1]: https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/chat-client-agent?utm_source=chatgpt.com "Agent based on any IChatClient | Microsoft Learn"
