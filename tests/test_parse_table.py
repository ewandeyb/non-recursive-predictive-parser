import io
import textwrap

from parsers.parse_table import ParseTable, get_terminals, load_parse_table

csv_content = textwrap.dedent(
    """\
        ,id,+,*,(,),$
        E,1,,,1,,
        E’,,2,,,3,3
        T,4,,,4,,
        T’,,6,5,,6,6
        F,8,,,7,,"""
)


def test_parse_table():
    ptbl = io.StringIO(csv_content)

    expected_parse_table = {
        "E": {"id": 1, "(": 1},
        "E’": {"+": 2, ")": 3, "$": 3},
        "T": {"id": 4, "(": 4},
        "T’": {"+": 6, "*": 5, ")": 6, "$": 6},
        "F": {"id": 8, "(": 7},
    }

    result = load_parse_table(ptbl)
    assert result == expected_parse_table


def test_get_terminals():
    ptbl = io.StringIO(csv_content)

    expected_terminals = ["id", "+", "*", "(", ")", "$"]

    result = get_terminals(ptbl)
    assert result == expected_terminals


class TestParseTableClass:
    def test_parse_table_class_initialization(self):
        ptbl = io.StringIO(csv_content)

        expected_parse_table = load_parse_table(ptbl)

        expected_terminals = get_terminals(ptbl)

        parse_table_instance = ParseTable(ptbl, prod_rules=[])
        assert parse_table_instance.table == expected_parse_table
        assert parse_table_instance.terminals == expected_terminals
        assert parse_table_instance.rules == []
