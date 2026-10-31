from dataclasses import dataclass


@dataclass(frozen=True)
class ProductRow:
    """Produto como exibido em uma listagem: nome e preço formatado (ex.: "$29.99")."""

    name: str
    price: str


@dataclass(frozen=True)
class CartItemRow:
    """Item como exibido no carrinho: quantidade, nome e preço formatado."""

    quantity: str
    name: str
    price: str
