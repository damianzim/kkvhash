from hashlib import sha256
from pathlib import Path
from typing import (
    Dict,
    Optional,
    Union,
)

from python.kkvhash import kkv_hash


kkvhash_py_path = Path('../python//kkvhash.py').resolve()


def read_values(analyzer: 'Analyzer') -> bool:
    try:
        with open(analyzer.paths.input) as fr:
            index = 0
            while True:
                line = fr.readline()
                if not line:
                    break
                if not analyzer.append(kkv_hash(line.strip().encode()), index):
                    break
                index += 1
    except Exception as e:
        return False
    finally:
        return True


def read_values_by_index(
        path: Path,
        indexes: Dict[int, int]) -> Optional[Dict[int, Dict[int, str]]]:
    values = {}
    try:
        with open(path) as fr:
            index = 0
            while True:
                line = fr.readline()
                if not line:
                    break

                if index in indexes:
                    _hash = indexes[index]
                    if _hash not in values:
                        values[_hash] = {}
                    values[_hash].update({index: line.strip()})
                index += 1
    except IOError:
        print(f"Cannot open the file: {path}")
        return None
    except:
        return None

    return values


def round_to(n: Union[float, int], precision: Union[float, int]) -> Union[float, int]:
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


def get_kkvhash_hash() -> str:
    return sha256(open(kkvhash_py_path).read().encode()).hexdigest()[:7]
