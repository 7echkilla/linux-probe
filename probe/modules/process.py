import psutil

from probe.module import Module

class Process(Module):
    def __init__(self):
        """
        Information relevant to processes
        """
        self.name = "process"
        self.description = "Processes information"

    def get_data(self):
        """
        Return dictionary with all processes information
        """
        data = {}
        
        data.update(self._get_top_processes())

        return data

    def _get_top_processes(self):
        """
        Get top 5 processes by CPU and memory usage
        """
        processes = self._get_processes()

        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = processes[:5]

        return {"Top processes by CPU usage": top_processes}

    def _get_processes(self):
        """
        Get processes list
        """
        processes = []
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append(process.info)

        return processes