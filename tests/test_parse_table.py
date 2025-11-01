import io
import textwrap
from parsers.parse_table import create_parse_table


def test_create_parse_table():
    csv_content = textwrap.dedent("""\
        ,id,+,*,(,),$
        E,1,,,1,,
        E’,,2,,,3,3
        T,4,,,4,,
        T’,,6,5,,6,6
        F,8,,,7,,""")

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
