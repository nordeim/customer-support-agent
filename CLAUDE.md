# AI Agent Onboarding: Customer Support AI Agent (`CLAUDE.md`)

## 1. Project Overview

This document provides a comprehensive technical briefing for the **Customer Support AI Agent**. The project is a production-grade, containerized application designed to provide intelligent, automated customer support.

- **Core Functionality**: It functions as a chatbot that leverages a Retrieval-Augmented Generation (RAG) pipeline to answer user queries based on a private knowledge base.
- **Primary Technologies**: The system is built on a Python/FastAPI backend and a React/TypeScript frontend. It utilizes the Microsoft Agent Framework for orchestrating AI logic.
- **Operational Environment**: The entire stack is designed to be run via Docker Compose, ensuring a consistent environment for development and production.

## 2. Core Objective & Business Value

The system is designed to automate customer support interactions to achieve:
- **Efficiency**: Reduce response times and operational costs.
- **Availability**: Provide 24/7 support.
- **Consistency**: Deliver standardized, high-quality answers.
- **Scalability**: Handle high volumes of customer queries.

## 3. System Architecture

The application follows a microservices architecture.

### 3.1. High-Level Components

1.  **Frontend**: A React-based single-page application that provides the user-facing chat interface.
2.  **Backend**: A FastAPI server that exposes a RESTful API, handles business logic, and orchestrates the AI agent.
3.  **AI Agent Framework**: The core of the AI logic, responsible for tool execution (RAG, memory), context management, and reasoning.
4.  **Databases & Caching**:
    *   **PostgreSQL**: The primary relational database for production data (sessions, conversations).
    *   **SQLite**: Used for development and for the agent's persistent memory system.
    *   **Chroma**: A vector database for storing text embeddings and performing similarity searches for the RAG pipeline.
    *   **Redis**: In-memory cache for session data, query optimization, and rate limiting.
5.  **Monitoring**:
    *   **Prometheus**: Scrapes and stores time-series metrics from the backend.
    *   **Grafana**: Provides dashboards for visualizing metrics.
6.  **Web Server/Proxy**:
    *   **Nginx**: Acts as a reverse proxy, handles SSL termination, and serves static frontend files in production.

### 3.2. Technology Stack

- **Frontend**: React 18.2.0, TypeScript 5.0, Axios
- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Alembic
- **AI/ML**: Microsoft Agent Framework, `EmbeddingGemma-300m` (for text embeddings), ChromaDB
- **Databases**: PostgreSQL, SQLite, Redis
- **DevOps & Deployment**: Docker, Docker Compose, GitHub Actions

### 3.3. Data and Logic Flow

The primary application flow for a user interaction is as follows:
1.  **Session Initiation**: The user accesses the frontend, which requests a new session from the backend. The backend creates and stores this session in the database.
2.  **Message Submission**: The user sends a message (with optional file attachments).
3.  **Backend Processing**: The backend receives the message and retrieves the conversation history.
4.  **Agent Execution**: The message and context are passed to the **Microsoft Agent Framework**.
5.  **RAG Pipeline**:
    *   The agent uses the `rag_tool` to generate an embedding of the user's query.
    *   It searches the **Chroma** vector database for relevant documents.
    *   The retrieved documents are used as context for generating a response.
6.  **Response Generation**: The agent synthesizes an answer. If the query cannot be answered, it may trigger an escalation to a human agent.
7.  **State Persistence**: The new conversation turn (user message and agent response) is stored in the database.
8.  **Response Delivery**: The final response, including source citations from the RAG pipeline, is sent back to the frontend and displayed to the user.

### 3.4. Key Directory and File Analysis

-   `backend/app/main.py`: The entry point for the FastAPI application.
-   `backend/app/agents/chat_agent.py`: **Contains the core agent logic**. The agent's instructions, personality, and tool integration are defined here. This is a primary file for modifying agent behavior.
-   `backend/app/tools/`: This directory contains the agent's capabilities (tools).
    -   `rag_tool.py`: Implements the RAG search functionality.
    -   `memory_tool.py`: Manages conversation history.
    -   `attachment_tool.py`: Handles file processing.
    -   `escalation_tool.py`: Manages escalation logic.
-   `backend/app/api/routes/chat.py`: Defines the FastAPI routes for chat interaction (`/chat/sessions`, etc.).
-   `backend/scripts/populate_kb.py`: Script used to load and process documents into the Chroma vector database.
-   `frontend/src/hooks/useChat.ts`: The primary React hook for managing client-side chat state and communication with the backend.
-   `frontend/src/services/api.ts`: The `fetch`-based client for making HTTP requests to the backend. Note: The `README.md` also mentions `axios`, but the primary implementation in `api.ts` uses the native `fetch` API.
-   `docker-compose.yml`: Defines and configures all the services for the **development environment**.
-   `docker-compose.prod.yml`: Defines the configuration for the **production environment**.
-   `.env.example`: A template for the required environment variables. A `.env` file must be created from this.

**Note on File Discrepancies**: The original `README.md` mentions a file `backend/app/agents/agent_factory.py`, which was not found during codebase review. The primary agent creation logic resides directly in `chat_agent.py`.

## 4. Operational Guide for AI Agent

### 4.1. Prerequisites

- Docker and Docker Compose
- Git

### 4.2. Environment Setup and Execution

1.  **Clone Repository**:
    ```bash
    git clone https://github.com/nordeim/customer-support-agent.git
    cd customer-support-agent
    ```
2.  **Configure Environment**:
    ```bash
    cp .env.example .env
    # IMPORTANT: Review and edit .env with necessary configurations.
    ```
3.  **Start All Services**:
    ```bash
    docker-compose up -d
    ```
4.  **Database Initialization**:
    ```bash
    docker-compose exec backend python scripts/init_db.py
    ```
5.  **Populate Knowledge Base** (Required for RAG functionality):
    ```bash
    docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
    ```

### 4.3. Service Endpoints (Default Local)

-   **Frontend UI**: `http://localhost:3000`
-   **Backend API**: `http://localhost:8000`
-   **API Docs (Swagger UI)**: `http://localhost:8000/docs`
-   **Grafana**: `http://localhost:3001`
-   **Prometheus**: `http://localhost:9090`

### 4.4. Interacting with the API

-   **Authentication Clarification**: The `README.md` states the API is secured with JWTs. However, codebase review of `backend/app/api/routes/chat.py` shows that the primary chat endpoints (`/chat/sessions` and `/chat/sessions/{session_id}/messages`) **do not** have authentication middleware applied. They are effectively public. Authentication may be enforced by a gateway in production, but is not active at the application level for these routes.
-   **Primary Chat Endpoints**:
    -   `POST /chat/sessions`: To create a new chat session.
    -   `POST /chat/sessions/{session_id}/messages`: To send a message to a session.

### 4.5. Monitoring and Health

-   **Health Checks**: `GET /health/`, `GET /health/detailed`
-   **Metrics**: Prometheus metrics are exposed at `GET /metrics`.

## 5. Development and Customization

### 5.1. Modifying Agent Behavior

-   To change the agent's core instructions, personality, or logic, edit `backend/app/agents/chat_agent.py`.
-   To add new capabilities, create a new tool in the `backend/app/tools/` directory and integrate it into the agent.

### 5.2. Updating the Knowledge Base

1.  Add, remove, or modify documents in a local directory (e.g., `docs/knowledge-base/`).
2.  Re-run the population script:
    ```bash
    docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
    ```

### 5.3. Code Style

-   **Python**: PEP 8
-   **TypeScript/React**: ESLint rules (as configured in the project).

### 5.4. Testing

The project includes unit, integration, and e2e tests in the `backend/tests/` directory. Any new functionality should be accompanied by corresponding tests.

## 6. Summary & Key Takeaways for AI Agent

-   **Fully Containerized**: Your primary interface for running and managing the application is `docker-compose`.
-   **Agent Logic is Centralized**: The most critical file for understanding and modifying the AI's behavior is `backend/app/agents/chat_agent.py`.
-   **RAG is a Core Feature**: The agent's ability to answer questions is dependent on the knowledge base. Ensure it is populated before testing query responses.
-   **API-Driven**: All interactions with the backend are through the FastAPI RESTful API. Refer to the Swagger UI at `http://localhost:8000/docs` for a live schema.
-   **Configuration via `.env`**: All sensitive or environment-specific settings are managed in the `.env` file.

## 7. Codebase Findings and Recommendations

This section summarizes findings from a direct codebase review and provides recommendations for improvement.

### 7.1. Discrepancies Noted

1.  **Documentation vs. Implementation**:
    *   **`agent_factory.py`**: This file is listed in the `README.md`'s file hierarchy but does not exist in the codebase. The agent is instantiated directly within `chat_agent.py`.
    *   **API Authentication**: The documentation claims JWT authentication is used, but the core chat endpoints are not protected by any authentication middleware at the application layer.
    *   **Axios vs. Fetch**: The `README.md` lists Axios as a technology, but the `api.ts` service uses the native `fetch` API.
2.  **Unused WebSocket Configuration**:
    *   The frontend's Docker configuration sets a `REACT_APP_WS_URL` environment variable, and the `README.md` mentions WebSocket support. However, the primary chat logic in `useChat.ts` is implemented via standard HTTP requests. The WebSocket logic likely exists elsewhere (`useWebSocket.ts`) but is not integrated into the main chat flow reviewed.

### 7.2. Recommendations for Improvement

1.  **Update Documentation**:
    *   **Recommendation**: Align the `README.md` with the codebase. Remove the reference to `agent_factory.py` and clarify the use of `fetch` instead of `axios` in the primary API service.
    *   **Reasoning**: Accurate documentation is critical for developer onboarding and reduces confusion.
2.  **Clarify or Implement API Security**:
    *   **Recommendation**: If the chat endpoints are intended to be public, this should be explicitly stated in the documentation. If they are meant to be secure, implement the necessary FastAPI dependencies (e.g., `Depends(get_current_user)`) on the routes in `chat.py`.
    *   **Reasoning**: Security posture should be explicit. Leaving sensitive endpoints unprotected, even in development, can lead to security vulnerabilities in production if the architecture is misunderstood.
3.  **Integrate or Remove WebSocket Code**:
    *   **Recommendation**: Decide on the primary communication method. If WebSockets are the intended future, integrate `useWebSocket.ts` into the main `ChatWindow` component. If HTTP polling/long-polling is sufficient, remove the unused WebSocket code and configuration to simplify the codebase.
    *   **Reasoning**: Unused code and configuration add complexity and can mislead developers about the system's intended functionality.
