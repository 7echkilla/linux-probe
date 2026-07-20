import typer

from abc import ABC, abstractmethod

class Module(ABC):
    def __init__(self):
        """
        Define the base class structure for modules
        """
        self.name = "unknown"
        self.description = "no description"

    @abstractmethod
    def get_data(self):
        """
        Return a flat dict of diagnostic data. Values must be raw and
        JSON-serialisable: int/float/str/None, or a list[dict] for tabular
        data (e.g. per-process rows). Numeric metrics must not be
        pre-formatted as strings - encode the unit in the key name instead
        (e.g. "used_gb", "uptime_seconds", "load_avg_1m").
        """
        pass

    def warm_up(self):
        """
        Optional one-time hook called by the loader immediately after
        instantiation. Override in modules that rely on psutil's stateful
        percentage counters (cpu_percent) to make an initial call so the
        first real get_data() call already has a delta to compute against.
        """
        pass

    def get_app(self):
        """
        Generate app command for Typer extension
        """
        app = typer.Typer(help=self.description)

        # Default behaviour when no subcommand is provided
        @app.callback(invoke_without_command=True)
        def main(context: typer.Context):
            if (context.invoked_subcommand is None):
                self.print_data()

        # Explicit subcommand
        @app.command(name="get-data")
        def get_data():
            self.print_data()

        return app

    def print_data(self):
        data = self.get_data()
        parts = []

        for metric, value in data.items():
            if (isinstance(value, list)):
                parts.append(f"{metric}: {len(value)} item(s)")
            else:
                parts.append(f"{metric}: {value}")

        print(f"{self.name:10} " + " | ".join(parts))
