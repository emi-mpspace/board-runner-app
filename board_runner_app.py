from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Label
from textual.reactive import reactive
from runner.contexts import ApplicationContext, BoardContext
from runner.messages import AppEvents
from screens import QuitScreen, BoardSerialScreen, BoardInfoScreen, TestRunnerScreen
from dataclasses import replace


class BoardRunnerApp(App[None]):

    BINDINGS = [
        ("i", "board_info", "Board Info"),
        ("q", "quit", "Quit"),
    ]

    CSS_PATH = "app.tcss"

    board_context_state = reactive(None, recompose=True)

    def __init__(self):
        self.app_context = ApplicationContext()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="commands"):
            with Horizontal():
                yield Button("Read serial", id="read_serial_btn")
                yield Button("Run tests", id="test_runner_btn")
                yield Button("Flash FW")
            yield Label("Board Info:", classes="title")

            with VerticalScroll():
                if self.board_context_state:
                    yield Label(f"Serial: {self.board_context_state.serial}")
                    yield Label(f"Revision: {self.board_context_state.revision or ''}")
                    yield Label(
                        f"Batch Number: {self.board_context_state.batch_number or ''}"
                    )
                else:
                    yield Label("No board information, click on Read Serial to get started!")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Board Runner App"

    def action_board_info(self) -> None:
        if self.app_context.board_context:
            self.push_screen(BoardInfoScreen(self.app_context.board_context))
        else:
            self.push_screen(BoardSerialScreen())

    def action_quit(self) -> None:
        self.push_screen(QuitScreen())

    @on(Button.Pressed, "#read_serial_btn")
    def on_read_serial(self) -> None:
        self.push_screen(BoardSerialScreen())

    @on(Button.Pressed, "#test_runner_btn")
    def on_test_runner(self) -> None:
        self.push_screen(TestRunnerScreen())

    # App Events
    @on(AppEvents.Quit)
    def on_quit(self, event) -> None:
        self.exit(event.code or 0)

    @on(AppEvents.ReadSerial)
    def on_serial(self, event) -> None:
        if self.app_context.board_context:
            self.update_board_context(
                replace(self.app_context.board_context, serial=event.serial)
            )
        else:
            self.update_board_context(BoardContext(serial=event.serial))

    @on(AppEvents.BoardContextUpdate)
    def on_board_context_update(self, event) -> None:
        self.update_board_context(event.context)

    def update_board_context(self, context) -> None:
        self.board_context_state = context
        self.app_context = replace(self.app_context, board_context=context)
