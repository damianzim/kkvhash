from enum import IntEnum, unique
from pathlib import Path
from typing import (
    Dict,
    NamedTuple,
    Optional,
)


class PathSet(NamedTuple):
    input: Path
    output: Path


@unique
class Mode(IntEnum):
    m100mln = 1 # 100 mln most popular passwords
    korelogic_password = 2


INPUT_DIR = '../data/input'
OUTPUT_DIR = '../data/output'


class Paths(object):
    PATHS = {
        Mode.m100mln: [
            '10-million-password-list-top-1000000.txt',
            '100mln.yaml',
        ]
    }

    @staticmethod
    def get_path(mode: Mode) -> Optional[PathSet]:
        if not mode in Paths.PATHS:
            return None

        a = Path(INPUT_DIR)
        a /= Paths.PATHS[mode][0]
        b = Path(OUTPUT_DIR)
        b /= Paths.PATHS[mode][1]
        return PathSet(a, b)
