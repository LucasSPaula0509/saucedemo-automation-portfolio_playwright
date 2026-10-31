"""Cenários @defeito -> ID do defeito (sem alterar as features).

O ID vira link de issue no Allure (--allure-link-pattern no pyproject.toml).
Chave: tag de rastreabilidade do cenário, sem "@".
"""

from typing import Final

KNOWN_DEFECTS: Final = {
    # DEF-001 - Reset App State não restaura os botões dos produtos para "Add to cart"
    "CT013_Carrinho": "DEF-001",
    # DEF-002 - Checkout é iniciado com o carrinho vazio
    "CT011_Checkout": "DEF-002",
    # DEF-003 - Menu lateral exibe a opção "Dynamic Catalog", ausente no resultado esperado
    "CT009_Produtos": "DEF-003",
}
