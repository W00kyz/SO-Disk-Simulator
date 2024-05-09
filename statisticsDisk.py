import random
import matplotlib.pyplot as plt
import numpy as np


def plotBarLatency(disk, sizes):

    aleatories, sequentials = __generateRandomLists(sizes)

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

    plt.savefig("imgs/comparasion_latency.png")
    plt.close()
    return


def __generateRandomLists(sizes):
    aleatories = [[random.randint(0, 1000) for _ in range(size)] for size in sizes]
    sequentials = [[i for i in range(size)] for size in sizes]

    return aleatories, sequentials


def plotRequestsLatency(disk, max_size=100):

    latency_aleatories_sstf = []
    latency_sequentials_sstf = []
    latency_aleatories_scan = []
    latency_sequentials_scan = []

    for size in range(1, max_size + 1):
        aleatories = [random.randint(0, 511) for _ in range(size)]
        sequentials = [i for i in range(size)]

        req_aleatory = aleatories.copy()
        req_sequential = sequentials.copy()

        # Calculando a latência para SSTF com requisições aleatórias e sequenciais
        latency_aleatories_sstf.append(disk.sstf(req_aleatory))
        latency_sequentials_sstf.append(disk.sstf(req_sequential))

        # Calculando a latência para SCAN com requisições aleatórias e sequenciais
        latency_aleatories_scan.append(disk.scan(req_aleatory))
        latency_sequentials_scan.append(disk.scan(req_sequential))

    plt.plot(range(1, max_size + 1), latency_aleatories_sstf, label="SSTF Aleatório")
    plt.plot(range(1, max_size + 1), latency_sequentials_sstf, label="SSTF Sequencial")
    plt.plot(range(1, max_size + 1), latency_aleatories_scan, label="SCAN Aleatório")
    plt.plot(range(1, max_size + 1), latency_sequentials_scan, label="SCAN Sequencial")

    plt.xlabel("Quantidade de Requisições")
    plt.ylabel("Latência (ms)")
    plt.title("Latência em Função da Quantidade de Requisições")
    plt.legend()
    plt.savefig("imgs/latency_by_num_req.png")
    plt.close()

    return
