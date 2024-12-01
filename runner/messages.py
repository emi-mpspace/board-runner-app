from abc import ABC
from textual.message import Message
from runner.contexts import BoardContext


class AppEvents(ABC):
    class Quit(Message):
        def __init__(self, code: int = 0):
            self.code = code
            super().__init__()

    class ReadSerial(Message):
        def __init__(self, serial: str) -> None:
            self.serial = serial
            super().__init__()

    class BoardContextUpdate(Message):
        def __init__(self, context: BoardContext) -> None:
            self.context = context
            super().__init__()
