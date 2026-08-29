# Spec 002 — Persistence Layer

**Status:** Draft
**Version:** 1.0
**Depends on:** Constitution v1.0
**Target:** PostgreSQL

---

## 1. Objective

Establish PostgreSQL as the system of record for enterprise document metadata, document lifecycle state, tenant information, authorization metadata, processing state, and audit information.

PostgreSQL MUST NOT become tightly coupled to the RAG retrieval implementation.

Search and retrieval indexes will be maintained separately.

---

## 2. Responsibilities

PostgreSQL will own:

* Tenant metadata
* Document identity
* Document metadata
* Document versions
* Document lifecycle state
* Processing state
* Document authorization metadata
* Audit events
* Index synchronization state

PostgreSQL will NOT own:

* Raw document binaries
* Embedding vectors as the primary vector store
* Search indexes
* LLM prompts/responses as the primary data store

---

## 3. High-Level Architecture

```text
                         Enterprise RAG Platform
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
               PostgreSQL        S3        OpenSearch
                    │             │             │
                    │             │             ├── BM25
                    │             │             ├── Vector
                    │             │             └── Hybrid Search
                    │             │
                    │             └── Raw documents
                    │
                    ├── Tenants
                    ├── Documents
                    ├── Versions
                    ├── ACLs
                    ├── Processing
                    ├── Index state
                    └── Audit
```

---

# 4. Entity Model

The initial persistence model contains:

```text
Tenant
  │
  └── Document
        │
        ├── DocumentVersion
        │
        ├── DocumentACL
        │
        └── ProcessingJob

AuditEvent
```

---

# 5. Tenant

A tenant represents an enterprise/customer boundary.

### Required attributes

```text
id
name
status
created_at
updated_at
```

### Requirements

* Tenant IDs MUST be globally unique.
* Tenant data MUST be logically isolated.
* Every document MUST belong to exactly one tenant.
* Tenant ID MUST be available throughout the document processing pipeline.
* Queries MUST NOT permit accidental cross-tenant access.

---

# 6. Document

A Document represents the logical identity of an enterprise document.

A document is distinct from its individual versions.

### Required attributes

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

### Requirements

* `id` MUST be immutable.
* `tenant_id` MUST be immutable.
* `external_id` SHOULD identify the document in its source system.
* `(tenant_id, source, external_id)` SHOULD be unique.
* A document MAY have multiple versions.
* A document MUST have at most one current active version.
* Deletion MUST NOT immediately destroy audit history.

---

# 7. Document Version

A DocumentVersion represents a specific immutable representation of a document.

### Required attributes

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

### Requirements

* Version numbers MUST be monotonically increasing for a document.
* A version MUST NOT be modified after becoming immutable.
* Content hash MUST uniquely identify the stored content representation.
* The raw content SHOULD be stored outside PostgreSQL.
* `object_uri` SHOULD reference the object-storage location.
* Previous versions MUST remain available for audit/reproducibility according to retention policy.

Example:

```text
Document: employee-handbook

Version 1
   │
   ├── content_hash = abc123
   └── SUPERSEDED

Version 2
   │
   ├── content_hash = def456
   └── ACTIVE
```

---

# 8. Document Lifecycle

A Document lifecycle state represents whether the logical document is available to users.

Initial states:

```text
ACTIVE
TOMBSTONED
```

### ACTIVE

The document is eligible for retrieval subject to authorization.

### TOMBSTONED

The document has been logically deleted.

A tombstoned document:

* MUST NOT be returned by normal retrieval.
* MUST NOT be included in newly generated LLM context.
* MUST remain auditable.
* SHOULD retain metadata required for compliance and troubleshooting.

Physical deletion may occur later according to retention policy.

---

# 9. Processing State

Processing state represents the state of asynchronous document processing.

Initial states:

```text
DISCOVERED
INGESTING
PARSING
CHUNKING
EMBEDDING
INDEXING
COMPLETED
FAILED
```

Processing state MUST be separate from document lifecycle state.

Example:

```text
Document Status
     ACTIVE

Processing Status
     INDEXING
```

This separation allows a document to remain logically active while a new version is being processed.

---

# 10. Document ACL

DocumentACL stores authorization metadata associated with a document.

### Required attributes

```text
id
document_id
principal_type
principal_id
permission
created_at
```

Examples of principals:

```text
USER
GROUP
ROLE
```

Permissions may initially include:

```text
READ
```

Future permissions may include:

```text
WRITE
DELETE
ADMIN
```

### Security requirement

Authorization filtering MUST occur before retrieved content is supplied to the LLM.

The system MUST NOT:

```text
Retrieve unauthorized document
        ↓
Send to LLM
        ↓
Filter answer afterward
```

Instead:

```text
User Identity
     ↓
Authorization Context
     ↓
Search Filter
     ↓
Authorized Documents
     ↓
LLM Context
```

---

# 11. Processing Job

ProcessingJob represents an asynchronous document processing operation.

### Required attributes

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

Initial job types:

```text
INGEST
PARSE
CHUNK
EMBED
INDEX
DELETE_INDEX
```

### Requirements

* Jobs SHOULD be idempotent.
* Failed jobs SHOULD be retryable.
* Attempts MUST be tracked.
* Errors MUST be recorded without storing sensitive content.
* A job MUST reference a specific document version.

---

# 12. Index Synchronization

PostgreSQL remains the source of truth for document lifecycle and indexing state.

The search index is a derived representation.

Conceptually:

```text
PostgreSQL
    │
    │ source of truth
    ▼
Document Version
    │
    ▼
Indexing Event
    │
    ▼
OpenSearch
```

The system MUST be able to identify documents that are:

```text
DATABASE STATE ≠ SEARCH INDEX STATE
```

This allows reconciliation jobs to repair indexing inconsistencies.

---

# 13. Audit Event

AuditEvent records security- and lifecycle-relevant actions.

### Required attributes

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

Initial event types:

```text
DOCUMENT_CREATED
DOCUMENT_UPDATED
DOCUMENT_TOMBSTONED
DOCUMENT_RESTORED
DOCUMENT_INDEXED
DOCUMENT_INDEX_FAILED
ACL_CHANGED
```

Audit records SHOULD be append-only.

---

# 14. Transaction Requirements

Operations affecting PostgreSQL-owned state MUST use appropriate database transactions.

For example:

```text
Create Document Version
        │
        ├── create version
        ├── update document state
        └── create processing job
```

These changes SHOULD occur within a single transaction when they represent one logical database operation.

External systems such as S3 and OpenSearch cannot participate directly in the PostgreSQL transaction.

Therefore, asynchronous processing and reconciliation mechanisms MUST be used for cross-system consistency.

---

# 15. Repository Abstraction

The application MUST NOT directly depend on SQLAlchemy session logic.

Define repository interfaces at the application/domain boundary.

Examples:

```text
DocumentRepository
DocumentVersionRepository
TenantRepository
ProcessingJobRepository
AuditRepository
```

Conceptually:

```text
Application Layer
       │
       ▼
Repository Interface
       │
       ▼
PostgreSQL Repository
       │
       ▼
SQLAlchemy
       │
       ▼
PostgreSQL
```

This allows testing without requiring PostgreSQL and preserves infrastructure separation.

---

# 16. Identifier Strategy

Identifiers SHOULD use UUIDs.

Database-generated identifiers MUST NOT expose implementation-specific sequential IDs as public resource identifiers.

External source identifiers MUST remain separate from internal identifiers.

Example:

```text
Internal:
document_id = UUID

External:
external_id = "SHAREPOINT-12345"
```

---

# 17. Timestamp Strategy

All persisted timestamps SHOULD use UTC.

Required timestamp fields SHOULD use timezone-aware database types.

Application code MUST NOT depend on local server time.

---

# 18. Data Integrity

The database MUST enforce important invariants using:

* primary keys
* foreign keys
* unique constraints
* not-null constraints
* check constraints where appropriate

Application validation alone MUST NOT be relied upon for critical data integrity.

---

# 19. Multi-Tenant Isolation

Every tenant-owned entity MUST have a reliable tenant relationship.

Queries involving tenant-owned data MUST require tenant context.

Cross-tenant queries SHOULD be prohibited by default.

Future implementations MAY introduce PostgreSQL Row-Level Security where appropriate.

---

# 20. Failure Handling

The system MUST handle:

* database connection failure
* transaction failure
* duplicate document
* duplicate version
* invalid foreign key
* concurrent update
* processing job failure
* indexing failure

Failures MUST produce actionable structured errors.

---

# 21. Performance Considerations

The initial implementation MUST create indexes for common access patterns.

Expected indexes include:

```text
documents:
    tenant_id
    (tenant_id, external_id, source)
    status
    current_version_id

document_versions:
    document_id
    (document_id, version_number)
    content_hash

processing_jobs:
    document_version_id
    status

document_acl:
    document_id
    principal_id

audit_events:
    tenant_id
    resource_id
    created_at
```

Indexes SHOULD be validated against actual query patterns as the system evolves.

---

# 22. Security Requirements

The persistence layer MUST:

* use parameterized queries
* avoid storing plaintext secrets
* avoid logging sensitive document content
* protect database credentials
* use encrypted connections in cloud environments
* enforce least-privilege database access
* support auditability

---

# 23. Definition of Done

Spec 002 is complete when:

1. Domain entities are defined.
2. SQLAlchemy models are implemented.
3. Database migrations are implemented.
4. Repository interfaces are defined.
5. PostgreSQL repositories are implemented.
6. Unit tests exist.
7. Integration tests run against PostgreSQL.
8. Tenant isolation is tested.
9. Document versioning is tested.
10. Tombstone behavior is tested.
11. Transaction behavior is tested.
12. Failure scenarios are tested.
13. Documentation is updated.
14. CI validates database-related tests.

---

# 24. Future Extensions

The persistence architecture should allow future support for:

* document retention policies
* legal holds
* richer ACL models
* user/group synchronization
* ingestion source tracking
* document classification
* PII classification metadata
* data residency
* compliance policies
* encryption key references
* processing pipeline versions

These are intentionally outside the initial implementation scope.

---

## 25. Architectural Principle

PostgreSQL is the **system of record**.

Object storage contains the **source document**.

OpenSearch contains a **derived retrieval representation**.

Therefore:

```text
             SOURCE OF TRUTH
                    │
                    ▼
               PostgreSQL
                    │
           ┌────────┴────────┐
           ▼                 ▼
       Object Store      Search Index
           │                 │
       Raw content        Derived data
                             │
                      Can be rebuilt
```

The search index MUST be considered rebuildable from authoritative source data and metadata.
