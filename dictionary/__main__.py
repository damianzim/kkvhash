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
	'b': ['B'],
	'c': ['C'],
	'd': ['D'],
	'e': ['E', '3'],
	'f': ['F'],
	'g': ['G'],
	'h': ['H'],
	'i': ['I'],
	'j': ['J'],
	'k': ['K'],
	'l': ['L'],
	'm': ['M'],
	'n': ['N'],
	'o': ['O', '0'],
	'p': ['P'],
	'q': ['Q', 'g'],
	'r': ['R'],
	's': ['S', '5', '$'],
	't': ['T'],
	'u': ['U'],
	'v': ['V', 'u'],
	'w': ['W'],
	'x': ['X'],
	'y': ['Y'],
	'z': ['Z'],
}

data_path = '../data/dictionary'


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


class WordCombinations(object):

    def __init__(self, word: str) -> None:
        self._word = word
        self._combinations = 0
        self._i = 0

    def __iter__(self) -> 'WordCombinations':
        return self

    def __next__(self) -> str:

        # GET COMBINATIONS HERE!
        if self._i < 1:
            self._i += 1
            return ''
        raise StopIteration

    def print_farewell(self) -> None:
        if self._word and self._combinations > 0:
            print(f"Word: {self._word} Combinations: {self._i}")


class Dictionary(object):

    buf_size = 128
    input_file = 'input.txt'
    output_dir = 'output/'
    output_extension = '.txt'

    def __init__(self) -> None:
        self._base_path = dirname(abspath(__file__))
        self._fdict: TextIO = None
        self._buf = Buffer(Dictionary.buf_size)
        self._fword: TextIO = None

    def __del__(self) -> None:
        self._fdict.close()

    def dump(self) -> bool:
        if self._fword.closed:
            return False

        saved = self._fword.write('\n'.join(self._buf.dump()) + '\n')
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
        self._fdict = open(fdict_path)

        counter = 0
        for line in FileIterator(self._fdict):
            if not line:
                return counter
            output_path = Path(
                self._base_path,
                data_path,
                self.output_dir,
                line + self.output_extension
            )

            self._fword = open(output_path, "w")

            words = WordCombinations(line)

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
    dictionary = Dictionary()

    result = dictionary.run()
    if result < 0:
        print('Something went wrong!')
    else:
        print(f"Saved: {result}")

