import io
import textwrap

from parsers.parse_table import ParseTable


class TestParseTableClass:
    def test_parse_table_class_initialization(self):
        csv_content = textwrap.dedent(
            """\
        ,id,+,*,(,),$
        E,1,,,1,,
        E’,,2,,,3,3
        T,4,,,4,,
        T’,,6,5,,6,6
        F,8,,,7,,"""
        )
        ptbl = io.StringIO(csv_content)

        expected_terminals = ["id", "+", "*", "(", ")", "$"]
        expected_parse_table = {
            "E": {"id": 1, "(": 1},
            "E’": {"+": 2, ")": 3, "$": 3},
            "T": {"id": 4, "(": 4},
            "T’": {"+": 6, "*": 5, ")": 6, "$": 6},
            "F": {"id": 8, "(": 7},
        }

        parse_table_obj = ParseTable(ptbl, [])
        assert parse_table_obj.terminals == expected_terminals
        assert parse_table_obj.table == expected_parse_table
