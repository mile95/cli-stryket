from __future__ import annotations
from cli_stryket.system_exception import InvalidSystemException


def read_input(filename: str) -> list(str):
    raw_system = parse_input_file(filename)
    validated_system = validate_system(raw_system)
    formatted_system = [format_system_row(row) for row in validated_system]
    return formatted_system


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


def format_system_row(system_row: str) -> str:
    if len(system_row) == 3:
        return system_row
    if len(system_row) == 2:
        if "1" not in system_row:
            return " x2"
        if "x" not in system_row:
            return "1 2"
        if "2" not in system_row:
            return "1x "
    if len(system_row) == 1:
        if "1" in system_row:
            return "1  "
        if "x" in system_row:
            return " x "
        if "2" in system_row:
            return "  2"
