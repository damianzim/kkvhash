from argparse import (
    ArgumentParser,
    Namespace,
)
import datetime

from analyzer import Analyzer
from config import (
    Mode,
)
from kkvhash import kkv_hash
from testing.similarity import (
    sim_int_list_cross,
)


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--similarity', action='store_true', help='Print similarity')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-1mln', action='store_true', dest='mode_1mln')

    return parser.parse_args()


def run_1mln() -> None:
    analyzer = Analyzer(Mode.m1mln)

    try:
        with open(analyzer.paths.input) as fr:
            index = 0
            while True:
                line = fr.readline()
                if not line:
                    break
                analyzer.append(kkv_hash(line.strip().encode()), index)
                index += 1
    except IOError:
        raise f"Cannot open the file: {analyzer.paths.input}"

    print(f"Duplicates: {analyzer.find_duplicates()}")

    analyzer.dump()


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

    if args.mode_1mln:
        run_1mln()
    else:
        run_simple(args.similarity)


if __name__ == '__main__':
    exit(main())
