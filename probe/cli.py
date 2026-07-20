import typer

from probe.loader import load_modules
from probe.logging_config import setup_logging

setup_logging()

app = typer.Typer(help="System diagnostics tool")
plugins = load_modules()

for plugin in plugins.values():
    app.add_typer(plugin.get_app(), name=plugin.name)

@app.command(name="all", help="Print metrics for every discovered module")
def run_all():
    for plugin in plugins.values():
        plugin.print_data()

@app.command(name="monitor", help="Launch the live dashboard")
def monitor(
    interval: float = typer.Option(2.0, "--interval", "-i", help="Refresh interval in seconds"),
):
    from probe.tui import ProbeApp
    ProbeApp(plugins=plugins, interval=interval).run()

if __name__ == "__main__":
    app()
