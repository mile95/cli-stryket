from __future__ import annotations

import sys


class InvalidSystemException(Exception):
    pass


def parse_input_file(filename: str) -> list(str):
    with open(filename) as f:
        raw_system = f.read().split("\n")

    return raw_system


def validate_system(system: list(str)) -> list(str):
    system = [row for row in system if row]  # Remove empty lines
    if len(system) != 13:
        raise InvalidSystemException("System must have 13 rows")
    for i, row in enumerate(system):
        if row not in ["1", "x", "2", "1x", "12", "x2", "1x2"]:
            raise InvalidSystemException(f"Row {i + 1}: {row} is not valid")
    return system


def main() -> int:
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Please provide the filename with your system")
        return 1

    raw_system = parse_input_file(filename)
    try:
        system = validate_system(raw_system)
    except InvalidSystemException as e:
        print(f"Invalid system input. {e}")
        return 1

    print(system)


if __name__ == "__main__":
    raise SystemExit(main())
