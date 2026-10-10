from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Task:
    """Represents a task in a workflow."""

    name: str
    enabled: bool = True


@dataclass(frozen=True)
class WorkflowSnapshot:
    """This is Memento object. It captures a specific state of the workflow at a point in time."""

    name: str
    tasks: tuple[Task, ...]


class SnapshotTable[T](Protocol):
    """Represents a table of workflow snapshots."""

    def snapshot(self) -> T:
        """Returns the snapshot."""
        ...

    def restore(self, snapshot: T) -> None:
        """Restores the workflow to the given snapshot."""
        ...


class History[T]:
    """Maintains a history of mementos workflow snapshots."""

    def __init__(self) -> None:
        self._undo: list[T] = []
        self._redo: list[T] = []

    def save(self, obj: SnapshotTable[T]) -> None:
        """Saves a snapshot to the history."""
        self._undo.append(obj.snapshot())
        self._redo.clear()

    def undo(self, obj: SnapshotTable[T]) -> bool:
        """Undoes the last action."""
        if not self._undo:
            return False

        self._redo.append(obj.snapshot())
        obj.restore(self._undo.pop())
        return True

    def redo(self, obj: SnapshotTable[T]) -> bool:
        """Redoes the last undone action."""
        if not self._redo:
            return False

        self._undo.append(obj.snapshot())
        obj.restore(self._redo.pop())
        return True


class Workflow:
    """Represents a workflow with tasks and supports snapshotting."""

    def __init__(self, name: str, tasks: list[Task]) -> None:
        self._name: str = name
        self._tasks: list[Task] = tasks
        self.last_run_at: datetime | None = None
        self.execution_count: int = 0

    def rename(self, new_name: str) -> None:
        """Renames the workflow."""
        self._name = new_name

    def add_task(self, task: Task) -> None:
        """Adds a task to the workflow."""
        self._tasks.append(task)

    def move_task(self, task_name: str, position: int) -> None:
        """Moves a task to a new index in the workflow."""
        task_index: int = next(
            i for i, task in enumerate(self._tasks) if task.name == task_name
        )
        task: Task = self._tasks.pop(task_index)
        self._tasks.insert(position, task)

    def run(self, now: datetime) -> None:
        """Runs the workflow."""
        self.last_run_at = now
        self.execution_count += 1

    def snapshot(self) -> WorkflowSnapshot:
        """Creates a snapshot of the workflow."""
        return WorkflowSnapshot(name=self._name, tasks=tuple(self._tasks))

    def restore(self, snapshot: WorkflowSnapshot) -> None:
        """Restores the workflow to a given snapshot."""
        self._name = snapshot.name
        self._tasks = list(snapshot.tasks)

    def describe(self) -> str:
        """Returns a description of the workflow."""
        tasks: str = ", ".join([task.name for task in self._tasks])
        return f"{self._name}: [{tasks}], executions: {self.execution_count}"


def main() -> None:
    """Demonstrates the Memento pattern with a workflow example."""

    # Create a workflow.
    workflow = Workflow(
        name="Invoice processing",
        tasks=[Task(name="validate_invoice"), Task(name="charge_card")],
    )

    # Create a history object to manage snapshots.
    history: History[WorkflowSnapshot] = History()

    # Run the workflow and save its initial state.
    workflow.run(now=datetime.now())
    history.save(obj=workflow)
    print(f"Initial: {workflow.describe()}")

    # Edit the workflow.
    workflow.rename(new_name="Process customer invoice")
    workflow.add_task(task=Task(name="send_confirmation"))
    workflow.move_task(task_name="charge_card", position=2)
    print(f"Edited: {workflow.describe()}")

    # Undo the changes.
    assert history.undo(workflow)
    print(f"Undone: {workflow.describe()}")
    assert workflow.execution_count == 1  # Runtime state is not part of the memento.

    # Redo the changes.
    assert history.redo(workflow)
    print(f"Redone: {workflow.describe()}")


if __name__ == "__main__":
    main()
