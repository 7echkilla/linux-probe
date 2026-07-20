# Linux System Diagnostic Tool

A Python-based diagnostic tool that provides real-time system metrics and performance data - CPU, memory, system, process, and network metrics, with more planned. It is designed to be modular, allowing additional diagnostic plugins to be added easily.

The tool is built with **Typer** to provide a user-friendly CLI and it includes a **Textual**-based live dashboard for monitoring multiple system metrics simultaneously. Heavily inspired by Linux debugging workflows used in production systems.

### Features
- Modular design: Easily extendable with custom plugins
- CLI commands: View various system metrics through simple commands
- Live dashboard: Monitor multiple system metrics simultaneously in a real-time terminal UI

## Installation
1. Clone the repository: `git clone https://github.com/7echkilla/linux-probe.git`
2. Install the tool: `pip install -e .`

### Requirements
- Python3.10+
- `psutil` for system metrics
- `typer` for CLI
- `textual` for the live dashboard

## Usage
1. List all available modules: `probe --help`
2. Print all metrics once: `probe all`
3. Print a single module's metrics: `probe cpu`
4. Live dashboard: `probe monitor --interval 2` or `probe-monitor --interval 2`

Note: CPU and per-process CPU usage are computed from a delta between samples.
One-shot commands (`probe cpu`, `probe process`, `probe all`) only have a very
short window to sample from, so their CPU% readings are noisier than the
live dashboard, where each refresh tick has a full `--interval` seconds to
average over.

## Plugin System

The project is designed with modular plugins. You can easily add new plugins by creating new modules under the `probe/modules` directory. Each plugin should subclass `Module` and implement its `get_data()` method to return a dictionary of diagnostic data.

- `get_data()` must return raw, JSON-serialisable values only - numbers,
  strings, `None`, or a `list[dict]` for tabular data. Don't pre-format
  numeric metrics as strings (e.g. use `uptime_seconds: 120.5`, not
  `uptime: "2 minutes"`) - encode the unit in the key name instead, so
  values can be consumed directly by both the CLI and the TUI.
- Override the optional `warm_up()` hook if your module uses one of
  psutil's stateful percentage counters (like `cpu_percent`) - it's called
  once by the loader right after the module is instantiated, priming the
  counter so the first real `get_data()` call already has a delta to
  compute against.

The plugin will then be automatically discovered and available as a command under Typer.