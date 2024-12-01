from textual import on
from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DirectoryTree, Footer, Header, Label, RichLog
from textual.reactive import reactive
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Iterable


class DirectoryOnlyTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [
            path
            for path in paths
            if path.is_dir()
            and not path.name.startswith(".")
            and not path.name.startswith("__")
        ]


class SelectDirectoryScreen(ModalScreen[None]):

    CSS_PATH = "modal.tcss"

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Select test directory!")
            yield DirectoryOnlyTree("./", id="directory_tree")

    @on(DirectoryTree.DirectorySelected, "#directory_tree")
    def select_directory(self, event) -> None:
        self.dismiss(event.path)


class TestRunnerScreen(Screen):

    CSS_PATH = ["tests.tcss"]

    BINDINGS = [("escape", "app.pop_screen", "Back"), ("c", "clear_log", "Clear Log")]

    selected_directory = reactive(None, recompose=True)

    def on_mount(self) -> None:
        self.sub_title = "Test Runner"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container():
            with Horizontal():
                yield Button("Select directory", id="select_directory")
                yield Button.success("Run", id="run")
            yield Label(f"Test Directory: {self.selected_directory or ''}")
            with VerticalScroll():
                yield RichLog()

    def action_clear_log(self):
        log = self.query_one(RichLog)
        log.clear()

    @on(Button.Pressed, "#select_directory")
    def select_press(self, event) -> None:
        self.app.push_screen(SelectDirectoryScreen(), self.directory_selected)

    @on(Button.Pressed, "#run")
    def run_pressed(self, event) -> None:
        log = self.query_one(RichLog)
        if self.selected_directory is not None:
            with Popen(
                ["pytest", self.selected_directory],
                stdout=PIPE,
                stderr=PIPE,
                bufsize=1,
                universal_newlines=True,
            ) as p:
                for line in p.stdout:
                    log.write(line)
        else:
            log.write("No directory selected!")

    def directory_selected(self, path) -> None:
        self.selected_directory = path
