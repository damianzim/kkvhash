import datetime

from kkvhash import kkv_hash

if __name__ == '__main__':
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

    for key in data:
        start = datetime.datetime.now()
        temp_hash = kkv_hash(key.encode())
        time = datetime.datetime.now() - start
        print(
            f"{temp_hash:10d}",
            '-',
            f"{temp_hash:08X}",
            '-',
            f"{time.microseconds:10d}",
            '-',
            ' '.join(f"{ord(l):02X}" for l in key),
        )

