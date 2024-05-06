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
