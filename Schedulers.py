from abc import ABC
from typing import List


class SchedulerAlgorithm(ABC):
    def schedule(self, head: int, requests: List[int]) -> List[int]:
        raise NotImplemented()


class SSTF(SchedulerAlgorithm):
    def schedule(self, head: int, requests: List[int]) -> List[int]:
        return sorted(requests, key=lambda curr_track: abs(curr_track - head))
