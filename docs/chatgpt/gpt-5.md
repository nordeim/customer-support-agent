Understood. I’ll proceed to create the necessary files for **Sprint B (RAG + Knowledge Base Ingestion)** as per our plan. Below are the contents for key modules ready for your review and commit.

---

### `backend/app/knowledge_base/preprocessor.py`

```python
import os
import pathlib
import hashlib
import logging
from typing import List, Dict

import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

from ..config import settings

logger = logging.getLogger(__name__)

class DocumentChunk:
    def __init__(self, doc_id: str, chunk_id: int, text: str, metadata: Dict):
        self.doc_id = doc_id
        self.chunk_id = chunk_id
        self.text = text
        self.metadata = metadata

class KBPreprocessor:
    def __init__(self, model_id: str = settings.EMBEDDING_MODEL_ID):
        logger.info(f"Loading embedding model: {model_id}")
        self.model = SentenceTransformer(model_id)

    def _chunk_text(self, text: str, max_sentences: int = 5) -> List[str]:
        """Chunk by sentence count; simple heuristic."""
        sentences = sent_tokenize(text)
        chunks = []
        for i in range(0, len(sentences), max_sentences):
            chunk = " ".join(sentences[i:i+max_sentences])
            chunks.append(chunk)
        return chunks

    def ingest_document(self, path: pathlib.Path) -> List[DocumentChunk]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        doc_id = hashlib.sha256(str(path).encode("utf-8")).hexdigest()
        logger.info(f"Ingesting document {path} as doc_id {doc_id}")
        chunks = self._chunk_text(text)
        chunk_objs = []
        for idx, chunk in enumerate(chunks):
            metadata = {
                "source_path": str(path),
                "doc_id": doc_id,
                "chunk_id": idx
            }
            chunk_objs.append(DocumentChunk(doc_id=doc_id, chunk_id=idx, text=chunk, metadata=metadata))
        return chunk_objs

    def ingest_directory(self, dir_path: str) -> List[DocumentChunk]:
        p = pathlib.Path(dir_path)
        all_chunks = []
        for file in p.rglob("*.txt"):
            all_chunks.extend(self.ingest_document(file))
        return all_chunks
```

---

### `backend/app/knowledge_base/indexer.py`

```python
import os
import logging
from typing import List

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from .preprocessor import DocumentChunk
from ..config import settings

logger = logging.getLogger(__name__)

class KBIndexer:
    def __init__(self, persist_directory: str = settings.CHROMA_PERSIST_DIRECTORY, collection_name: str = settings.CHROMA_COLLECTION_NAME):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        logger.info(f"Initializing Chroma client with persist_directory={persist_directory}")
        self.client = chromadb.Client(ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory))
        if collection_name in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.collection = self.client.create_collection(name=collection_name)

    def index_chunks(self, chunks: List[DocumentChunk]):
        texts = [c.text for c in chunks]
        metadatas = [c.metadata for c in chunks]
        ids = [f"{c.doc_id}__{c.chunk_id}" for c in chunks]
        logger.info(f"Embedding {len(texts)} chunks and indexing into Chroma collection {self.collection_name}")
        # Here we embed using SentenceTransformer; if you want use model directly, could use self.model
        # But we assume the embeddings happen at this step
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.EMBEDDING_MODEL_ID)
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        self.collection.add(ids=ids, embeddings=embeddings.tolist(), metadatas=metadatas, documents=texts)
        self.client.persist()
        logger.info("Index persisted")

    def query(self, query_text: str, top_k: int = settings.KB_TOP_K):
        logger.info(f"Querying Chroma for top_k={top_k}: {query_text}")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.EMBEDDING_MODEL_ID)
        query_embedding = model.encode([query_text], convert_to_numpy=True)[0]
        results = self.collection.query(query_embeddings=[query_embedding.tolist()], n_results=top_k, include=[ "documents", "metadatas", "distances"])
        return results
```

---

### `backend/app/tools/rag_tool.py`

```python
import logging
from typing import List, Dict

from ..knowledge_base.indexer import KBIndexer

logger = logging.getLogger(__name__)

class RAGTool:
    def __init__(self):
        self.indexer = KBIndexer()

    def retrieve(self, query: str, top_k: int = None) -> List[Dict]:
        top_k = top_k or  settings.KB_TOP_K
        results = self.indexer.query(query, top_k=top_k)
        docs = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            docs.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })
        logger.info(f"RAG retrieved {len(docs)} docs for query: \"{query}\"")
        return docs

    def format_for_agent(self, retrieved: List[Dict]) -> str:
        """Format the retrieved docs into a textual prompt for agent context."""
        formatted = []
        for i, r in enumerate(retrieved):
            formatted.append(f"[{i+1}] Source: {r['metadata'].get('source_path')} | Chunk {r['metadata'].get('chunk_id')} | Text: {r['text']}")
        return "\n".join(formatted)
```

---

### `backend/app/config.py` (updates)

Include new configuration parameters:

```python
class Settings(BaseSettings):
    ...
    # RAG / Knowledge base
    EMBEDDING_MODEL_ID: str = "google/embeddinggemma-300m"
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "support_kb"
    KB_CHUNK_SIZE_SENTENCES: int = 5
    KB_TOP_K: int = 5
    ...
```

---

### `backend/tests/unit/test_preprocessor.py`

```python
import tempfile
import pathlib
import os
import pytest
from backend.app.knowledge_base.preprocessor import KBPreprocessor

@pytest.fixture(scope="module")
def sample_text_file(tmp_path_factory):
    d = tmp_path_factory.mktemp("kbdocs")
    file = d / "doc1.txt"
    file.write_text("This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five. This is sentence six.")
    return str(file)

def test_ingest_document(sample_text_file):
    pre = KBPreprocessor()
    chunks = pre.ingest_document(pathlib.Path(sample_text_file))
    assert len(chunks) == 2
    assert all(hasattr(c, "text") for c in chunks)
    assert chunks[0].metadata["chunk_id"] == 0
    assert chunks[1].metadata["chunk_id"] == 1
```

---

### `backend/tests/integration/test_rag_tool.py`

```python
import pathlib
import shutil
import tempfile
from backend.app.knowledge_base.preprocessor import KBPreprocessor
from backend.app.knowledge_base.indexer import KBIndexer
from backend.app.tools.rag_tool import RAGTool

def test_rag_pipeline(tmp_path):
    # Setup temporary persist directory
    persist_dir = tmp_path / "chroma_persist"
    from backend.app.config import settings
    settings.CHROMA_PERSIST_DIRECTORY = str(persist_dir)
    # Ingest sample doc
    doc = tmp_path / "doc2.txt"
    doc.write_text("Support documentation about return policy. Customers can return product within 30 days. Refund will be processed within 5 business days.")
    pre = KBPreprocessor()
    chunks = pre.ingest_document(doc)
    indexer = KBIndexer(persist_directory=str(persist_dir))
    indexer.index_chunks(chunks)
    # Query via RAGTool
    rag = RAGTool()
    results = rag.retrieve("How many days to return a product?")
    assert len(results) > 0
    formatted = rag.format_for_agent(results)
    assert "return product within 30 days" in formatted
```

