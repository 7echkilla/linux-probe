import psutil

from probe.module import Module

class CPU(Module):
    def __init__(self):
        """
        Metrics relevant to CPU
        """
        self.name = "cpu"
        self.description = "CPU metrics"

    def get_data(self):
        """
        Return dictionary with all CPU metrics
        """
        data = {}
        
        data.update(self._get_cpu_usage())
        data.update(self._get_cpu_cores())

        return data
    
    def _get_cpu_usage(self):
        """
        Get current CPU usage percentage
        """
        cpu_usage = psutil.cpu_percent()
        
        return {"CPU Usage (%)": cpu_usage}
    
    def _get_cpu_cores(self):
        """
        Get number of CPU cores
        """
        cpu_count = psutil.cpu_count(logical=False)

        return {"CPU Cores": cpu_count}