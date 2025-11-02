"""
given a ParseTable object, create a table with the stack, input buffer, and action taken at each step of parsing.

input: ParseTable object, "id + id * id"
test_rules.prsd:
E $,id + id * id $
T E’ $,id + id * id $,Output E > T E’
F T’ E’ $,id + id * id $,Output T > F T’
id T’ E’ $,id + id * id $,Output F > id
T’ E’ $,+ id * id $,Match id
E’ $,+ id * id $,Output T’ > e
+ T E’ $,+ id * id $,Output E’ > + T E’
T E’ $,id * id $,Match +
F T’E’ $,id * id $,Output T > F T’
id T’ E’ $,id * id $,Output F > id
T’ E’ $,* id $,Match id
* F T’ E’ $,* id $,Output T’ > * F T’
F T’ E’ $,id $,Match *
id T’ E’ $,id $,Output F > id
T’ E’ $,$,Match id
E’ $,$,Output T’ > e
$,$,Output E’ > e
,,Match $
"""

from parsers.parse_table import ParseTable


def create_parsing_steps_table(
    parse_table: ParseTable, input_string: str
) -> list[list[str]]:
    """Creates a table of parsing steps from the given ParseTable and input string.

    Args:
        parse_table (ParseTable): The parse table object containing parsing rules.
        input_string (str): The input string to be parsed.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing each step in the parsing process.
    """
    steps = []

    assert parse_table.rules[1]  # type check
    stack = ["$", parse_table.rules[1].name]
    input_buffer = ["$"] + input_string.split()[::-1]

    current_stack = " ".join(reversed(stack))
    current_input = " ".join(reversed(input_buffer))
    steps.append([current_stack, current_input, ""])

    while stack:
        top_stack = stack.pop()

        if top_stack == input_buffer[-1]:  # Match
            action = f"Match {top_stack}"
            input_buffer.pop()

        elif top_stack in parse_table.table:  # Non-terminal
            terminal = input_buffer[-1]

            if terminal in parse_table.table[top_stack]:
                rule_index = parse_table.table[top_stack][terminal]
                production_rule = parse_table.rules[rule_index]

                assert production_rule  # type check
                action = f"Output {production_rule.name} > {' '.join(production_rule.rule) if production_rule.rule else 'e'}"

                for symbol in reversed(production_rule.rule):
                    if symbol != "e":  # Skip epsilon
                        stack.append(symbol)
            else:
                action = (
                    f"Error: No rule for {top_stack} with lookahead {terminal}"
                )
                break
        else:
            action = f"Error: Unexpected symbol {top_stack}"
            break

        current_stack = " ".join(reversed(stack))
        current_input = " ".join(reversed(input_buffer))
        steps.append([current_stack, current_input, action])

    return steps


def create_file(steps: list[list[str]], input_filename: str):
    """Creates a .prsd file with the parsing steps.

    Args:
        steps (list[list[str]]): The list of parsing steps.
        input_filename (str): The name of the input file to derive the output filename.
    """

    output_filename = "test_" + input_filename + ".prsd"
    with open(output_filename, "w", encoding="utf-8") as f:
        for step in steps:
            f.write(",".join(step) + "\n")
