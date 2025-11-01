import pytest

from parsers.production_rules import ProductionRule


def test_from_prod_string_parses_three_parts():
    s = "1,E,T E'"
    pr = ProductionRule.from_prod_string(s)
    assert pr.name == "E"
    assert pr.rule == ["T", "E'"]


def test_from_prod_string_bad_format_raises():
    with pytest.raises(ValueError):
        ProductionRule.from_prod_string("E,T")
