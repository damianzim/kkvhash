from enum import IntEnum, unique
from pathlib import Path
from os.path import (
    abspath,
    dirname,
)
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
    m1mln = 1 # 100 mln most popular passwords
    korelogic_password = 2
    m1mln_key = 3


INPUT_DIR = '../data/input'
OUTPUT_DIR = '../data/output'


class Paths(object):
    PATHS = {
        Mode.m1mln: [
            '1-million-password-list-top-1000000.txt',
            '1mln.yaml',
        ],
        Mode.korelogic_password: [
            'korelogic-password.txt',
            'korelogic-password.yaml',
        ],
        Mode.m1mln_key: [
            '',
            '1mln-key.yaml',
        ]
    }

    @staticmethod
    def get_paths(mode: Mode) -> Optional[PathSet]:
        if not mode in Paths.PATHS:
            return None

        base_path = dirname(abspath(__file__))

        a = Path(base_path, INPUT_DIR).resolve()
        a /= Paths.PATHS[mode][0]
        b = Path(base_path, OUTPUT_DIR).resolve()
        b /= Paths.PATHS[mode][1]
        return PathSet(a, b)


test_scenario = {
    Mode.m1mln_key: (
        'key',          # base
        0,              # <
        1000000,        # )
    ),
}

