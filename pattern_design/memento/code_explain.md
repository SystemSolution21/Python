# Codebase Explain

This Python script implements the **Memento Design Pattern** to add fully functional **Undo and Redo** capabilities to a workflow application.
Here is a step-by-step breakdown of how every class and function works together.

## 1. Data Models: `Task` and `WorkflowSnapshot`

These classes define the core building blocks of what gets saved.  

- **`Task` (Frozen Dataclass):**

    ```python
    @dataclass(frozen=True)
    class Task:
        name: str
        enabled: bool = True
    ```

  - Represents an individual task in a workflow (e.g., `"validate_invoice"`).
  - Marked as `frozen=True` (immutable) so that once a task is created, its values cannot be accidentally mutated in place.

- **`WorkflowSnapshot` (The Memento):**

    ```python
    @dataclass(frozen=True)
    class WorkflowSnapshot:
        name: str
        tasks: tuple[Task, ...]
    ```

  - This is the actual **Memento object**. It captures a specific state of the workflow at a point in time.
  - Notice the state boundary: it only stores structural properties (`name` and `tasks`) and leaves out runtime data like execution counters. It uses a `tuple` for tasks to guarantee immutability.

## 2. Interface Protocol: `Snapshotable`

```python
class Snapshotable[T](Protocol):
    def snapshot(self) -> T: ...
    def restore(self, snapshot: T) -> None: ...
```

- Uses Python's `Protocol` (structural subtyping / interfaces) to define a contract.
- Any class that wants to support undo/redo must implement two methods: `snapshot()` (to export its current state) and `restore()` (to load a past state back in). This decouples the `History` manager from the specific details of the `Workflow` class.

## 3. State Manager: `History`

```python
class History[T]:
    def __init__(self) -> None:
        self._undo: list[T] = []
        self._redo: list[T] = []
```

- Acts as the caretaker. It manages two stacks (`_undo` and `_redo`) containing snapshots.
- **`save(obj)`:**

    ```python
    def save(self, obj: Snapshotable[T]) -> None:
        self._undo.append(obj.snapshot())
        self._redo.clear()
    ```

  - Takes a snapshot of the current object and pushes it onto the `_undo` stack.
  - Clears the `_redo` stack because performing a new action invalidates any forward-redo history.

- **`undo(obj)`:**

    ```python
    def undo(self, obj: Snapshotable[T]) -> bool:
        if not self._undo: return False
        self._redo.append(obj.snapshot())
        obj.restore(self._undo.pop())
        return True
    ```

  - If the undo stack is empty, it returns `False`.
  - Otherwise, it pushes the _current_ state onto the `_redo` stack (so you can get it back), pops the most recent past snapshot from `_undo`, and feeds it to `obj.restore()`.

- **`redo(obj)`:**
  - Operates symmetrically to `undo`: it pops from `_redo`, pushes the current state to `_undo`, and restores the forward state.

## 4. Originator: `Workflow`

This is the main application class whose state changes over time.

- **`__init__`:** Initializes structural state (`_name`, `_tasks`) and **runtime state** (`last_run_at`, `execution_count`).
- **Mutator Methods (`rename`, `add_task`, `move_task`):** Modify the structural properties of the workflow.
- **`run()`:** Simulates executing the workflow, modifying runtime metrics (`execution_count += 1`).
- **`snapshot()` & `restore()`:** Fulfills the `Snapshotable` protocol.  
  - `snapshot()` returns a `WorkflowSnapshot` containing only the workflow's name and its tasks.
  - `restore()` unpacks a snapshot back into the workflow's active attributes.

## 5. Execution Flow: `main()`

The `main` function puts the pattern into action:

1. **Initial Setup:** Creates a `workflow` with two tasks and initializes a `History` manager.
2. **Execution & Saving:**

    ```python
    workflow.run(datetime(2026, 9, 10, 9, 0))
    history.save(workflow)
    ```

    The workflow runs (increasing `execution_count` to 1), and a snapshot of its initial state is saved to history.
3. **Mutations:** The workflow is modified (renamed, a task is added, a task is moved).
4. **Undoing:**

    ```python
    assert history.undo(workflow)
    ```

    Reverts the structural changes back to what they were right before the mutations.
    - **Crucial Takeaway:** `assert workflow.execution_count == 1` proves that **runtime state (`execution_count`) was untouched** by the undo operation, illustrating a clean state boundary (only user-editable design state is rolled back, not background telemetry or execution history).

5. **Redoing:** `history.redo(workflow)` pushes the workflow back forward to the modified state.
