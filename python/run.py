import sys
sys.path.insert(0, '..')

from argparse import (
    ArgumentParser,
    Namespace,
)
import datetime

from kkvhash import kkv_hash
from python.analyzer import Analyzer
from python.config import (
    Mode,
)
from python.testing.similarity import (
    sim_int_list_cross,
)
from python.utils import (
    read_values,
)


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--similarity', action='store_true', help='Print similarity')

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-1mln', action='store_true', dest='mode_1mln')
    mode.add_argument('-1mln-analyze', action='store_true', dest='mode_1mln_analyze')
    mode.add_argument('-korelogic-password', action='store_true', dest='korelogic_password')
    mode.add_argument('-1mln-key', action='store_true', dest='mode_1mln_key')

    return parser.parse_args()


def run_case(mode: Mode) -> None:
    analyzer = Analyzer(mode)

    if not read_values(analyzer):
        return

    print(f"Duplicates: {analyzer.find_duplicates()}")

    analyzer.dump()


def run_1mln_analyze() -> None:
    analyzer = Analyzer(Mode.m1mln)
    analyzer.load()

    duplicates_similarity = analyzer.calc_similarity()
    if duplicates_similarity is not None:
        for similarity, occurrence in duplicates_similarity:
            print(f"{similarity:3d}% - {occurrence}")
    else:
        print('There are no duplicates')


def expected_case(mode: Mode) -> None:
    analyzer = Analyzer(mode)
    if not analyzer.set_test_scenario():
        return

    base, start, end = analyzer.get_test_scenario()
    for i in range(start, end):
        # analyzer.append(kkv_hash(base+str(i).encode()), i))
        if not analyzer.append(kkv_hash((base + str(i)).encode()), i):
            break

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
        run_case(Mode.m1mln)
    elif args.mode_1mln_analyze:
        run_1mln_analyze()
    elif args.korelogic_password:
        run_case(Mode.korelogic_password)
    elif args.mode_1mln_key:
        expected_case(Mode.m1mln_key)
    else:
        run_simple(args.similarity)


if __name__ == '__main__':
    exit(main())
