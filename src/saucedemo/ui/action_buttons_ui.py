"""Botões de navegação acionados pelo rótulo visível no Gherkin (ele aciona "Finish").

O mesmo rótulo pode existir em mais de uma página (ex.: "Cancel"), mas o data-test é igual.
"""

from typing import Final

from saucedemo.ui import (
    cart_ui,
    checkout_complete_ui,
    checkout_info_ui,
    checkout_overview_ui,
    product_detail_ui,
)

_BUTTONS_BY_LABEL: Final = {
    "Back to products": product_detail_ui.BACK_TO_PRODUCTS,
    "Back Home": checkout_complete_ui.BACK_HOME,
    "Continue Shopping": cart_ui.CONTINUE_SHOPPING,
    "Checkout": cart_ui.CHECKOUT,
    "Continue": checkout_info_ui.CONTINUE,
    "Cancel": checkout_info_ui.CANCEL,
    "Finish": checkout_overview_ui.FINISH,
}


def by_label(label: str) -> str:
    if label not in _BUTTONS_BY_LABEL:
        raise ValueError(
            f"Botão sem locator mapeado: '{label}'. Mapeados: {list(_BUTTONS_BY_LABEL)}"
        )
    return _BUTTONS_BY_LABEL[label]
