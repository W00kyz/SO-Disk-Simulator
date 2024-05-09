import random
import statistics
from httpx import head
import matplotlib.pyplot as plt


class DiskSimulator:
    def __init__(
        self,
        sector_size: int,
        num_tracks: int,
        sectors_per_track: int,
        seek_time: int,
        rotation_rpm: int,
        transfer_time: int,
    ):
        self.sector_size = sector_size
        self.num_tracks = num_tracks
        self.sectors_per_track = sectors_per_track
        self.seek_time = seek_time
        self.rotation_rpm = rotation_rpm
        self.transfer_time = transfer_time
        self.head = 0

    def set_head(self, value):
        self.head = value

    def calculate_latency(self, block_number):
        track, _ = divmod(block_number, self.sectors_per_track)
        if track >= self.num_tracks:
            raise ValueError("Invalid block number")

        seek_distance = abs(track - self.head)
        seek_latency = (self.seek_time + random.uniform(-0.5, 0.5)) * seek_distance

        rotation_latency = ((60000 / self.rotation_rpm) / 2) * random.uniform(0.9, 1.1)

        transfer_latency = self.transfer_time * random.uniform(0.9, 1.1)

        total_latency = seek_latency + rotation_latency + transfer_latency

        self.set_head(track)

        return total_latency

    def sstf(self, requests):
        sequence = list(requests)
        total_latency = 0
        total_seek_op = 0
        for i in range(len(sequence)):
            for j in range(len(sequence) - i - 1):
                if abs(sequence[j] - self.head) > abs(sequence[j + 1] - self.head):
                    sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]
            self.head = sequence[i] // self.sectors_per_track

        # atende as requisições.
        for block in sequence:
            latency = self.calculate_latency(block)
            total_latency += latency

        # resetar cabeça.
        self.head = 0

        return total_latency

    def scan(self, requests):
        sequence = list(requests)
        sequence.sort()
        total_latency = 0
        current_track = self.head // self.sectors_per_track
        direction = 1  # 1 for upward scan, -1 for downward scan

        while sequence:
            next_block = None
            for block in sequence:
                block_track = block // self.sectors_per_track
                if (block_track >= current_track and direction == 1) or (
                    block_track <= current_track and direction == -1
                ):
                    next_block = block
                    break

            if next_block is None:  # No more blocks in the current direction
                direction *= -1  # Change direction
                continue

            sequence.remove(next_block)  # Remove the block from the sequence
            latency = self.calculate_latency(next_block)
            total_latency += latency
            current_track = next_block // self.sectors_per_track

        # Resetar cabeça.
        self.head = 0

        return total_latency

    def __str__(self):
        attributes = [
            f"Sector Size: {self.sector_size}",
            f"Number of Tracks: {self.num_tracks}",
            f"Sectors per Track: {self.sectors_per_track}",
            f"Seek Time: {self.seek_time}",
            f"Rotation RPM: {self.rotation_rpm}",
            f"Transfer Time: {self.transfer_time}",
            f"Current Head Position: {self.head}",
        ]
        return "\n".join(attributes)
