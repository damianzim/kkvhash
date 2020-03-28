from itertools import (
    combinations,
)
from pathlib import Path
from typing import (
    List,
    Optional,
    Tuple,
)

import yaml

from python.config import (
    test_scenario,
    Mode,
    Paths,
)
from python.testing.similarity import (
    sim_str,
)
from python.utils import (
    read_values_by_index,
    round_to,
)

class Analyzer(object):

    BUFFER_LIMIT: int = 16777216        # About 64MiB (only hashes)

    def __init__(self, mode: Mode, buffer_limit: int = None) -> None:
        self.paths = Paths.get_paths(mode)
        self._mode = mode
        self._limmit = Analyzer.BUFFER_LIMIT if buffer_limit is None else buffer_limit
        self.__buffer: List[Tuple[int, int]] = []
        self.__test_scenario = None
        self.__post_data = {
            'total_quantity': 0,
            'number_of_duplicates': 0,
            'duplicate_indicator': 0,
            'with_the_same_hash': 0,
            'duplicates': {},
        }

    def size(self) -> int:
        return len(self.__buffer)

    def __len__(self) -> int:
        return self.size()

    def set_test_scenario(self) -> bool:
        try:
            self.__test_scenario = test_scenario[self._mode]
        except KeyError:
            print('There is no test scenario for the running mode')
        finally:
            return self.__test_scenario is not None

    def get_test_scenario(self) -> Tuple[str, int, int]:
        if self.__test_scenario is None:
            raise Exception('Test scenario is not set')
        return self.__test_scenario

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

    def append(self, hash: int, index: int) -> bool:
        if self.can_append():
            self.__buffer.append((hash, index))
            self.__post_data['total_quantity'] += 1
            return True
        else:
            return False

    def __append_duplicate(self, hash: int, info: Tuple[int, List[int]]) -> None:
        self.__post_data['number_of_duplicates'] += info[0]
        self.__post_data['duplicates'][hash] = { i: None for i in info[1]} \
            if self.__test_scenario is None \
            else { i: self.__test_scenario[0] + str(i) for i in info[1]}

    def __update_duplicate_indicator(self) -> None:
        self.__post_data['duplicate_indicator'] = \
            self.__post_data['number_of_duplicates'] / self.__post_data['total_quantity']

    def assign_values_to_duplicates(self) -> None:
        if not len(self.__post_data['duplicates']):
            return

        if self.__test_scenario is not None:
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

        self.__post_data['with_the_same_hash'] = len(duplicates)
        self.__update_duplicate_indicator()

        if self.__test_scenario is None:
            # Assign values to duplicates if the mode is not `test scenario`for
            # this mode the vales are already assigned in self.__append_duplicate()
            # method, it introduces a little confusion, but it's faster
            self.assign_values_to_duplicates()

        return len(duplicates)

    def calc_similarity(self) -> Optional[Tuple[Tuple[int, int], ...]]:
        if not len(self.__post_data['duplicates']):
            return None

        result = [0] * 21

        for duplicate in self.__post_data['duplicates'].values():
            pairs = list(combinations(duplicate.values(), 2))
            for pair in pairs:
                similarity = round_to(sim_str(*pair), 0.05)
                result[int(similarity * 100) // 5] += 1

        return tuple(
            (index * 5, occurrence)
            for index, occurrence
            in enumerate(result)
        )
