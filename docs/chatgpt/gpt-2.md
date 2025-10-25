Here’s our detailed **Phase 2 – Build plan (Sprint A)** for the skeleton and core backend, aligned with the *Production-Ready* track. 

---

## Phase 2 Sprint A – Skeleton & Core Backend

### Objectives

* Set up repository structure, foundational configuration, and baseline modules.
* Implement the basic backend service: REST endpoints, memory tool (SQLite), basic agent setup with Microsoft Agent Framework (Python) according to the programming guide. ([Microsoft Learn][1])
* Provide unit tests for the memory and agent interface.
* Configure CI (GitHub Actions) for linting, unit tests, build.
* Create Dockerfile and docker-compose stub (Chroma placeholder) for local dev.

### Deliverables in this Sprint

1. **Repository skeleton**

   * Root README.md with overview, architecture summary, tech stack list.
   * `backend/` directory with modules: `app`, `tools`, `db`, `config`, etc.
   * `tests/` directory: `unit/` with initial tests.
   * `.github/workflows/ci.yml` template for CI.
   * `Dockerfile`, `docker-compose.yml` (with placeholder for Chroma, SQLite volume).
   * `requirements.txt` or `pyproject.toml` locking dependencies.
2. **Configuration & startup**

   * `backend/app/main.py` to start FastAPI, define `/healthz` endpoint.
   * `backend/app/config.py` to load environment variables (via `pydantic`).
   * Logging config (`backend/app/logging_config.py`) with structured logging.
   * Metrics stub (`backend/app/metrics.py`) exposing Prometheus metrics.
3. **Memory tool implementation**

   * `backend/app/tools/memory_tool.py` with class `MemoryTool` that interfaces with SQLite using `SQLAlchemy`.
   * `backend/app/db/sqlite.py` with SQLAlchemy engine setup, session factory.
   * SQLite schema definition (e.g., `sessions`, `messages`, `memory_entries`).
   * Unit tests for memory tool (CRUD operations).
4. **Agent setup**

   * `backend/app/agents.py`: set up basic agent using Microsoft Agent Framework (Python) as an Assistants client.
   * Create stub tool registration (memory tool integrated).
   * Endpoint `POST /chat/message` stub that receives message, calls agent, returns dummy response.
   * Unit test for endpoint (mock agent response).
5. **CI configuration**

   * GitHub Actions config: lint (flake8/black), unit tests (pytest), coverage.
   * Ensure fails on lint errors or test failures.
6. **Docker & Dev Setup**

   * Dockerfile: base Python 3.12 image, install dependencies, set working directory.
   * docker-compose.yml: services: backend, vector-db (placeholder for Chroma). SQLite as volume.
   * README instructions: “Run `docker-compose up` to start backend + placeholder DB.”
7. **Acceptance criteria for this Sprint**

   * Backend starts locally and serves `/healthz` returning 200 OK.
   * Memory tool unit tests pass locally.
   * CI config defined and passes locally (for lint + unit tests).
   * Docker compose starts backend without error (even if Chroma service is placeholder).
   * README clearly describes how to build/run, test, lint.
   * Code passes lint checks (flake8/black) and type checks (`mypy`).
   * Logging and metrics endpoints stub are present (though functionality minimal).
   * The architecture doc from Phase 1 is referenced in README for context.

### Timeline & Checkpoints

* **Day 1-2**: Setup repo skeleton, dependencies, config files.
* **Day 3-4**: Implement memory tool and SQLite schema, unit tests.
* **Day 5**: Implement agent stub + `/chat/message` endpoint.
* **Day 6**: Write CI config, Dockerfile/docker-compose, update README.
* **Day 7**: Review & polish, ensure acceptance criteria met, prepare for Sprint B plan.

### Risks & Mitigation

* Risk: Integrating Microsoft Agent Framework might have unexpected complications — mitigate by building minimal stub, and leaving full tool integration for later sprints.
* Risk: SQLite concurrency limits might block future integration — mitigate by designing abstraction so switching to PostgreSQL later is straightforward.
* Risk: Vector DB placeholder may delay dependencies — mitigate by isolating vector DB dependency until Sprint B.



[1]: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview?utm_source=chatgpt.com "Introduction to Microsoft Agent Framework | Microsoft Learn"
