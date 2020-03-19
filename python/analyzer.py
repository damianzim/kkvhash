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
from utils import (
    read_values_by_index,
)

class Analyzer(object):

    BUFFER_LIMIT: int = 16777216        # About 64MiB (only hashes)

    def __init__(self, mode: Mode, buffer_limit: int = None) -> None:
        self.paths = Paths.get_path(mode)
        self._limmit = Analyzer.BUFFER_LIMIT if buffer_limit is None else buffer_limit
        self.__buffer: List[Tuple[int, int]] = []
        self.__post_data = {
            'total_quantity': 0,
            'number_of_duplicates': 0,
            'duplicate_indicator': 0,
            'duplicates': {},
        }

    def size(self) -> int:
        return len(self.__buffer)

    def __len__(self) -> int:
        return self.size()

    def can_append(self) -> bool:
        return self.size() < self._limmit

    def load(self) -> bool:
        try:
            with open(self.paths.output) as fr:
                self.__post_data = yaml.load(fr, Loader=yaml.FullLoader)
                return self.__buffer is not None
        except:
            return False

    def dump(self) -> bool:
        try:
            with open(self.paths.output, 'w') as fw:
                yaml.dump(self.__post_data, fw)
                return True
        except:
            return False

    def append(self, hash: int, index: int) -> None:
        if self.can_append():
            self.__buffer.append((hash, index))
            self.__post_data['total_quantity'] += 1

    def __append_duplicate(self, hash: int, info: Tuple[int, List[int]]) -> None:
        self.__post_data['number_of_duplicates'] += info[0]
        self.__post_data['duplicates'][hash] =  { i: None for i in info[1]}

    def __update_duplicate_indicator(self) -> None:
        self.__post_data['duplicate_indicator'] = \
            self.__post_data['number_of_duplicates'] / self.__post_data['total_quantity']

    def assign_values_to_duplicates(self) -> None:
        if not len(self.__post_data['duplicates']):
            return

        read_values = read_values_by_index(
            self.paths.input,
            {
                index: hash
                for hash, indexes
                in self.__post_data['duplicates'].items()
                for index
                in indexes
            }
        )

        if read_values is None:
            return

        self.__post_data['duplicates'] = read_values

    def find_duplicates(self) -> int:
        if not self.size():
            return self.__post_data['number_of_duplicates']

        duplicates = []
        seen = {}

        for hash, index in self.__buffer:
            if hash not in seen:
                seen[hash] = [1, [index]]
            else:
                if seen[hash][0] == 1:
                    duplicates.append(hash)
                seen[hash][0] += 1
                seen[hash][1].append(index)

        for _duplicate in duplicates:
            self.__append_duplicate(_duplicate, seen[_duplicate])

        self.__update_duplicate_indicator()

        self.assign_values_to_duplicates()

        return len(duplicates)
