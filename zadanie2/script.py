from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

class LineViewer(App):
    CSS_PATH = None
    current_line = reactive(0)

    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        with open(filename, 'r') as f:
            self.lines = [line.rstrip('\n') for line in f]

    def compose(self) -> ComposeResult:
        line_text = self.lines[0] if self.lines else "Brak danych."
        display = f"{self.current_line+1}: {line_text}"
        yield Static(display, id="line")

    async def on_key(self, event):
        if event.key == "space":
            if self.current_line < len(self.lines) - 1:
                self.current_line += 1
                display = f"{self.current_line+1}: {self.lines[self.current_line]}"
                self.query_one("#line", Static).update(display)
        elif event.key == "b":
            if self.current_line > 0:
                self.current_line -= 1
                display = f"{self.current_line+1}: {self.lines[self.current_line]}"
                self.query_one("#line", Static).update(display)

if __name__ == "__main__":
    import sys
    filename = "output.txt" if len(sys.argv) < 2 else sys.argv[1]
    LineViewer(filename).run()
