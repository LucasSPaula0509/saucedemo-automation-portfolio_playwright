from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final, Self

from saucedemo.utils import money

TAX_RATE: Final = Decimal("0.08")


@dataclass(frozen=True)
class OrderTotals:
    """Regra de cálculo do resumo do pedido: subtotal = soma dos itens; imposto = 8% do subtotal,
    arredondado a 2 casas (HALF_UP); total = subtotal + imposto.
    """

    item_prices: list[Decimal]
    subtotal: Decimal
    tax: Decimal
    total: Decimal

    @classmethod
    def from_item_prices(cls, formatted_prices: list[str]) -> Self:
        prices = [money.parse(price) for price in formatted_prices]
        subtotal = sum(prices, Decimal("0.00"))
        tax = (subtotal * TAX_RATE).quantize(money.CENTS, rounding=ROUND_HALF_UP)
        return cls(prices, subtotal, tax, subtotal + tax)

    def describe(self) -> str:
        items = ", ".join(money.format_amount(price) for price in self.item_prices)
        rate = (TAX_RATE * 100).normalize()
        subtotal = money.format_amount(self.subtotal)
        return (
            f"Itens: [{items}]\n"
            f"Subtotal (soma dos itens): {subtotal}\n"
            f"Imposto ({rate}% de {subtotal}, HALF_UP): {money.format_amount(self.tax)}\n"
            f"Total (subtotal + imposto): {money.format_amount(self.total)}\n"
        )
