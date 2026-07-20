import psutil

from probe.module import Module

class Memory(Module):
    def __init__(self):
        """
        Network stats (bytes sent/received, packets, errors)
        """
        self.name = "network"
        self.description = "Get network stats"

    def get_data(self):
        """
        Return dictionary with all network information
        """
        data = {}
        

        return data
    