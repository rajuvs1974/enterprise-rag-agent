# Enterprise RAG Agent

A production-oriented, cloud-neutral Enterprise RAG Agent platform built using Spec-Driven Development.

The platform is being developed **AWS-first** and will subsequently be deployed to **Azure**, while keeping the core application architecture vendor neutral.

---

## 🎯 Vision

Build an enterprise-grade RAG Agent capable of securely ingesting, processing, indexing, retrieving, and reasoning over enterprise documents.

The target architecture is designed to scale toward **10M+ documents** while supporting:

* Hybrid search
* Vector retrieval
* Metadata filtering
* Reranking
* Agentic RAG
* Document versioning
* Incremental updates
* Tombstone deletion
* Multi-tenancy
* Document-level authorization
* Citations
* RAG evaluation
* Observability
* Terraform-based infrastructure
* GitHub Actions CI/CD
* AWS and Azure deployments

---

## 🏗️ Engineering Principles

The project follows a formal engineering constitution defined in:

```text
specs/constitution.md
```

Key principles:

* Spec-Driven Development
* Cloud neutrality
* API-first architecture
* Security by default
* Retrieval before generation
* Evaluation-driven AI
* Observability
* Infrastructure as Code
* Automated CI/CD
* Testability
* Scalability
* Cost-conscious engineering

---

## 🧰 Technology Stack

### Application

* Python 3.12
* FastAPI
* Pydantic
* Pydantic Settings

### Development

* uv
* Ruff
* MyPy
* Pytest
* Docker

### Data & Search

Planned:

* PostgreSQL
* OpenSearch
* Object storage
* Vector search
* Hybrid retrieval

### AI

Planned:

* Configurable LLM provider
* Configurable embedding provider
* Reranking
* LangGraph-based agent orchestration
* RAG evaluation

### Cloud

Initial:

* AWS

Future:

* Azure

### Infrastructure & DevOps

* Terraform
* GitHub
* GitHub Actions
* Docker
* OpenTelemetry

---

## 📁 Repository Structure

```text
enterprise-rag-agent/
│
├── .github/
│   └── workflows/
│
├── specs/
│   ├── constitution.md
│   └── 001-project-foundation/
│
├── src/
│   └── erap/
│       ├── api/
│       ├── application/
│       ├── config/
│       ├── domain/
│       ├── infrastructure/
│       └── observability/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── terraform/
│   ├── modules/
│   └── aws/
│
└── docker/
```

---

## 🚀 Local Development

### Prerequisites

Install:

* Python 3.12
* uv
* Git
* Docker

This project uses **uv exclusively for Python environment and dependency management**.

---

### Install dependencies

Clone the repository:

```bash
git clone <repository-url>
cd enterprise-rag-agent
```

Synchronize the environment:

```bash
uv sync
```

---

## ▶️ Run the API

Start the FastAPI application:

```bash
uv run uvicorn erap.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ❤️ Health Checks

Application health:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

Application readiness:

```bash
curl http://127.0.0.1:8000/ready
```

Expected:

```json
{
  "status": "ready"
}
```

---
## 🔍 Observability Foundation

The API includes a basic observability foundation:

- Application logging
- Request correlation IDs
- `X-Request-ID` propagation
- Health and readiness endpoints

Each HTTP request receives a correlation ID.

Clients may provide their own:

```bash
curl \
  -H "X-Request-ID: portfolio-test-001" \
  http://127.0.0.1:8000/health

## 🧪 Testing

Run the test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

Run MyPy:

```bash
uv run mypy src
```

All three are intended to become CI quality gates.

---

## 📋 Spec-Driven Development

Development follows:

```text
Specification
      ↓
Design
      ↓
Implementation Plan
      ↓
Tasks
      ↓
Implementation
      ↓
Tests
      ↓
Evaluation
      ↓
Documentation
```

Major functionality will have a corresponding specification under:

```text
specs/
```

---

## 🗺️ Roadmap

### Phase 1 — Foundation

- [x] GitHub repository
- [x] uv-based Python project
- [x] FastAPI
- [x] Pydantic Settings
- [x] Health endpoint
- [x] Readiness endpoint
- [x] Testing foundation
- [x] Ruff
- [x] MyPy
- [x] Application logging
- [x] Request correlation IDs
- [x] Centralized exception handling
- [ ] PostgreSQL
- [ ] Docker Compose
- [ ] GitHub Actions

### Phase 2 — RAG Platform

* [ ] Document ingestion
* [ ] Document parsing
* [ ] Chunking
* [ ] Embeddings
* [ ] Indexing
* [ ] Hybrid retrieval
* [ ] Metadata filtering
* [ ] Reranking
* [ ] Citations

### Phase 3 — Enterprise

* [ ] Document versioning
* [ ] Incremental updates
* [ ] Tombstone deletion
* [ ] Multi-tenancy
* [ ] RBAC
* [ ] Document ACLs
* [ ] Audit logging

### Phase 4 — Agentic AI

* [ ] RAG Agent
* [ ] Query planning
* [ ] Tool execution
* [ ] Retrieval refinement
* [ ] Grounded response generation
* [ ] Guardrails

### Phase 5 — AI Evaluation & Observability

* [ ] Golden datasets
* [ ] Retrieval evaluation
* [ ] Generation evaluation
* [ ] Regression evaluation
* [ ] Distributed tracing
* [ ] Metrics
* [ ] Cost monitoring

### Phase 6 — Cloud

* [ ] AWS Terraform deployment
* [ ] AWS CI/CD
* [ ] AWS production architecture
* [ ] Load testing
* [ ] Azure Terraform deployment
* [ ] Azure CI/CD
* [ ] Multi-cloud validation

---

## 🎯 Project Goal

The final platform should demonstrate production-level capabilities across:

```text
AI Engineering
    +
Software Engineering
    +
Cloud Engineering
    +
DevOps
    +
Security
    +
System Architecture
```

The goal is not simply to build a RAG chatbot.

The goal is to demonstrate how to **design, build, deploy, evaluate, secure, observe, and operate an enterprise AI platform.**
