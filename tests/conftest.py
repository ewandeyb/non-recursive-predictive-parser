import io
import textwrap

import pytest

from parsers.parse_table import ParseTable
from parsers.production_rules import ProductionRule


@pytest.fixture
def production_rules():
    return [
        None,
        ProductionRule(name="E", rule=["T", "E’"]),
        ProductionRule(name="E’", rule=["+", "T", "E’"]),
        ProductionRule(name="E’", rule=["e"]),
        ProductionRule(name="T", rule=["F", "T’"]),
        ProductionRule(name="T’", rule=["*", "F", "T’"]),
        ProductionRule(name="T’", rule=["e"]),
        ProductionRule(name="F", rule=["(", "E", ")"]),
        ProductionRule(name="F", rule=["id"]),
    ]


@pytest.fixture
def parse_table(production_rules):
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
    return ParseTable(ptbl, prod_rules=production_rules)
