from argparse import (
    ArgumentParser,
    Namespace,
)
from functools import reduce
from os.path import (
    abspath,
    dirname,
)
from pathlib import Path
from typing import (
    List,
    Optional,
    TextIO,
)


letters =  {
	'a': ['A', '4', '@'],
	'b': ['B', '6', '8'],
	'c': ['C', '('],
	'd': ['D', '0'],
	'e': ['E', '3'],
	'f': ['F'],
	'g': ['G'],
	'h': ['H'],
	'i': ['I', '1', '!', '|'],
	'j': ['J'],
	'k': ['K'],
	'l': ['L', '1', '7','!', '|'],
	'm': ['M'],
	'n': ['N'],
	'o': ['O', '0'],
	'p': ['P'],
	'q': ['Q', 'g'],
	'r': ['R'],
	's': ['S', '5', '$'],
	't': ['T', '7'],
	'u': ['U'],
	'v': ['V', 'u'],
	'w': ['W'],
	'x': ['X'],
	'y': ['Y'],
	'z': ['Z', '2'],
}

data_path = '../data/dictionary'


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    parser.add_argument('--min-length', action='store', type=int, default=-1)

    return parser.parse_args()


class FileIterator(object):

    def __init__(self, ifs: TextIO) -> None:
        self._ifs = ifs

    def __iter__(self) -> 'FileIterator':
        return self

    def __next__(self) -> Optional[str]:
        if self._ifs.closed:
            return None

        line = self._ifs.readline().strip()
        if line:
            return line
        raise StopIteration


class Buffer(object):

    def __init__(self, size: int) -> None:
        self._size = size
        self._data = []

    def __len__(self) -> int:
        return len(self._data)

    def is_full(self) -> bool:
        return len(self) == self._size

    def append(self, word: str) -> bool:
        """Return True when the buffer is full"""
        if len(word):
            self._data.append(word)
        return self.is_full()

    def clear(self) -> None:
        self._data = []

    def dump(self) -> List[str]:
        return self._data


class LetterStat(object):
    letters: List[str]
    limit: int
    current: int = 0

    def __init__(self, letters: List[str], tick_height: int) -> None:
        self.letters = letters
        self.limit = len(letters)

        self._tick_divisor = tick_height // self.limit

    def get(self, height: int) -> str:
        if not height % self._tick_divisor:
            if self.current + 1 < self.limit:
                self.current += 1
            else:
                self.current = 0
        return self.letters[self.current]


class WordCombinations(object):

    def __init__(self, word: str) -> None:
        self._word = word
        self._combinations = 0
        self._i = 0
        self._stat: List[LetterStat] = None
        self._last_initialized = 1

    def __iter__(self) -> 'WordCombinations':
        return self

    def __next__(self) -> str:
        if self._stat is not None and self._i < self._combinations:
            self._i += 1
            return ''.join([letter.get(self._i) for letter in self._stat])
        raise StopIteration

    def count(self) -> int:
        if not self._word:
            return -1

        if not self._word.islower() or not self._word.isalpha():
            return -1

        self._stat = []
        for x in self._word:
            letter_combinations = [x] + letters[x]
            self._last_initialized *= len(letter_combinations)
            self._stat.append(
                LetterStat(letter_combinations, self._last_initialized)
            )

        self._combinations = reduce(
            lambda x, y: x * y,
            map(lambda x: x.limit, self._stat),
        )

        return self._combinations

    def print_farewell(self) -> None:
        if self._word and self._combinations > 0:
            print(f"Word: {self._word} Combinations: {self._combinations}")


class Dictionary(object):

    buf_size = 1024
    input_file = 'input.txt'
    output_dir = 'output/'
    output_extension = '.txt'

    def __init__(self, min_length: int = -1,  debug: bool = False) -> None:
        self.debug = debug
        self.min_length = min_length

        self._base_path = dirname(abspath(__file__))
        self._fdict: TextIO = None
        self._buf = Buffer(Dictionary.buf_size)
        self._fword: TextIO = None

    def __del__(self) -> None:
        self._fdict.close()

    def dump(self) -> bool:
        if self._fword.closed:
            return False

        to_save = '\n'.join(self._buf.dump()) + '\n'
        saved = self._fword.write(to_save)

        if self.debug:
            if len(to_save) == saved:
                print(f"Dumped: {len(self._buf)}")
            else:
                print(f"Dumped: {saved}/{to_save} bytes")

        if saved > 0:
            self._buf.clear()
            return True
        else:
            return False

    def run(self) -> int:
        """Return number of words that was calculated"""

        fdict_path = Path(self._base_path, data_path, self.input_file).resolve()
        if not fdict_path.is_file():
            return -1
        try:
            self._fdict = open(fdict_path)
        except IOError:
            print(f"Cannot open file: {fdict_path}")
            return -1

        counter = 0
        for line in FileIterator(self._fdict):
            if not line:
                break

            if self.min_length > 0 and len(line) < self.min_length:
                continue

            if self.debug:
                print(f"Processing: {line}")

            words = WordCombinations(line)
            if words.count() < 1:
                continue

            output_path = Path(
                self._base_path,
                data_path,
                self.output_dir,
                line + self.output_extension
            )

            try:
                self._fword = open(output_path, "w")
            except IOError:
                print(f"Cannot open file: {output_path}")
                continue

            for word in words:
                if self._buf.append(word):
                    if not self.dump():
                        break

            if len(self._buf) and not self.dump():
                self._buf.clear()
            words.print_farewell()
            self._fword.close()
            counter += 1
        return counter


if __name__ == '__main__':
    args = parse_args()
    dictionary = Dictionary(min_length=args.min_length, debug=args.debug)

    result = dictionary.run()
    if result < 0:
        print('Something went wrong!')
    else:
        print(f"Processed {result} words")

