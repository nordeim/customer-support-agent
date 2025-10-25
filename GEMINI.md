# GEMINI Analysis: Customer Support AI Agent

This document provides a comprehensive summary and operational guide for the Customer Support AI Agent project, intended for use as an instructional context for AI-driven development.

## 1. Project Overview

This is a production-grade, containerized software project that implements an intelligent customer support agent.

-   **Purpose**: To automate and enhance customer support by using a conversational AI to answer queries. The agent leverages a Retrieval-Augmented Generation (RAG) pipeline to provide answers based on a private knowledge base.
-   **Architecture**: The system employs a microservices architecture consisting of a React/TypeScript frontend, a Python/FastAPI backend, and a suite of data stores (PostgreSQL/SQLite, ChromaDB, Redis). The entire environment is orchestrated via Docker Compose.
-   **Core Technologies**:
    -   **Frontend**: React, TypeScript
    -   **Backend**: Python, FastAPI
    -   **AI/ML**: Microsoft Agent Framework, `EmbeddingGemma-300m`, ChromaDB
    -   **Databases**: PostgreSQL (production), SQLite (development), Redis (caching)
    -   **Deployment**: Docker, Docker Compose, GitHub Actions

## 2. Building and Running

The following steps are required to set up and run the application in a local development environment.

### Step 1: Clone the Repository
```bash
git clone https://github.com/nordeim/customer-support-agent.git
cd customer-support-agent
```

### Step 2: Configure Environment Variables
Create a `.env` file from the provided example and modify it if necessary.
```bash
cp .env.example .env
```

### Step 3: Start the Application Services
This command builds the containers and starts all services (backend, frontend, databases, etc.) in detached mode.
```bash
docker-compose up -d
```

### Step 4: Initialize the Database
This command runs the database initialization script inside the running backend container.
```bash
docker-compose exec backend python scripts/init_db.py
```

### Step 5: Populate the Knowledge Base
To enable the RAG functionality, populate the Chroma vector database with documents.
```bash
docker-compose exec backend python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
```

### Accessing the Services
-   **Frontend UI**: `http://localhost:3000`
-   **Backend API**: `http://localhost:8000`
-   **API Documentation (Swagger)**: `http://localhost:8000/docs`

## 3. Development Conventions

-   **Code Style**:
    -   **Python**: Adheres to PEP 8 standards.
    -   **TypeScript/React**: Follows the ESLint rules configured in the project.
-   **Testing**:
    -   The project includes unit, integration, and end-to-end tests located in the `backend/tests/` directory.
    -   New functionality should be accompanied by corresponding tests, with a target of at least 80% test coverage.
-   **Contribution Process**:
    -   Changes should be made in a feature branch.
    -   Pull requests should be submitted to the main branch.
    -   The `README.md` and any other relevant documentation must be updated.
    -   All CI checks (run via GitHub Actions) must pass before a PR can be merged.
-   **Key Files for Modification**:
    -   **Agent Behavior**: `backend/app/agents/chat_agent.py`
    -   **API Endpoints**: `backend/app/api/routes/`
    -   **Agent Tools**: `backend/app/tools/`
    -   **Frontend Logic**: `frontend/src/hooks/` and `frontend/src/components/`
