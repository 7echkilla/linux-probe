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
        hostname = platform.node()

        return {"Device Name": hostname}
    
    def _get_os(self):
        """
        Get current OS
        """
        os = platform.system()

        return {"OS": os}
    
    def _get_kernel(self):
        """
        Get kernel version
        """
        kernel = platform.release()

        return {"Kernel": kernel}
    
    def _get_architecture(self):
        """
        Get device architecture
        """
        architecture = platform.machine()

        return {"Architecture": architecture}
    
    def _get_uptime(self):
        """
        Get system uptime
        """
        boot_time = psutil.boot_time()
        elapsed_time = time.time() - boot_time

        # Calculate hours, minutes and seconds
        uptime_hours = int(elapsed_time // 3600)
        uptime_minutes = int((elapsed_time % 3600) // 60)
        uptime_seconds = int(elapsed_time % 60)

        string = f"{uptime_hours} hours {uptime_minutes} minutes {uptime_seconds} seconds"

        return {"Uptime": string}