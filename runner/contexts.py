from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class BoardContext:
    serial: str = None
    batch_number: str = None
    revision: str = None


@dataclass(frozen=True)
class RemoteContext:
    url: str = None


@dataclass(frozen=True)
class ExecutionContext:
    task: str
    result: Any


@dataclass(frozen=True)
class ApplicationContext:
    board_context: BoardContext = None
    remote_context: RemoteContext = None
    execution_contexts: list[ExecutionContext] = field(default_factory=list)
