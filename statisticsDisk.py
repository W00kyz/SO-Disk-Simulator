from cProfile import label
import random
import attr
import matplotlib.pyplot as plt
import numpy as np


def plotLatency(disk, request):
    latencies = []
    seek_distances = []
    for block in request:
        latency, seek_distance = disk.calculate_latency(block)
        latencies.append(latency)
        seek_distances.append(seek_distance)

    plt.plot(latencies, label="Latency")
    plt.plot(seek_distances, label="Seek Distance")
    plt.xlabel("Block Index")
    plt.ylabel("Latency/Seek Distance")
    plt.title("Latency and Seek Distance for Request")
    plt.legend()
    plt.show()


def plotBarLatency(disk, sizes):

    aleatories, sequentials = generateRandomLists(sizes)

    categorias = ("SSTF", "SCAN")

    latencies = {
        "Latência Aleatória": (
            disk.sstf(aleatories[-1]),
            disk.scan(aleatories[-1]),
        ),
        "Latência Sequencial": (
            disk.sstf(sequentials[-1]),
            disk.scan(sequentials[-1]),
        ),
    }

    x = np.arange(len(categorias))

    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for attribute, measurement in latencies.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel("Latência Total (ms)")
    ax.set_title("Tempo de Execução por Algoritmo")
    ax.set_xticks(x + width, categorias)
    ax.legend(loc="upper left", ncols=2)

    plt.show()

    return


def generateRandomLists(sizes):
    aleatories = [[random.randint(0, 1000) for _ in range(size)] for size in sizes]
    sequentials = [[i for i in range(size)] for size in sizes]

    return aleatories, sequentials


def plotRequestsLatency(disk, sizes):

    aleatories, sequentials = generateRandomLists(sizes)

    latency_aleatories_sstf = []
    latency_sequentials_sstf = []
    latency_aleatories_scan = []
    latency_sequentials_scan = []

    for aleatory, sequential in zip(aleatories, sequentials):
        latency_aleatories_sstf.append(disk.sstf(aleatory))
        latency_sequentials_sstf.append(disk.sstf(sequential))
        latency_aleatories_scan.append(disk.scan(aleatory))
        latency_sequentials_scan.append(disk.scan(sequential))

    plt.plot(sizes, latency_aleatories_sstf, label="Latência Aleatório")
    plt.plot(sizes, latency_sequentials_sstf, label="Latência Sequencial")

    plt.xlabel("Tipo de Acesso")
    plt.ylabel("Latência Total")
    plt.title("Comparação entre Acesso Aleatório e Sequencial")

    plt.legend()
    plt.show()

    return
