import psutil

from probe.module import Module

class Network(Module):
    def __init__(self):
        """
        Network stats (bytes sent/received, packets, errors)
        """
        self.name = "network"
        self.description = "Network stats"

    def get_data(self):
        """
        Return dictionary with all network information
        """
        data = {}

        data.update(self._get_io_counters())
        data.update(self._get_interfaces())

        return data

    def _get_io_counters(self):
        """
        Get cumulative network I/O counters
        """
        counters = psutil.net_io_counters()

        return {
            "bytes_sent": counters.bytes_sent,
            "bytes_recv": counters.bytes_recv,
            "packets_sent": counters.packets_sent,
            "packets_recv": counters.packets_recv,
            "errin": counters.errin,
            "errout": counters.errout,
            "dropin": counters.dropin,
            "dropout": counters.dropout,
        }

    def _get_interfaces(self):
        """
        Get list of network interface names
        """
        return {"interfaces": list(psutil.net_if_addrs().keys())}
