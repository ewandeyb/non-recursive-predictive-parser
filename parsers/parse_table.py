from dataclasses import dataclass
from typing import TextIO

from parsers.production_rules import ProductionRule


@dataclass
class ParseTable:
    table: dict[str, dict[str, int]]
    terminals: list[str]
    rules: list[ProductionRule | None]

    def __init__(
        self,
        pbtl_ptr: TextIO,
        prod_rules: list[ProductionRule | None],
    ) -> None:
        self.table = load_parse_table(pbtl_ptr)
        self.terminals = get_terminals(pbtl_ptr)
        self.rules = prod_rules


def load_parse_table(ptbl: TextIO) -> dict[str, dict[str, int]]:
    """Creates a parse table from a given file pointer.

    Format of return:
    {
        'NonTerminal1': {
            'Terminal1': rule_index,
            'Terminal2': rule_index,
            ...
        },
        'NonTerminal2': {...}
    }
    """

    ptbl.seek(0)  # Reset pointer to the beginning
    parse_table: dict[str, dict[str, int]] = {}
    # Extract headers
    headers = (
        ptbl.readline().strip().split(",")[1:]
    )  # Skip the first empty cell

    for line in ptbl:  # from second line to end
        parts = line.strip().split(",")
        non_terminal = parts[0]
        parse_table[non_terminal] = {}

        for i, entry in enumerate(parts[1:]):
            terminal = headers[i]
            if entry:
                try:
                    parse_table[non_terminal][terminal] = int(entry)
                except ValueError:
                    raise ValueError(
                        f"Invalid integer value '{entry}' for non-terminal '{non_terminal}', terminal '{terminal}'"
                    )

    return parse_table


def get_terminals(ptbl: TextIO) -> list[str]:
    """Extracts the list of terminals from the parse table file pointer."""
    ptbl.seek(0)  # Reset pointer to the beginning
    terminals = (
        ptbl.readline().strip().split(",")[1:]
    )  # Skip the first empty cell
    return terminals
