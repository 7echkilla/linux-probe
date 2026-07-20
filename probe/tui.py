import logging

import typer
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Header, Footer, Static, DataTable

from probe.loader import load_modules
from probe.logging_config import setup_logging

logger = logging.getLogger(__name__)

class ModulePanel(Vertical):
    def __init__(self, plugin):
        super().__init__(id=f"panel-{plugin.name}")
        self.plugin = plugin

    def compose(self) -> ComposeResult:
        yield Static(self.plugin.description, classes="panel-title")
        yield DataTable(id=f"table-{self.plugin.name}")

    def on_mount(self):
        table = self.query_one(DataTable)

        if (self.plugin.name == "process"):
            table.add_columns("PID", "Name", "CPU %", "Mem %")
        else:
            table.add_columns("Metric", "Value")

        self.refresh_data()

    def refresh_data(self):
        data = self.plugin.get_data()
        table = self.query_one(DataTable)
        table.clear()

        if (self.plugin.name == "process"):
            for row in data.get("top_by_cpu", []):
                table.add_row(
                    str(row.get("pid")),
                    str(row.get("name")),
                    f"{row.get('cpu_percent', 0):.1f}",
                    f"{row.get('memory_percent', 0):.1f}",
                )
        else:
            for metric, value in data.items():
                if (isinstance(value, list)):
                    value = f"{len(value)} item(s)"

                table.add_row(metric, "N/A" if value is None else str(value))


class ProbeApp(App):
    CSS = """
    Grid {
        grid-size: 2;
        grid-gutter: 1;
    }

    ModulePanel {
        border: round $accent;
        padding: 0 1;
    }

    .panel-title {
        text-style: bold;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]
    TITLE = "linux-probe"
    SUB_TITLE = "first tick may read low for CPU/process metrics"

    def __init__(self, plugins, interval=2.0):
        super().__init__()
        self.plugins = plugins
        self.interval = interval

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Grid():
            for plugin in self.plugins.values():
                yield ModulePanel(plugin)

        yield Footer()

    def on_mount(self):
        self.set_interval(self.interval, self.refresh_all)

    def refresh_all(self):
        for panel in self.query(ModulePanel):
            try:
                panel.refresh_data()
            except Exception:
                logger.exception("Failed to refresh panel for module %s", panel.plugin.name)


def main(interval: float = 2.0):
    """
    Launch the live dashboard
    """
    setup_logging()
    plugins = load_modules()
    ProbeApp(plugins=plugins, interval=interval).run()


def _cli_entry():
    typer.run(main)

if __name__ == "__main__":
    _cli_entry()
