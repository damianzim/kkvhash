from argparse import (
    ArgumentParser,
    Namespace,
)
import datetime

from kkvhash import kkv_hash
from testing.similarity import sim_int_list_cross


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--similarity', action='store_true', help='Print similarity')

    return parser.parse_args()


def main() -> None:
    args = parse_args()

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

    if args.similarity:
        print('Similarity:')
        [
            print(' '.join(f"{num:.2f}" for num in e))
            for e
            in sim_int_list_cross(hashes)
        ]


if __name__ == '__main__':
    exit(main())
