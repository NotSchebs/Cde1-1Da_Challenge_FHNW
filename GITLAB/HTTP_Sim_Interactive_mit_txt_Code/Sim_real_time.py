
import time

class RealTimeDataSimulator:
    def __init__(self, data, delay=0.05):
        """
        Simulate real-time data streaming.
        :param data: Full list of route data to simulate incoming data.
        :param delay: Delay between each data chunk (in seconds).
        """
        self.data = data
        self.delay = delay

    def datastream(self):
        """Generator that simulates data being sent in chunks."""
        for i in range(1, len(self.data) + 1):
            yield self.data[:i]  # Yield a subset of the data
            time.sleep(self.delay)  # Simulate delay for real-time effect