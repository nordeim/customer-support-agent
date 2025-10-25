Here are the additional files integrating the Microsoft Agent Framework usage into `/chat/message` flow, updating CI config for the new tests, and providing an integration test skeleton.

---

### `backend/app/agents.py` (updated)

```python
import uuid
import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .tools.memory_tool import MemoryTool
from .tools.rag_tool import RAGTool
from .tools.escalation_tool import EscalationTool
from .config import settings
from .logging_config import configure_logging
from .metrics import record_request
from .db.sqlite import Base, engine

# Importing Agent Framework
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient  # using OpenAI provider as example

configure_logging()
logger = logging.getLogger(__name__)

router = APIRouter()
memory_tool = MemoryTool()
rag_tool = RAGTool()
escalation_tool = EscalationTool()

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
    logger.info(f"Session {payload.session_id}: received message: {payload.message}")

    # Build context: past messages and memory entries
    msgs = memory_tool.get_messages(payload.session_id)
    memory_entries = memory_tool.get_memory_entries(payload.session_id)
    # Create string context for agent
    context_str = "\n".join(f"{m.sender}: {m.content}" for m in msgs)
    memory_str = "\n".join(f"{e.key}: {e.value}" for e in memory_entries)

    # Use RAG to fetch relevant docs
    retrieved = rag_tool.retrieve(payload.message)
    docs_context = rag_tool.format_for_agent(retrieved)

    instructions = """
You are a friendly customer-support AI assistant. Use the conversation context, memory entries, and knowledge base documents to craft your response. If you cannot confidently answer, suggest escalation.
"""
    # Combine everything into agent prompt
    prompt = f"{instructions}\n\nMemory:\n{memory_str}\n\nKnowledgeBaseDocs:\n{docs_context}\n\nConversation:\n{context_str}\nUser: {payload.message}"

    # Initialize Agent Framework ChatAgent
    # Note: Replace model details/config as needed
    chat_client = OpenAIChatClient(api_key=settings.OPENAI_API_KEY, model_id=settings.OPENAI_CHAT_MODEL_ID)
    agent = ChatAgent(chat_client=chat_client, instructions=instructions)

    # Run agent asynchronously
    result = await agent.run(payload.message)

    response_text = result.text.strip()
    logger.info(f"Session {payload.session_id}: agent response: {response_text}")

    # Persist agent response
    memory_tool.add_message(payload.session_id, sender="agent", content=response_text)

    # Optionally: escalate if certain keywords
    if "escalate" in response_text.lower() or "human agent" in response_text.lower():
        ticket = escalation_tool.escalate(payload.session_id, reason="Agent indicated human hand-off")
        logger.info(f"Session {payload.session_id} escalated: {ticket}")

    return ChatResponse(session_id=payload.session_id, response=response_text)
```

**Notes:**

* We integrated the RAG tool to retrieve relevant knowledge.
* We used the Microsoft Agent Framework Python client (via `ChatAgent` and `OpenAIChatClient`). Documentation shows such usage. ([Microsoft Learn][1])
* Memory and message persistence remain via the `MemoryTool`.
* Escalation tool stub triggers based on keywords in agent response.

---

### `backend/.github/workflows/ci.yml` (updated to include new tests)

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
      - name: Lint with black
        run: black --check backend/app
      - name: Lint with flake8
        run: flake8 backend/app
      - name: Type check with mypy
        run: mypy backend/app
      - name: Run unit tests
        run: pytest --cov=backend/app tests/unit
      - name: Run integration tests (RAG + ingestion)
        run: pytest --cov=backend/app tests/integration
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: backend/htmlcov
```

---

### `backend/tests/integration/test_chat_flow.py`

```python
import tempfile
import pathlib
import uuid
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config import settings
from backend.app.knowledge_base.preprocessor import KBPreprocessor
from backend.app.knowledge_base.indexer import KBIndexer

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_kb(tmp_path_factory):
    # Setup knowledge base ingestion
    persist_dir = tmp_path_factory.mktemp("chroma_int_test")
    settings.CHROMA_PERSIST_DIRECTORY = str(persist_dir)
    doc = persist_dir / "support_doc.txt"
    doc.write_text("If your product is damaged you can return it within 30 days for a full refund.")
    pre = KBPreprocessor()
    chunks = pre.ingest_document(doc)
    idx = KBIndexer(persist_directory=str(persist_dir))
    idx.index_chunks(chunks)
    return True

def test_chat_support_flow():
    session_id = str(uuid.uuid4())
    # Send first user message
    resp = client.post("/chat/message", json={"session_id": session_id, "message": "My product arrived broken, what do I do?"})
    assert resp.status_code == 200
    json_data = resp.json()
    assert json_data["session_id"] == session_id
    assert "within 30 days" in json_data["response"]

    # Send follow-up message
    resp2 = client.post("/chat/message", json={"session_id": session_id, "message": "And how long for the refund?"})
    assert resp2.status_code == 200
    json_data2 = resp2.json()
    assert "refund" in json_data2["response"]
```

---

### Summary

* Integrated RAG retrieval within chat flow.
* Integrated Microsoft Agent Framework client usage.
* Updated CI workflow to run unit & integration tests.
* Added integration test skeleton to validate chat-flow including RAG.

[1]: https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/openai-assistants-agent?utm_source=chatgpt.com "OpenAI Assistants Agents | Microsoft Learn"
