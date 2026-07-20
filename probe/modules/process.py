import psutil

from probe.module import Module

class Process(Module):
    def __init__(self):
        """
        Information relevant to processes
        """
        self.name = "process"
        self.description = "Process information"

    def warm_up(self):
        """
        Prime every process's stateful CPU usage counter so the first real
        get_data() call has a delta to compute against.
        """
        for process in psutil.process_iter(["pid"]):
            try:
                process.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def get_data(self):
        """
        Return dictionary with all processes information
        """
        return self._get_top_processes()

    def _get_top_processes(self, limit=5):
        """
        Get top processes by CPU usage
        """
        processes = self._get_processes()
        processes.sort(key=lambda process: process["cpu_percent"], reverse=True)

        return {"top_by_cpu": processes[:limit]}

    def _get_processes(self):
        """
        Get processes list
        """
        processes = []

        for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            info = process.info

            if (info.get("memory_percent") is not None):
                info["memory_percent"] = round(info["memory_percent"], 2)

            processes.append(info)

        return processes
