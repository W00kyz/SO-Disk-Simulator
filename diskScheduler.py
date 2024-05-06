import random
import matplotlib.pyplot as plt
from Schedulers import SSTF


class DiskSimulator:
    def __init__(
        self,
        sector_size,
        num_tracks,
        sectors_per_track,
        seek_time,
        rotation_rpm,
        transfer_time,
    ):
        self.sector_size = sector_size
        self.num_tracks = num_tracks
        self.sectors_per_track = sectors_per_track
        self.seek_time = seek_time
        self.rotation_rpm = rotation_rpm
        self.transfer_time = transfer_time
        self.scheduling_strategy = SSTF()
        self.head = None

    def set_scheduling(self, scheduling_strategy):
        self.scheduling_strategy = scheduling_strategy

    def set_head(self, value):
        self.head = value

    def calculate_latency(self, block_number, current_track):
        track, _ = divmod(block_number, self.sectors_per_track)
        if track >= self.num_tracks:
            raise ValueError("Invalid block number")

        seek_distance = abs(track - current_track)
        seek_latency = (self.seek_time + random.uniform(-0.5, 0.5)) * seek_distance

        rotation_latency = ((60000 / self.rotation_rpm) / 2) * random.uniform(0.9, 1.1)

        transfer_latency = self.transfer_time * random.uniform(0.9, 1.1)

        total_latency = seek_latency + rotation_latency + transfer_latency

        self.set_head(track)

        return total_latency

    def run_simulation(self, initial_track, requests):
        sortedRequests = self.scheduling_strategy.schedule(initial_track, requests)
        self.set_head(initial_track)

        total_latency = 0

        # Atender requests
        for request in sortedRequests:
            latency = self.calculate_latency(request, self.head)
            print(f"Bloco {request} - Head: {self.head} - Latência: {latency:.2f}")
            total_latency += latency

        return total_latency

    def plot_total_latency(self, initial_track, requests, strategies):
        total_latencies = []

        for strategy in strategies:
            self.set_scheduling(strategy)
            total_latency = self.run_simulation(initial_track, requests)
            print()
            total_latencies.append(total_latency)

        plt.figure(figsize=(10, 6))
        plt.bar(
            [str(strategy.__class__.__name__) for strategy in strategies],
            total_latencies,
        )
        plt.xlabel("Algoritmo de Simulação")
        plt.ylabel("Latência Total (milliseconds)")
        plt.title("Latência Total para Diferentes Algoritmos.")
        plt.savefig("disk_latency.png")


initial = 25

options = {
    "sector_size": 512,
    "num_tracks": 100,
    "sectors_per_track": 32,
    "seek_time": 3,
    "rotation_rpm": 7500,
    "transfer_time": 2,
}

requests = [45, 521, 30, 135, 0, 10, 89, 301, 205, 100]

disk = DiskSimulator(**options)
disk.plot_total_latency(initial, requests, [SSTF()])