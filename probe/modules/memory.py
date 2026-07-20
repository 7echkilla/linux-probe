import psutil

from probe.module import Module

class Memory(Module):
    def __init__(self):
        """
        Initialise memory class
        """
        self.name = "memory"
        self.description = "memory metrics"

    def get_data(self):
        mem = psutil.virtual_memory()

        return {
            "percent": mem.percent,
            "used_gb": round(mem.used / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "total_gb": round(mem.total / (1024**3), 2)
        }