Let us create the **remaining files** needed for Sprint B (RAG + Ingestion) according to the plan:

---

### `backend/app/knowledge_base/README.md`

````markdown
# Knowledge Base Ingestion (`knowledge_base` module)

This module provides tools to ingest, preprocess, and index a support knowledge-base for retrieval-augmented generation (RAG) in the Customer Support AI Agent.

## Components

- `preprocessor.py`: Load documents (text, PDF, etc.), chunk into manageable pieces, and prepare for embedding.  
- `indexer.py`: Interface with ChromaDB vector store. Embeds chunks using the embedding model `SentenceTransformer` (model ID `google/embeddinggemma-300m`) and persists them for later retrieval.

## Usage

### Step 1 – Ingest documents
```bash
python -m backend.app.knowledge_base.preprocessor \
    --input_dir ./docs/support_kb \
    --output_metadata ./data/kb_metadata.json
````

(This is a stub; you may invoke `KBPreprocessor.ingest_directory` from your own script.)

### Step 2 – Index into Chroma

```bash
python -m backend.app.knowledge_base.indexer \
    --persist_dir ./data/chroma_db \
    --collection_name support_kb
```

### Step 3 – Query

In your backend code (via `RAGTool`):

```python
from backend.app.tools.rag_tool import RAGTool
rag = RAGTool()
results = rag.retrieve("How can I return a damaged product?")
print(rag.format_for_agent(results))
```

## Configuration

The following settings (in `config.py`) govern behaviour:

* `EMBEDDING_MODEL_ID`: default `"google/embeddinggemma-300m"`
* `CHROMA_PERSIST_DIRECTORY`: default `"./data/chroma_db"`
* `CHROMA_COLLECTION_NAME`: default `"support_kb"`
* `KB_CHUNK_SIZE_SENTENCES`: default `5`
* `KB_TOP_K`: default `5`

## Implementation Notes

* Document chunking uses simple sentence‐based heuristics; you may refine later (e.g., by token count).
* Embedding is done at ingestion; query embeddings happen at retrieval.
* ChromaClient is instantiated once on tool init; persistent directory is used for durability.
* Example integration tests exist in `tests/integration/test_rag_tool.py`.

````

---

### `backend/app/tools/attachment_tool.py`
```python
import logging
import pathlib
from typing import Tuple

from markitdown import MarkItDown

logger = logging.getLogger(__name__)

class AttachmentTool:
    """
    Tool to process user-uploaded attachments (e.g., PDF, DOCX, images).
    Converts attachments into plain text/Markdown for indexing or memory decisions.
    """

    def __init__(self):
        self.converter = MarkItDown()

    def convert_file(self, filepath: pathlib.Path) -> Tuple[str, str]:
        """
        Converts the file at `filepath` into Markdown/plain text.

        Returns:
            tuple of (converted_text: str, metadata: str)
        """
        logger.info(f"Converting attachment: {filepath}")
        try:
            result = self.converter.convert(str(filepath))
            text = result.text_content
            metadata = result.meta or ""
            return text, metadata
        except Exception as e:
            logger.exception(f"Failed to convert attachment {filepath}: {e}")
            raise

    def process_for_ingestion(self, filepath: pathlib.Path, doc_id: str):
        """
        Converts the file and returns chunks ready for KB ingestion.

        Returns:
            list of dicts with keys: doc_id, chunk_id, text, metadata
        """
        text, metadata = self.convert_file(filepath)
        # Simple split on paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        for idx, p in enumerate(paragraphs):
            chunks.append({
                "doc_id": doc_id,
                "chunk_id": idx,
                "text": p,
                "metadata": {
                    "source_path": str(filepath),
                    "doc_id": doc_id,
                    "chunk_id": idx,
                    "metadata": metadata
                }
            })
        logger.info(f"Processed {len(chunks)} chunks from attachment {filepath}")
        return chunks
````

---

### `backend/app/tools/escalation_tool.py`

```python
import logging

logger = logging.getLogger(__name__)

class EscalationTool:
    """
    Stub tool to escalate a conversation to a human agent.
    """

    def __init__(self):
        pass

    def escalate(self, session_id: str, reason: str) -> dict:
        """
        Trigger escalation and return ticket info.
        """
        logger.info(f"Escalating session {session_id} for reason: {reason}")
        # In a real system, integrate with ticketing system (Zendesk/ServiceNow/etc)
        ticket = {
            "ticket_id": f"ESCAL-{session_id}-{int(logger.makeRecord('',0,'',0, '', (), None)[3])}",
            "session_id": session_id,
            "reason": reason,
            "status": "open"
        }
        return ticket
```

---

### `backend/app/tools/__init__.py`

```python
# This file allows tool modules to be imported under tools package

from .memory_tool import MemoryTool
from .rag_tool import RAGTool
from .attachment_tool import AttachmentTool
from .escalation_tool import EscalationTool
```

---

### `backend/tests/unit/test_attachment_tool.py`

```python
import tempfile
import pathlib
import pytest
from backend.app.tools.attachment_tool import AttachmentTool

@pytest.fixture
def sample_txt_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Paragraph one.\n\nParagraph two.\n\nParagraph three.")
    return file

def test_convert_file_txt(sample_txt_file):
    at = AttachmentTool()
    text, metadata = at.convert_file(sample_txt_file)
    assert "Paragraph one" in text
    assert metadata is not None

def test_process_for_ingestion(sample_txt_file):
    at = AttachmentTool()
    chunks = at.process_for_ingestion(sample_txt_file, doc_id="DOCID123")
    assert isinstance(chunks, list)
    assert len(chunks) == 3
    assert chunks[0]["chunk_id"] == 0
    assert chunks[1]["chunk_id"] == 1
```

---

### `backend/tests/unit/test_rag_tool.py`

```python
import tempfile
import pathlib
import shutil
from backend.app.knowledge_base.preprocessor import KBPreprocessor
from backend.app.knowledge_base.indexer import KBIndexer
from backend.app.tools.rag_tool import RAGTool
from backend.app.config import settings

def test_rag_retrieve_simple(tmp_path):
    # Setup persist directory
    persist_dir = tmp_path / "chroma_test"
    settings.CHROMA_PERSIST_DIRECTORY = str(persist_dir)
    # Create sample doc
    doc = tmp_path / "sample.txt"
    doc.write_text("This document describes how to reset your password. To reset, go to Settings > Security > Reset Password within 5 minutes.")
    # Ingest and index
    pre = KBPreprocessor()
    chunks = pre.ingest_document(doc)
    idx = KBIndexer(persist_directory=str(persist_dir))
    idx.index_chunks(chunks)
    # Now use RAGTool
    rag = RAGTool()
    results = rag.retrieve("How do I reset my password?")
    assert results and any("reset your password" in r["text"] for r in results)
```

---

With these files in place, we cover:

* Ingestion/Preprocessing module
* Indexing & retrieval module
* Attachment processing tool
* Escalation stub tool
* Tool package init
* Unit tests for new modules

