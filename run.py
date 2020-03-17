from argparse import (
    ArgumentParser,
    Namespace,
)
import datetime
from enum import Enum
from pathlib import Path

from kkvhash import kkv_hash
from testing.similarity import sim_int_list_cross


INPUT_DIR = 'data/input'
OUTPUT_DIR = 'data/output'
FILENAMES = {
    '100mln': '10-million-password-list-top-1000000.txt',
    'korelogic_password': 'korelogic-password.txt',
}


class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class DataType(NoValue):
    INPUT = 'input'
    OUTPUT = 'output'


def resolve_data_path(filename: str, datatype: DataType) -> Path:
    if not datatype in DataType:
        return Path()

    path = Path(INPUT_DIR if datatype == DataType.INPUT else OUTPUT_DIR)
    path /= filename

    return path


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--similarity', action='store_true', help='Print similarity')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-100mln', action='store_true', dest='mode_100mln')

    return parser.parse_args()


def run_100mln() -> None:
    path = resolve_data_path(FILENAMES['100mln'], DataType.INPUT)

    hashes = []

    try:
        with open(path) as fr:
            while True:
                line = fr.readline()
                if not line:
                    break
                hashes.append(kkv_hash(line.strip().encode()))
    except IOError:
        raise f"Cannot open the file {str(path)}"

    seen = {}
    dupes = []

    for x in hashes:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1

    print(f"Duplicates: {len(dupes)}")

    # dupes = sorted(map(lambda x: [x, seen[x]], dupes), key=lambda x: x[1], reverse=True)
    # print(dupes)


def run_simple(similarity: bool = False) -> None:
    data = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "some text",
        "some textt",
        "foo",
        "bar",
        "baz",
    ]

    print(f"{'Hash dec':10} - {'Hash hex':8} - {'Time (us)':10} - Input hex")

    hashes = []

    for key in data:
        start = datetime.datetime.now()
        temp_hash = kkv_hash(key.encode())
        time = datetime.datetime.now() - start
        hashes.append(temp_hash)
        print(
            f"{temp_hash:10d}",
            '-',
            f"{temp_hash:08X}",
            '-',
            f"{time.microseconds:10d}",
            '-',
            ' '.join(f"{ord(l):02X}" for l in key),
        )

    if similarity:
        print('Similarity:')
        [
            print(' '.join(f"{num:.2f}" for num in e))
            for e
            in sim_int_list_cross(hashes)
        ]


def main() -> None:
    args = parse_args()

    if args.mode_100mln:
        run_100mln()
    else:
        run_simple(args.similarity)


if __name__ == '__main__':
    exit(main())
