from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Customer:
    """Dados pessoais informados no formulário "Checkout: Your Information"."""

    first_name: str
    last_name: str
    postal_code: str


DEFAULT: Final = Customer("Ana", "Teste", "06500000")
