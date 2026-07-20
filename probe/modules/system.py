import time
import psutil
import platform

from probe.module import Module

class System(Module):
    def __init__(self):
        """
        Information relevant to device
        """
        self.name = "system"
        self.description = "System information"

    def get_data(self):
        """
        Return dictionary with all system information
        """
        data = {}

        data.update(self._get_hostname())
        data.update(self._get_os())
        data.update(self._get_kernel())
        data.update(self._get_architecture())
        data.update(self._get_uptime())

        return data

    def _get_hostname(self):
        """
        Get device name
        """
        return {"hostname": platform.node()}

    def _get_os(self):
        """
        Get current OS
        """
        return {"os": platform.system()}

    def _get_kernel(self):
        """
        Get kernel version
        """
        return {"kernel": platform.release()}

    def _get_architecture(self):
        """
        Get device architecture
        """
        return {"architecture": platform.machine()}

    def _get_uptime(self):
        """
        Get system uptime as raw seconds
        """
        return {"uptime_seconds": round(time.time() - psutil.boot_time(), 2)}
