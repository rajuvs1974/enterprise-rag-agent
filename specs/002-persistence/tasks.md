# Spec 002 — Persistence Layer Tasks

**Specification:** `002-persistence/spec.md`
**Implementation Plan:** `002-persistence/plan.md`
**Status:** Ready for implementation

---

# Phase 1 — Dependencies & Configuration

## T001 — Add persistence dependencies

Add the required packages using `uv`.

Expected dependencies:

* SQLAlchemy 2.x
* PostgreSQL async driver
* Alembic

Acceptance criteria:

* Dependencies are present in `pyproject.toml`.
* `uv.lock` is updated.
* `uv sync` succeeds.

---

## T002 — Add database configuration

Extend Pydantic Settings with database configuration.

Initial configuration:

```text
DATABASE_URL
```

Acceptance criteria:

* Database URL is configurable through environment variables.
* No credentials are hard-coded.
* Configuration has unit tests.
* Application starts without a database configured during the initial development phase.

---

# Phase 2 — Database Infrastructure

## T003 — Create persistence package

Create:

```text
src/erap/infrastructure/
└── persistence/
    ├── __init__.py
    ├── database.py
    ├── models/
    └── repositories/
```

Acceptance criteria:

* Persistence code is isolated under infrastructure.
* Domain/application layers do not import SQLAlchemy.

---

## T004 — Implement async database engine

Create the SQLAlchemy async engine.

Requirements:

* Async SQLAlchemy engine
* Configuration-driven database URL
* Connection pooling configuration
* No global database sessions

Acceptance criteria:

* Engine can be created from configuration.
* Application can initialize the persistence layer.
* Database connection errors are handled appropriately.

---

## T005 — Implement database session factory

Create an async session factory.

Requirements:

* One session per unit of work/request.
* Sessions are properly closed.
* Transactions are explicit.
* No session stored globally.

Acceptance criteria:

* Session lifecycle is tested.
* Commit and rollback behavior is defined.

---

# Phase 3 — Database Models

## T006 — Create declarative base

Create the SQLAlchemy declarative base.

Requirements:

* Common base model
* UUID primary-key support where appropriate
* Timestamp support
* Typed SQLAlchemy mappings

Acceptance criteria:

* All persistence models can inherit from the common base.
* MyPy passes.

---

## T007 — Implement Tenant model

Create the `tenants` table.

Fields:

```text
id
name
status
created_at
updated_at
```

Acceptance criteria:

* UUID primary key.
* Required fields enforced.
* Migration created.
* Model tests added.

---

## T008 — Implement Document model

Create the `documents` table.

Fields:

```text
id
tenant_id
external_id
source
filename
mime_type
status
current_version_id
created_at
updated_at
deleted_at
```

Acceptance criteria:

* Tenant relationship exists.
* `(tenant_id, source, external_id)` uniqueness is enforced.
* Lifecycle status is represented explicitly.
* Tombstoning is supported.
* Migration created.

---

## T009 — Implement DocumentVersion model

Create the `document_versions` table.

Fields:

```text
id
document_id
version_number
content_hash
object_uri
size_bytes
status
created_at
```

Acceptance criteria:

* Version belongs to exactly one document.
* Version number is unique per document.
* Content hash is stored.
* Versions are treated as immutable.
* Migration created.

---

## T010 — Implement DocumentACL model

Create the `document_acls` table.

Fields:

```text
id
document_id
principal_type
principal_id
permission
created_at
```

Acceptance criteria:

* ACL belongs to a document.
* Principal information is represented.
* Permission is explicit.
* Appropriate indexes exist.

---

## T011 — Implement ProcessingJob model

Create the `processing_jobs` table.

Fields:

```text
id
document_version_id
job_type
status
attempt
started_at
completed_at
error_code
error_message
created_at
```

Acceptance criteria:

* Job belongs to a document version.
* Job status is explicit.
* Retry attempts are tracked.
* Errors can be recorded safely.

---

## T012 — Implement AuditEvent model

Create the `audit_events` table.

Fields:

```text
id
tenant_id
actor_id
event_type
resource_type
resource_id
metadata
created_at
```

Acceptance criteria:

* Audit events are append-only.
* Tenant ownership is represented.
* Event metadata supports structured JSON.
* Sensitive document content is not stored.

---

# Phase 4 — Database Migrations

## T013 — Configure Alembic

Configure Alembic to discover SQLAlchemy models.

Acceptance criteria:

* Alembic configuration is committed.
* Database URL comes from configuration.
* No credentials are committed.

---

## T014 — Create initial migration

Generate the initial database migration.

Migration MUST create:

```text
tenants
documents
document_versions
document_acls
processing_jobs
audit_events
```

Acceptance criteria:

* Migration runs successfully on an empty PostgreSQL database.
* Migration rollback succeeds.
* Migration is deterministic.

---

# Phase 5 — Domain Models

## T015 — Define domain entities

Create domain representations separate from SQLAlchemy models.

Expected location:

```text
src/erap/domain/
├── tenant.py
├── document.py
├── document_version.py
├── document_acl.py
├── processing_job.py
└── audit_event.py
```

Acceptance criteria:

* Domain models do not import SQLAlchemy.
* Domain models contain business concepts rather than persistence concerns.
* Pydantic is used where appropriate.

---

# Phase 6 — Repository Interfaces

## T016 — Define TenantRepository

Define the application/domain repository contract.

Initial operations:

```text
get_by_id
create
```

Acceptance criteria:

* Interface does not depend on SQLAlchemy.
* Tenant context is respected.

---

## T017 — Define DocumentRepository

Initial operations:

```text
get_by_id
get_by_external_id
create
update_status
tombstone
```

Acceptance criteria:

* Tenant ID is part of tenant-scoped operations.
* Repository contract does not expose SQL.
* Tombstone behavior is represented.

---

## T018 — Define DocumentVersionRepository

Initial operations:

```text
get
list_versions
create
get_latest
```

Acceptance criteria:

* Versions are associated with documents.
* Version immutability is respected.

---

## T019 — Define remaining repository interfaces

Create:

```text
DocumentACLRepository
ProcessingJobRepository
AuditRepository
```

Acceptance criteria:

* Interfaces are business-oriented.
* Infrastructure implementation details do not leak into interfaces.

---

# Phase 7 — PostgreSQL Repository Implementations

## T020 — Implement TenantRepository

Implement the PostgreSQL repository.

Acceptance criteria:

* CRUD operations work.
* Transactions behave correctly.
* Errors are translated into application-level errors.

---

## T021 — Implement DocumentRepository

Implement document persistence.

Acceptance criteria:

* Tenant-scoped reads work.
* External ID uniqueness works.
* Lifecycle transitions work.
* Tombstone operation works.

---

## T022 — Implement DocumentVersionRepository

Implement version persistence.

Acceptance criteria:

* Versions can be created.
* Version ordering works.
* Previous versions remain accessible.
* Concurrent version creation is handled.

---

## T023 — Implement ACL repository

Acceptance criteria:

* ACLs can be created.
* ACLs can be queried by document/principal.
* Duplicate ACL behavior is defined.

---

## T024 — Implement ProcessingJob repository

Acceptance criteria:

* Jobs can be created.
* Jobs can be queried by status.
* Retry attempts can be updated.
* Failed jobs retain useful error information.

---

## T025 — Implement Audit repository

Acceptance criteria:

* Audit events can be appended.
* Events can be queried.
* Existing audit events cannot be modified through normal repository operations.

---

# Phase 8 — Transactions & Consistency

## T026 — Implement transaction boundary

Define the application-level transaction boundary.

Example:

```text
Create Version
      │
      ├── Create version
      ├── Update current version
      └── Create processing job
              │
              ▼
           COMMIT
```

Acceptance criteria:

* All related database changes commit atomically.
* Failure causes rollback.
* Partial database state cannot remain.

---

## T027 — Implement concurrency protection

Protect against concurrent document/version updates.

Acceptance criteria:

* Duplicate versions cannot be created accidentally.
* Concurrent updates are detected or safely serialized.
* Tests demonstrate the behavior.

---

# Phase 9 — Tenant Isolation

## T028 — Add tenant isolation tests

Test:

```text
Tenant A
   │
   └── Document A

Tenant B
   │
   └── Document B
```

Tenant A MUST NOT retrieve Document B.

Acceptance criteria:

* Cross-tenant reads fail.
* Cross-tenant updates fail.
* Cross-tenant tombstones fail.
* Tests run against real PostgreSQL.

---

# Phase 10 — Tombstone & Versioning

## T029 — Test document tombstones

Verify:

```text
ACTIVE
  ↓
TOMBSTONED
```

Acceptance criteria:

* Tombstoned document is not returned by normal retrieval.
* Audit event is created.
* Historical metadata remains available.

---

## T030 — Test document versioning

Verify:

```text
v1 → SUPERSEDED
v2 → ACTIVE
```

Acceptance criteria:

* Version history is retained.
* Current version is correctly identified.
* Historical versions remain immutable.

---

# Phase 11 — Integration Testing

## T031 — Add PostgreSQL Docker Compose service

Create local PostgreSQL infrastructure.

Acceptance criteria:

* PostgreSQL starts through Docker Compose.
* Application can connect using `DATABASE_URL`.
* Credentials are supplied through environment configuration.

---

## T032 — Create integration-test fixtures

Create reusable PostgreSQL test fixtures.

Acceptance criteria:

* Tests can create isolated test data.
* Database state is cleaned between tests.
* Tests do not depend on developer-specific local state.

---

## T033 — Run migration integration tests

Test:

```text
empty database
      ↓
migration
      ↓
schema
      ↓
repository
```

Acceptance criteria:

* Fresh database migration succeeds.
* Schema matches SQLAlchemy models.
* Rollback behavior is verified where practical.

---

# Phase 12 — Error Handling

## T034 — Map database exceptions

Translate infrastructure exceptions into application errors.

Examples:

```text
UniqueViolation
      ↓
DocumentAlreadyExistsError

ForeignKeyViolation
      ↓
InvalidReferenceError

DatabaseUnavailable
      ↓
PersistenceUnavailableError
```

Acceptance criteria:

* Database-specific exceptions do not reach API clients.
* Errors contain appropriate error codes.
* Request IDs are preserved.

---

# Phase 13 — Performance & Indexes

## T035 — Validate database indexes

Verify indexes for:

```text
documents:
    tenant_id
    status
    tenant_id + source + external_id

document_versions:
    document_id
    document_id + version_number
    content_hash

document_acls:
    document_id
    principal_id

processing_jobs:
    document_version_id
    status

audit_events:
    tenant_id
    resource_id
    created_at
```

Acceptance criteria:

* Indexes exist in the migration.
* Common queries use expected indexes.
* No unnecessary indexes are introduced.

---

# Phase 14 — Quality Gates

## T036 — Run unit tests

```bash
uv run pytest tests/unit
```

Acceptance criteria:

* All unit tests pass.

---

## T037 — Run integration tests

```bash
uv run pytest tests/integration
```

Acceptance criteria:

* All PostgreSQL integration tests pass.

---

## T038 — Run Ruff

```bash
uv run ruff check .
```

Acceptance criteria:

```text
All checks passed!
```

---

## T039 — Run MyPy

```bash
uv run mypy src
```

Acceptance criteria:

```text
Success: no issues found
```

---

# Phase 15 — Documentation

## T040 — Update README

Document:

* PostgreSQL architecture
* Local PostgreSQL setup
* Database configuration
* Migration commands
* Test commands
* Persistence architecture

Acceptance criteria:

* README accurately reflects the implementation.

---

# Phase 16 — Completion

## T041 — Final Spec 002 validation

Verify all acceptance criteria in:

```text
specs/002-persistence/spec.md
```

Acceptance criteria:

* Specification requirements are satisfied.
* Tests cover critical requirements.
* Documentation is updated.
* No known critical persistence defects remain.

---

## T042 — Commit Persistence Layer

Create a final milestone commit:

```bash
git add .
git commit -m "feat: implement persistence layer"
git push
```

---

# Definition of Done

Spec 002 is complete only when:

```text
Specification          ✅
Implementation         ✅
Database migrations    ✅
Repository contracts  ✅
PostgreSQL repos       ✅
Unit tests             ✅
Integration tests      ✅
Tenant isolation       ✅
Versioning             ✅
Tombstones             ✅
Transactions            ✅
Error mapping          ✅
Indexes                 ✅
Ruff                    ✅
MyPy                    ✅
README                  ✅
GitHub                  ✅
```

The resulting persistence layer MUST remain independent of AWS- or Azure-specific database APIs.
