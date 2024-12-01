from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Input
from textual.containers import Container, Horizontal
from runner.messages import AppEvents
from runner.contexts import BoardContext
from dataclasses import replace


class BoardSerialScreen(ModalScreen):

    CSS_PATH = "modal.tcss"

    def compose(self) -> ComposeResult:
        with Container(id="serial_container"):
            yield Label("Enter Serial Number:")
            yield Input(id="serial")
            with Horizontal():
                yield Button.error("Cancel")
                yield Button.success("OK")

    @on(Button.Pressed)
    @on(Input.Submitted)
    def submit(self) -> None:
        input = self.query_one(Input)
        if input.value:
            self.post_message(AppEvents.ReadSerial(input.value))
        self.dismiss()


class BoardInfoScreen(ModalScreen):

    CSS_PATH = ["modal.tcss", "form.tcss"]

    def __init__(self, context: BoardContext):
        self.ctx = context
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Serial Number:")
            yield Input(id="serial", value=self.ctx.serial or "")

            yield Label("Revision:")
            yield Input(id="revision", value=self.ctx.revision or "")

            yield Label("Batch Number:")
            yield Input(id="batch", value=self.ctx.batch_number or "")

            with Horizontal():
                yield Button.error("Cancel")
                yield Button.success("Save", id="save")

    @on(Button.Pressed)
    def submit(self, event) -> None:
        button_id = event.button.id
        if button_id == "save":
            context = replace(
                self.ctx,
                serial=self.query_one("#serial").value,
                revision=self.query_one("#revision").value,
                batch_number=self.query_one("#batch").value,
            )
            self.post_message(AppEvents.BoardContextUpdate(context=context))
        self.dismiss()
