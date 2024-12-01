from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Container, Horizontal
from runner.messages import AppEvents


class QuitScreen(ModalScreen):

    CSS_PATH = ["modal.tcss", "quit.tcss"]

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Quit the app?")
            with Horizontal():
                yield Button.error("No", id="no")
                yield Button.success("Yes", id="yes")

    @on(Button.Pressed)
    def exit_screen(self, event):
        button_id = event.button.id
        if button_id == "yes":
            self.post_message(AppEvents.Quit())
        self.dismiss()
