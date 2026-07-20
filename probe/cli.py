import typer

from probe.loader import load_modules

app = typer.Typer(help="System diagnostics tool")
plugins = load_modules()

for plugin in plugins.values():
    app.add_typer(plugin.get_app(), name=plugin.name)

    @app.command(name="all", help="System-wide metrics available under modules")
    def run_all():
        plugin.print_data()

if __name__ == "__main__":
    app()