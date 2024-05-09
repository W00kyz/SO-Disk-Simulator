import random
import statistics
import matplotlib.pyplot as plt


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

        return total_latency, seek_distance

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
            latency, seek_distance = self.calculate_latency(block)
            total_latency += latency
            total_seek_op += seek_distance

        # resetar cabeça.
        self.head = 0

        return total_latency, total_seek_op

    def scan(self, requests):
        sequence = list(requests)
        sequence.sort()
        total_latency = 0
        total_seek_op = 0
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
            latency, seek_distance = self.calculate_latency(next_block)
            total_latency += latency
            total_seek_op += seek_distance
            current_track = next_block // self.sectors_per_track

        # Resetar cabeça.
        self.head = 0

        return total_latency, total_seek_op

    def calculate_statistics(self, requests_list):
        latencies = []
        total_seek_ops = []
        for requests in requests_list:
            total_latency, total_seek_op = self.sstf(requests)
            latencies.append(total_latency)
            total_seek_ops.append(total_seek_op)
        mean_latency = statistics.mean(latencies)
        median_latency = statistics.median(latencies)
        mode_latency = statistics.mode(latencies)
        mean_seek_op = statistics.mean(total_seek_ops)
        mode_seek_op = statistics.mode(total_seek_ops)
        median_seek_op = statistics.median(total_seek_ops)
        return (
            mean_latency,
            median_latency,
            mode_latency,
            mean_seek_op,
            mode_seek_op,
            median_seek_op,
        )

    def plot_statistics(self, sizes, requests_list):
        mean_latencies = []
        median_latencies = []
        mode_latencies = []
        mean_seek_ops = []
        mode_seek_ops = []
        median_seek_ops = []
        for _ in requests_list:
            (
                mean_latency,
                median_latency,
                mode_latency,
                mean_seek_op,
                mode_seek_op,
                median_seek_op,
            ) = self.calculate_statistics(requests_list)
            mean_latencies.append(mean_latency)
            median_latencies.append(median_latency)
            mode_latencies.append(mode_latency)
            mean_seek_ops.append(mean_seek_op)
            mode_seek_ops.append(mode_seek_op)
            median_seek_ops.append(median_seek_op)

        # Gráfico para estatísticas de latência
        plt.plot(sizes, mean_latencies, label="Média de Latência")
        plt.plot(sizes, median_latencies, label="Mediana de Latência")
        plt.plot(sizes, mode_latencies, label="Moda de Latência")
        plt.xlabel("Tamanho da Lista de Requisição")
        plt.ylabel("Latência em milissegundos")
        plt.title("Latência para diferentes tamanhos de sequências")
        plt.legend()
        plt.savefig("imgs/latency_statistics.png")
        plt.close()

        # Gráfico para estatísticas de operações de busca
        plt.plot(sizes, mean_seek_ops, label="Média de Operações de Busca")
        plt.plot(sizes, mode_seek_ops, label="Moda de Operações de Busca")
        plt.plot(sizes, median_seek_ops, label="Mediana de Operações de Busca")
        plt.xlabel("Tamanho da Lista de Requisição")
        plt.ylabel("Operação de Busca")
        plt.title("Operações de Busca para diferentes tamanhos de sequências")
        plt.legend()
        plt.savefig("imgs/seek_op_statistics.png")
        plt.close()

    def plot_latency_comparison(self, requests_list):
        mean_latency_sstf, mean_latency_scan = self.calculate_latency_comparison(
            requests_list
        )

        # Plotting the comparison
        labels = ["SSTF", "SCAN"]
        mean_latencies = [mean_latency_sstf, mean_latency_scan]

        plt.bar(labels, mean_latencies, color=["blue", "orange"])
        plt.xlabel("Algoritmo de Escalonamento")
        plt.ylabel("Latência Total Média em segundos")
        plt.title("Comparação de Latência entre SSTF e SCAN")
        plt.savefig("imgs/latency_comparison.png")

    def calculate_latency_comparison(self, requests_list):
        latencies_sstf = []
        latencies_scan = []

        for requests in requests_list:
            total_latency_sstf, _ = self.sstf(requests)
            total_latency_scan, _ = self.scan(requests)
            total_latency_sstf = total_latency_sstf / 1000
            total_latency_scan = total_latency_scan / 1000
            latencies_sstf.append(total_latency_sstf)
            latencies_scan.append(total_latency_scan)

        mean_latency_sstf = statistics.mean(latencies_sstf)
        mean_latency_scan = statistics.mean(latencies_scan)

        return mean_latency_sstf, mean_latency_scan


# Main code
options = {
    "sector_size": 512,
    "num_tracks": 100,
    "sectors_per_track": 32,
    "seek_time": 3,
    "rotation_rpm": 7500,
    "transfer_time": 2,
}

sizes = [
    500,
    1000,
    1500,
    2000,
    2500,
]
requests_list = [[random.randint(0, 3199) for _ in range(size)] for size in sizes]

disk = DiskSimulator(**options)
disk.plot_statistics(sizes, requests_list)
disk.plot_latency_comparison(requests_list)
