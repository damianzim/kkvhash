from difflib import (
    SequenceMatcher,
)
from typing import (
    List,
)


def sim_int(a: int, b: int) -> float:
    if a == 0 and b == 0:
        return 1

    return round(min(a, b) / max(a, b), 2)


def sim_int_list_cross(numbers: List[int]) -> List[List[float]]:
    return [
        [
            sim_int(i, j)
            for j
            in numbers
        ]
        for i
        in numbers
    ]


def sim_str(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def sim_str_list_cross(strings: List[str]) -> List[List[float]]:
    return [
        [
            sim_str(x, y)
            if i != j
            else 1.0
            for j, y
            in enumerate(strings)
        ]
        for i, x
        in enumerate(strings)
    ]
