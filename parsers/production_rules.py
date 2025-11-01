from dataclasses import dataclass
from typing import TextIO


@dataclass
class ProductionRule:
    """Class for keeping track of a production rule."""

    name: str
    rule: list[str]

    @staticmethod
    def from_prod_string(prod_string: str) -> "ProductionRule":
        parts = [p.strip() for p in prod_string.strip().split(",", 2)]
        if len(parts) < 3:
            raise ValueError(
                f"expected 'id,LHS,RHS' format, got: {prod_string!r}"
            )

        name = parts[1]
        rhs = parts[2]

        rule_tokens: list[str] = [tok for tok in rhs.split() if tok]
        return ProductionRule(name=name, rule=rule_tokens)


def load_prod_rules(stream: TextIO) -> list[ProductionRule | None]:
    prod_rules: list[ProductionRule | None] = [None]
    for raw in stream:
        line = raw.strip()
        if not line:
            continue
        prod_rules.append(ProductionRule.from_prod_string(line))
    return prod_rules
