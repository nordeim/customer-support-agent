Here are the **remaining files** for polishing, documenting, refining error handling, adding streaming support and performance instrumentation.

---

### `backend/app/agents.py` (refined with streaming support, performance instrumentation & error handling)

```python
import uuid
import logging
import asyncio
import time
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .tools.memory_tool import MemoryTool
from .tools.rag_tool import RAGTool
from .tools.escalation_tool import EscalationTool
from .config import settings
from .logging_config import configure_logging
from .metrics import instrument_app, record_request, REQUEST_LATENCY, REQUEST_COUNT
from .db.sqlite import Base, engine

# Importing Agent Framework
from agent_framework import ChatAgent  # alias based on programming guide
from agent_framework.openai import OpenAIChatClient  # as example provider

configure_logging()
logger = logging.getLogger(__name__)

router = APIRouter()
memory_tool = MemoryTool()
rag_tool = RAGTool()
escalation_tool = EscalationTool()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    stream: bool = False  # new flag: whether the client wants streaming response

class ChatResponse(BaseModel):
    session_id: str
    response: str

@router.post("/chat/message", response_model=ChatResponse)
@record_request
async def chat_message(payload: ChatRequest, request: Request):
    start_ts = time.time()
    session_id = payload.session_id or str(uuid.uuid4())
    try:
        # Persist user message
        memory_tool.add_message(session_id, sender="user", content=payload.message)
        logger.info(f"Session {session_id}: received message: {payload.message}")

        # Build context
        msgs = memory_tool.get_messages(session_id)
        memory_entries = memory_tool.get_memory_entries(session_id)
        context_str = "\n".join(f"{m.sender}: {m.content}" for m in msgs)
        memory_str = "\n".join(f"{e.key}: {e.value}" for e in memory_entries)

        # Use RAG
        retrieved = rag_tool.retrieve(payload.message)
        docs_context = rag_tool.format_for_agent(retrieved)

        instructions = """
You are a friendly customer-support AI assistant. Use the conversation context, memory entries, and knowledge-base documents to craft your response. If you cannot confidently answer, suggest escalation to a human agent.
"""
        prompt = f"{instructions}\n\nMemory:\n{memory_str}\n\nKnowledgeBaseDocs:\n{docs_context}\n\nConversation:\n{context_str}\nUser: {payload.message}"

        # Setup Agent Framework client
        chat_client = OpenAIChatClient(api_key=settings.OPENAI_API_KEY, model_id=settings.OPENAI_CHAT_MODEL_ID, stream=payload.stream)
        agent = ChatAgent(chat_client=chat_client, instructions=instructions)

        if payload.stream:
            # Stream response back to client (via Server-Sent Events or WebSocket)
            async def event_generator():
                try:
                    async for chunk in agent.run_stream(prompt=prompt):
                        # chunk may include partial content
                        yield f"data: {chunk.text}\n\n"
                    elapsed = time.time() - start_ts
                    REQUEST_LATENCY.observe(elapsed)
                    yield f"data: [DONE]\n\n"
                except Exception as e:
                    logger.exception(f"Session {session_id}: streaming agent error: {e}")
                    yield f"data: [ERROR] {str(e)}\n\n"
            REQUEST_COUNT.inc()
            return StreamingResponse(event_generator(), media_type="text/event-stream")
        else:
            # Non-streaming fallback
            result = await agent.run(prompt=prompt)
            response_text = result.text.strip()
            logger.info(f"Session {session_id}: agent response: {response_text}")

            memory_tool.add_message(session_id, sender="agent", content=response_text)

            # Escalation logic
            if "escalate" in response_text.lower() or "human agent" in response_text.lower():
                ticket = escalation_tool.escalate(session_id, reason="Agent recommended escalation")
                logger.info(f"Session {session_id} escalated: {ticket}")

            elapsed = time.time() - start_ts
            REQUEST_LATENCY.observe(elapsed)
            REQUEST_COUNT.inc()
            return ChatResponse(session_id=session_id, response=response_text)

    except Exception as exc:
        logger.exception(f"Session {session_id}: unexpected error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")

```

---

### `backend/app/metrics.py` (update: add streaming latency histogram, tool invocation counters)

```python
from prometheus_client import Counter, Histogram, make_asgi_app
from fastapi import Request

REQUEST_COUNT = Counter(
    "agent_request_count_total", "Total number of chat requests received"
)
REQUEST_LATENCY = Histogram(
    "agent_request_latency_seconds", "Latency of agent request handling (non-stream mode)"
)
STREAM_REQUEST_LATENCY = Histogram(
    "agent_stream_request_latency_seconds", "Latency of streaming agent request handling"
)
TOOL_INVOCATIONS = Counter(
    "agent_tool_invocations_total", "Total number of tool invocations by the agent"
)

def instrument_app(app):
    prometheus_app = make_asgi_app()
    app.mount("/metrics", prometheus_app)

def record_request(func):
    async def wrapper(request: Request, *args, **kwargs):
        return await func(request, *args, **kwargs)
    return wrapper
```

---

### `backend/app/logging_config.py` (enhanced to include request IDs)

```python
import logging
import sys
import json
import uuid

class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        record_id = getattr(record, "request_id", None) or str(uuid.uuid4())
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "request_id": record_id,
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
    # Add request_id filter
    class RequestIdFilter(logging.Filter):
        def filter(self, rec):
            if not hasattr(rec, "request_id"):
                rec.request_id = str(uuid.uuid4())
            return True
    root.addFilter(RequestIdFilter())
```

---

### `backend/README.md` (update section on streaming & performance)

```markdown
...
## Streaming Responses Support  
The `/chat/message` endpoint supports streaming output if the client sets `"stream": true` in the request body. This will return a **Server-Sent Events (SSE)** response (`text/event-stream`) with incremental `data:` chunks. The final chunk is `[DONE]`.  
Clients should handle partial chunks and may display a typing indicator or progressive UI.

## Observability & Performance  
- A `/metrics` endpoint (Prometheus) is exposed, e.g., `agent_request_latency_seconds`, `agent_stream_request_latency_seconds`, `agent_tool_invocations_total`.  
- Logging uses structured JSON format with `request_id` for tracing across logs.  
- SLIs / SLOs (suggested):  
  - 95th percentile latency < 2 s for non-stream requests  
  - 90th percentile initial stream response < 1 s  
  - Tool error rate < 1%  
```

---

### `backend/tests/integration/test_streaming_chat_flow.py`

```python
import tempfile
import pathlib
import uuid
import time
import asyncio
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config import settings
from backend.app.knowledge_base.preprocessor import KBPreprocessor
from backend.app.knowledge_base.indexer import KBIndexer

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_kb(tmp_path_factory):
    persist_dir = tmp_path_factory.mktemp("chroma_stream_test")
    settings.CHROMA_PERSIST_DIRECTORY = str(persist_dir)
    doc = persist_dir / "support_stream_doc.txt"
    doc.write_text("Our policy: you can return faulty items within 45 days for replacement or refund.")
    pre = KBPreprocessor()
    chunks = pre.ingest_document(doc)
    idx = KBIndexer(persist_directory=str(persist_dir))
    idx.index_chunks(chunks)
    return True

def test_streaming_chat_support_flow():
    session_id = str(uuid.uuid4())
    # Request with streaming true
    resp = client.post("/chat/message", json={"session_id": session_id, "message": "What is the return policy?", "stream": True}, stream=True)
    assert resp.status_code == 200
    collected = ""
    for line in resp.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            assert decoded.startswith("data:")
            # strip prefix
            content = decoded[5:].strip()
            if content == "[DONE]":
                break
            collected += content
    assert "45 days" in collected
```


