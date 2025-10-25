Proceed to create the initial set of files for **Phase 2 Sprint A**. Below are the contents of key files. You can copy each into your repository workspace.

---

### `README.md`

````markdown
# Customer Support AI Agent

This repository implements a production-ready **Customer Support AI Agent** composed of:

- Frontend: React chat UI (to be implemented)  
- Backend: Python + FastAPI + Agent Framework (Assistants client)  
- Memory: SQLite via SQLAlchemy  
- Retrieval-Augmented Generation (RAG): Embeddings (embeddinggemma‑300m) + Chroma vector store  
- Attachment processing: markitdown package  

## Architecture

(See architecture diagram in Phase 1 planning document.)  
- User interacts via React frontend → sends messages to backend `/chat/message` endpoint.  
- Backend loads session context, memory, executes agent thread with tools (memory, RAG, attachments, escalation).  
- Agent uses RAG to search docs, uses tools to persist memory and respond.  
- Metrics, logging, health endpoints included for observability.  
- Dockerised for local/dev deployment; CI gating for quality.  

## Tech Stack

- Python 3.12, FastAPI, SQLAlchemy, Alembic (for migrations)  
- React (TypeScript) for frontend  
- Agent Framework (Python)  
- embeddinggemma-300m, Chroma vector store  
- markitdown for attachments  
- Prometheus client for metrics  
- GitHub Actions + flake8/black/mypy for CI  

## Getting Started (Sprint A)

### Prerequisites
- Python 3.11+  
- Docker & Docker Compose  
- Node.js & npm (for frontend later)  

### Running Backend Locally
```bash
cd backend
docker-compose up --build
````

This will start the backend service and placeholder vector-db service.

### Running Tests

```bash
cd backend
pytest --cov
```

### Code Style & Linting

```bash
flake8
black --check .
mypy .
```

## Next Steps

* Sprint B: implement RAG tool and knowledge base ingestion
* Sprint C: implement attachment processing + React UI
* Observability & Security features in Phase 3
* QA & Validation in Phase 4

````

---

### `backend/app/config.py`
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    # Database
    SQLITE_URL: str = "sqlite:///./data/agent_memory.db"
    # Logging
    LOG_LEVEL: str = "INFO"
    # Agent Framework
    AGENT_FRAMEWORK_API_KEY: str = ""  # placeholder; set via env
    # Vector DB / RAG
    CHROMA_URL: str = "http://localhost:8001"  # placeholder
    # Other
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
````

---

### `backend/app/logging_config.py`

```python
import logging
import sys
import json

class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonLogFormatter()
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
```

---

### `backend/app/metrics.py`

```python
from prometheus_client import Counter, Histogram, make_asgi_app
from fastapi import Request

REQUEST_COUNT = Counter(
    "agent_request_count", "Total number of chat requests received"
)
REQUEST_LATENCY = Histogram(
    "agent_request_latency_seconds", "Latency of agent request handling"
)
TOOL_INVOCATIONS = Counter(
    "agent_tool_invocations_total", "Total number of tool invocations by the agent"
)

def instrument_app(app):
    # Mount Prometheus ASGI middleware endpoint
    prometheus_app = make_asgi_app()
    app.mount("/metrics", prometheus_app)

def record_request(func):
    async def wrapper(request: Request, *args, **kwargs):
        REQUEST_COUNT.inc()
        with REQUEST_LATENCY.time():
            result = await func(request, *args, **kwargs)
        return result
    return wrapper
```

---

### `backend/app/db/sqlite.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import settings

engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

### `backend/app/db/models.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from .sqlite import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    messages = relationship("Message", back_populates="session")
    memory_entries = relationship("MemoryEntry", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    sender = Column(String)
    content = Column(Text)

    session = relationship("Session", back_populates="messages")

class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    key = Column(String)
    value = Column(Text)

    session = relationship("Session", back_populates="memory_entries")
```

---

### `backend/app/tools/memory_tool.py`

```python
from sqlalchemy.orm import Session as DbSession
from ..db.sqlite import SessionLocal
from ..db.models import Session as SessionModel, Message, MemoryEntry
import uuid
import datetime

class MemoryTool:
    def __init__(self):
        self.db = SessionLocal()

    def get_or_create_session(self, session_id: str):
        db: DbSession = self.db
        session = db.query(SessionModel).filter_by(session_id=session_id).first()
        if not session:
            session = SessionModel(session_id=session_id, created_at=datetime.datetime.utcnow())
            db.add(session)
            db.commit()
            db.refresh(session)
        return session

    def add_message(self, session_id: str, sender: str, content: str):
        session = self.get_or_create_session(session_id)
        msg = Message(session_id=session.id, sender=sender, content=content, timestamp=datetime.datetime.utcnow())
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_messages(self, session_id: str):
        session = self.get_or_create_session(session_id)
        msgs = self.db.query(Message).filter_by(session_id=session.id).order_by(Message.timestamp).all()
        return msgs

    def add_memory_entry(self, session_id: str, key: str, value: str):
        session = self.get_or_create_session(session_id)
        entry = MemoryEntry(session_id=session.id, key=key, value=value, timestamp=datetime.datetime.utcnow())
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_memory_entries(self, session_id: str):
        session = self.get_or_create_session(session_id)
        entries = self.db.query(MemoryEntry).filter_by(session_id=session.id).all()
        return entries
```

---

### `backend/app/agents.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
import logging

from .tools.memory_tool import MemoryTool
from .config import settings
from .logging_config import configure_logging
from .metrics import instrument_app, record_request, REQUEST_LATENCY, REQUEST_COUNT

# Placeholder for Agent Framework imports
# from agent_framework import AssistantsClient, ...

configure_logging()
logger = logging.getLogger(__name__)

router = APIRouter()

memory_tool = MemoryTool()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@router.post("/chat/message", response_model=ChatResponse)
@record_request
async def chat_message(payload: ChatRequest):
    # Persist user message
    memory_tool.add_message(payload.session_id, sender="user", content=payload.message)
    logger.info(f"Received message in session {payload.session_id}")

    # Stub: invoke agent, pass past messages and memory
    # todo: integrate Agent Framework Assistants client
    response_text = "Hello! This is a stub response. The real agent will be implemented soon."

    # Persist agent message
    memory_tool.add_message(payload.session_id, sender="agent", content=response_text)
    return ChatResponse(session_id=payload.session_id, response=response_text)
```

---

### `backend/app/main.py`

```python
import uvicorn
from fastapi import FastAPI
from .config import settings
from .logging_config import configure_logging
from .metrics import instrument_app
from .db.sqlite import Base, engine
from .agents import router as chat_router

configure_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Support AI Agent")

# Include routers
app.include_router(chat_router)

# Instrument metrics
instrument_app(app)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
```

---

### `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### `docker-compose.yml`

```yaml
version: "3.8"

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
    environment:
      - ENVIRONMENT=development
      - SQLITE_URL=sqlite:///./data/agent_memory.db
    depends_on:
      - vectordb

  vectordb:
    image: alpine  # placeholder until Chroma setup
    command: ["sleep", "3600"]
    ports:
      - "8001:8001"
```

---

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r backend/requirements.txt
      - name: Lint with flake8 & black
        run: |
          black --check backend/app
          flake8 backend/app
      - name: Type check with mypy
        run: |
          mypy backend/app
      - name: Run tests
        run: |
          pytest --cov=backend/app
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: backend/htmlcov
```

---

### `backend/requirements.txt`

```
fastapi
uvicorn[standard]
pydantic
sqlalchemy
prometheus_client
pytest
pytest-cov
flake8
black
mypy
agent-framework  # placeholder; actual import as per Microsoft Agent Framework
markitdown
```

---

### `backend/tests/unit/test_memory_tool.py`

```python
import tempfile
import os
import pytest
from backend.app.tools.memory_tool import MemoryTool
from backend.app.db.sqlite import Base, engine

@pytest.fixture(scope="module")
def temp_db(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test_memory.db"
    db_url = f"sqlite:///{db_file}"
    engine_test = engine = engine = engine = None
    # Monkey-patch engine for test
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine_test = create_engine(db_url, connect_args={"check_same_thread": False})
    SessionLocal_test = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
    # Create tables
    Base.metadata.create_all(bind=engine_test)
    # Patch the session maker in MemoryTool
    import backend.app.tools.memory_tool as mt
    mt.SessionLocal = SessionLocal_test
    yield SessionLocal_test
    # cleanup happen automatically

def test_add_and_get_memory_entries(temp_db):
    memory = MemoryTool()
    sid = "session-123"
    memory.add_memory_entry(sid, key="favorite_color", value="blue")
    entries = memory.get_memory_entries(sid)
    assert len(entries) == 1
    assert entries[0].key == "favorite_color"
    assert entries[0].value == "blue"

def test_add_and_get_messages(temp_db):
    memory = MemoryTool()
    sid = "session-456"
    memory.add_message(sid, sender="user", content="Hello agent")
    memory.add_message(sid, sender="agent", content="Hello user")
    msgs = memory.get_messages(sid)
    assert len(msgs) == 2
    assert msgs[0].sender == "user"
    assert msgs[1].sender == "agent"
```

