import os
import psutil

from probe.module import Module

class CPU(Module):
    def __init__(self):
        """
        Metrics relevant to CPU
        """
        self.name = "cpu"
        self.description = "CPU metrics"

    def warm_up(self):
        """
        Prime psutil's stateful CPU usage counter so the first real
        get_data() call has a delta to compute against.
        """
        psutil.cpu_percent(interval=None)

    def get_data(self):
        """
        Return dictionary with all CPU metrics
        """
        data = {}

        data.update(self._get_usage())
        data.update(self._get_physical_cores())
        data.update(self._get_logical_cores())
        data.update(self._get_load_average())
        data.update(self._get_temperature())

        return data

    def _get_usage(self):
        """
        Get current CPU usage percentage
        """
        return {"usage_percent": psutil.cpu_percent(interval=None)}

    def _get_physical_cores(self):
        """
        Get number of physical CPU cores
        """
        return {"physical_cores": psutil.cpu_count(logical=False)}

    def _get_logical_cores(self):
        """
        Get number of logical CPU cores
        """
        return {"logical_cores": psutil.cpu_count(logical=True)}

    def _get_load_average(self):
        """
        Get load average as raw numeric values
        """
        one, five, fifteen = os.getloadavg()

        return {
            "load_avg_1m": round(one, 2),
            "load_avg_5m": round(five, 2),
            "load_avg_15m": round(fifteen, 2),
        }

    def _get_temperature(self):
        """
        Get CPU temperature (if supported)
        """
        try:
            temperatures = psutil.sensors_temperatures()
            core_temperatures = temperatures.get("coretemp", [])
            value = core_temperatures[0].current if core_temperatures else None
        except AttributeError:
            value = None

        return {"temperature_c": value}
