from pathlib import Path
from typing import (
    Dict,
    Optional,
)

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
