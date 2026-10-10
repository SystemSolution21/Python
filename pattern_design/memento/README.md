# Memento

In a standalone memento, state is held purely in RAM, managed synchronously, and manipulated within a single process.

In a **real-world Python production backend** (such as a FastAPI or Django app connecting to relational databases, caches, and microservices), the classic "Gang of Four" Memento pattern undergoes architectural shifts. Because production systems are **stateless, distributed, and multi-tenant**, storing a history stack in-memory will not scale.

## How the Memento Pattern Evolves in Production

### 1. Persistence Layer: Storing Snapshots in Databases

Instead of a Python `list` (`self._undo`, `self._redo`), mementos are serialized and written to a database.

- **Relational DB (PostgreSQL):** You often store snapshots as JSON columns (`JSONB`) in a dedicated audit or history table (e.g., `workflow_revisions`). Every time a state change occurs, a new row is inserted with a foreign key to the entity and a version or timestamp.

- **NoSQL / Document Store (MongoDB, DynamoDB):** Ideal for hierarchical snapshots (like workflow tasks), where the entire JSON document can be versioned and pushed onto an array or a version-controlled document collection.

### 2. Stateless APIs and Distributed Microservices

In a microservices architecture, the application server does not hold the workflow object in memory across requests. When a user clicks "Undo" in a web UI:

1. The frontend calls an API endpoint: `POST /workflows/{id}/undo`.
2. The backend service fetches the workflow's state history from a database or event store.
3. It pops the previous snapshot, applies it to the active record, saves the changes, and pushes the current state to the redo stack.

### Alternative Production Approaches to the Memento Pattern

Depending on your exact requirements, production backends usually lean toward more robust architectural patterns rather than a manual Memento implementation:

#### A. Event Sourcing & CQRS (The Industrial-Strength Memento)

Instead of storing state _snapshots_, **Event Sourcing** stores a log of _every immutable event_ that occurred (e.g., `WorkflowCreated`, `StepAdded`, `WorkflowRenamed`).

- **How it works:** To get the current state, you replay the event log. To "undo," you simply stop replaying at $N-1$ events or append a compensating event (like a reversal event).

- **When to use:** Complex business domains, strict financial auditing requirements, or systems requiring comprehensive time-travel debugging.

#### B. Optimistic Concurrency Control (OCC) & Versioning

If your goal is preventing race conditions when multiple users edit the same workflow concurrently:

- **How it works:** The database record includes a `version` integer. When saving, the backend executes an update query: `UPDATE workflows SET name = :name, version = version + 1 WHERE id = :id AND version = :current_version`. If 0 rows are updated, someone else modified it first, and the transaction rolls back.

#### C. Built-in ORM State Tracking (SQLAlchemy / Django ORM)

If you just want to track changes and roll back transactions _within a single request lifecycle_:  

- **Python Frameworks:** ORMs like SQLAlchemy and Django manage internal "units of work." They keep track of dirty attributes automatically. If an error occurs midway through a transaction, you call `db.session.rollback()` (the database's native memento equivalent) to revert the entire transaction instantly.

### Summary Checklist: When to Use What

| **Requirement**                                                      | **Best Approach**                                          |
| -------------------------------------------------------------------- | ---------------------------------------------------------- |
| **In-memory UI state (e.g., Desktop app, local wizard)**             | Classic Memento Pattern (like the Codes script)            |
| **User profile/document "Revision History" (Undo/Redo in web apps)** | Database-backed Mementos (`JSONB` snapshots in PostgreSQL) |
| **Financial ledgers, audit logs, complex workflows**                 | Event Sourcing & Append-Only Event Logs                    |
| **Preventing overwrite conflicts in multi-user apps**                | Optimistic Concurrency Control (`version` column)          |
