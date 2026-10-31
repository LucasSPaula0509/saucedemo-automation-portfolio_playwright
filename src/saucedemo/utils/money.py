"""Conversão entre textos monetários da tela ("Tax: $0.80", "$29.99") e Decimal."""

import re
from decimal import ROUND_HALF_UP, Decimal

AMOUNT = re.compile(r"\$(\d+(?:\.\d+)?)")
CENTS = Decimal("0.01")


def parse(text: str) -> Decimal:
    match = AMOUNT.search(text)
    if match is None:
        raise ValueError(f"Valor monetário não encontrado em: '{text}'")
    amount = Decimal(match.group(1))
    if amount != amount.quantize(CENTS):
        raise ValueError(f"Valor monetário com mais de 2 casas decimais: '{text}'")
    return amount.quantize(CENTS)


def format_amount(amount: Decimal) -> str:
    return f"${amount.quantize(CENTS, rounding=ROUND_HALF_UP)}"
