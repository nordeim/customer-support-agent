Here’s the detailed plan for **Sprint B – RAG + Knowledge Base Ingestion**, aligned with our *Production-Ready* track. Please review and validate; once you approve, I’ll proceed with implementation.

---

## Sprint B Objectives

* Ingest a knowledge-base of support documents (e.g., FAQs, manuals, policy docs) into a vector store.
* Implement retrieval-augmented generation (RAG) tool in backend: embed user queries with SentenceTransformer using EmbeddingGemma‑300M from Google. ([Hugging Face][1])
* Integrate vector store using ChromaDB (via Python client). ([LangChain Docs][2])
* Expose backend endpoints to support document ingestion (batch) and query-flow (agent RAG tool).
* Write tests (unit + integration) for embedding ingestion, search, tool invocation.
* Update CI config as needed.
* Provide documentation for ingestion process, format of KB, and configuration for vector store persistence.

---

## Module / Component Breakdown

* `backend/app/knowledge_base/`

  * `preprocessor.py`: load documents (PDF, Markdown, text etc), chunk them (e.g., 500-token chunks), embed with EmbeddingGemma, prepare metadata.
  * `indexer.py`: interface with Chroma—create collection, add embeddings + docs + metadata, persist store.
* `backend/app/tools/rag_tool.py`: RAG tool for agent: given a user query and session context, embed query, search vector store (top-K), return relevant docs (with metadata) to agent, along with citations.
* `backend/app/config.py`: add config for vector store (e.g., `CHROMA_PERSIST_DIRECTORY`, collection name, max_documents, chunk_size).
* `backend/app/db/models.py` (if needed): potentially store metadata of ingestion (document_id, ingest_timestamp, version).
* Unit tests: `tests/unit/test_preprocessor.py`, `tests/unit/test_indexer.py`, `tests/integration/test_rag_tool.py`.
* Integration: After ingestion, query via `/chat/message` endpoint, ensure RAG tool is called and response contains citations.

---

## Acceptance Criteria

* Knowledge base ingestion script runs, ingesting at least one sample document, embeddings created and stored in Chroma collection.
* Querying the RAG tool returns relevant documents (based on a test query) with metadata.
* Agent flow: When agent is invoked via `/chat/message`, the RAG tool is used (stub + test) and output includes citations.
* Tests (unit + integration) pass. Coverage for new modules meets threshold (e.g., ≥ 80% for those parts).
* Vector store persistence: Chroma store configured to persist to disk (so re-startup doesn’t lose embeddings).
* Performance baseline documented: embedding time, retrieval latency (for sample corpus).
* Documentation added: ingestion instructions (how to add docs, how to update index).
* CI workflow extended to include new tests.
* Configuration parameters validated (chunk size, top-K retrieval, etc).
* Metrics: add metrics counters for RAG tool invocations (e.g., `rag_tool_invocations_total`, `rag_query_latency_seconds`).

---

## Timeline & Milestones

* **Day 1**: Document format specification, implement `preprocessor.py` (document load + chunking).
* **Day 2**: Implement embedding pipeline using EmbeddingGemma, test load of model.
* **Day 3**: Implement `indexer.py` for Chroma: create collection, add embeddings, persistent store. Unit tests for ingestion components.
* **Day 4**: Implement `rag_tool.py`: query embedding, Chroma search, result struct. Integration test for retrieval accuracy.
* **Day 5**: Integrate RAG tool into agent flow (`/chat/message` endpoint) stub, ensure citations are passed, build integration test.
* **Day 6**: Add metrics and logging for RAG tool, update CI config, update README/instructions.
* **Day 7**: Review, polish, document ingestion process, evaluate performance, prepare for next sprint.

---

## Risks & Mitigations

* **Risk**: EmbeddingGemma large model may have latency; mitigate by caching embeddings for documents, chunking appropriately, maybe use GPU if available.
* **Risk**: ChromaDB persistence and performance issues; mitigate by starting with embedded mode/persistent directory and document size small; include tests for retrieval latency.
* **Risk**: Retrieval relevance may be poor (wrong chunks, metadata missing); mitigate by chunk size tuning, metadata design, and integration tests to validate.
* **Risk**: Large knowledge base may exceed memory limits; mitigate by designing ingestion to run batch, include config for chunking and filtering, and note for future scaling (weaviate/pinecone).
* **Risk**: Agent tool integration complexity; mitigate by building tool in isolation, integration tests, clear interface.

---

## Metrics / SLIs for this Sprint

* Latency of embedding document ingestion (target: < 2 s per document chunk)
* Latency of retrieval query (target: < 500 ms for top-K retrieval on sample corpus)
* Retrieval accuracy test pass rate (unit/integration tests)
* RAG tool invocation count + error rate.

---

## Dependencies & Resources Needed

* Sample knowledge base documents (PDFs/Markdown) from you or test set to ingest.
* Access to compute environment that supports EmbeddingGemma (may need GPU or CPU fallback).
* ChromaDB persistence directory (config).
* Agent Framework stub (already set up) ready for integration.
* Attachment of license acceptance for EmbeddingGemma (Hugging Face gated model) — ensure licensing correct.

---

## Key Configuration Parameters to Define

* `KB_CHUNK_SIZE` (e.g., 500 tokens)
* `KB_TOP_K` for retrieval (e.g., 5)
* `EMBEDDING_MODEL_ID` = `"google/embeddinggemma-300m"`
* `CHROMA_COLLECTION_NAME` = `"support_kb"`
* `CHROMA_PERSIST_DIRECTORY` = `./data/chroma_db`
* `EMBEDDING_BATCH_SIZE` (e.g., 32)
* `INGESTION_PARALLELISM` (e.g., number of threads)

---

## Integration & CI Updates

* Add new unit/integration test target for knowledge_base modules.
* Possibly update CI job to include environment variable for embedding model license check or skip tests if model not downloaded (mark as optional for CI).
* Docker-Compose: add volume for Chroma persistent store (e.g., `./backend/data/chroma_db:/app/data/chroma_db`).
* README update: add “Knowledge base ingestion” section.

---

[1]: https://huggingface.co/google/embeddinggemma-300m?utm_source=chatgpt.com "google/embeddinggemma-300m · Hugging Face"
[2]: https://docs.langchain.com/oss/python/integrations/vectorstores/chroma?utm_source=chatgpt.com "Chroma - Docs by LangChain"
