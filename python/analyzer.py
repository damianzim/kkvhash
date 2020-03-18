from pathlib import Path
from typing import (
    List,
    Tuple,
)

import yaml

from config import (
    Mode,
    Paths,
)

class Analyzer(object):

    BUFFER_LIMIT: int = 16777216        # About 64MiB (only hashes)

    def __init__(self, mode: Mode, buffer_limit: int = None) -> None:
        self.paths = Paths.get_path(mode)
        self._limmit = Analyzer.BUFFER_LIMIT if buffer_limit is None else buffer_limit
        self.__buffer: List[Tuple[int, int]] = []

    def size(self) -> int:
        return len(self.__buffer)

    def __len__(self) -> int:
        return self.size()

    def can_append(self) -> bool:
        return self.size() < self._limmit

    def load(self, path: Path) -> bool:
        try:
            with open(path) as fr:
                self.__buffer = yaml.load(fr, Loader=yaml.FullLoader)
                return self.__buffer is not None
        except:
            return False

    def dump(self, path: Path) -> bool:
        pass

    def append(self, hash: int, index: int) -> None:
        if self.can_append():
            self.__buffer.append((hash, index))

    def find_duplicates(self) -> int:
        self.__duplicates = []
        seen = {}

        for hash, index in self.__buffer:
            if hash not in seen:
                seen[hash] = 1
            else:
                if seen[hash] == 1:
                    self.__duplicates.append(hash)
                seen[hash] += 1

        return len(self.__duplicates)
