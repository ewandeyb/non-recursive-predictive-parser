from typing import TextIO


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
