from typing import (
    List,
)

def sim_int(a: int, b: int) -> float:
    if a == 0 and b == 0:
        return 1

    return round(min(a, b) / max(a, b), 2)

def sim_int_list_cross(numbers: List[int]) -> List[float]:
    return [
        [
            sim_int(i, j)
            for j
            in numbers
        ]
        for i
        in numbers
    ]
