import configparser
from diskScheduler import DiskSimulator
from statisticsDisk import *


def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    disk_settings = dict(config.items("DiskSettings"))
    disk_settings = {key: int(value) for key, value in disk_settings.items()}
    simulation_settings = dict(config.items("SimulationSettings"))
    simulation_settings["sizes"] = list(
        map(int, simulation_settings["sizes"].split(", "))
    )
    return disk_settings, simulation_settings


def main():
    disk_settings, simulation_settings = read_config("config.ini")

    disk = DiskSimulator(**disk_settings)
    plotBarLatency(disk, simulation_settings["sizes"])
    plotRequestsLatency(disk)


if __name__ == "__main__":
    main()
