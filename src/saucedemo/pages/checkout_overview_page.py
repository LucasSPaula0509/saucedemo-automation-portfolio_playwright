import re

from saucedemo.data import paths
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import checkout_overview_ui as ui

TRAILING_COLON = re.compile(r":\s*$")


class CheckoutOverviewPage(LoadablePage):
    path = paths.CHECKOUT_STEP_TWO
    marker_selector = ui.SUMMARY_CONTAINER

    def summary_info(self) -> dict[str, str]:
        """Blocos informativos do resumo (pagamento e entrega), indexados pelo rótulo sem os
        dois-pontos finais exibidos na tela (ex.: "Payment Information:" -> "Payment Information").
        """
        return {
            self._label(ui.PAYMENT_INFO_LABEL): self._text_of(ui.PAYMENT_INFO_VALUE),
            self._label(ui.SHIPPING_INFO_LABEL): self._text_of(ui.SHIPPING_INFO_VALUE),
        }

    def item_prices(self) -> list[str]:
        return self._texts_of(ui.ITEM_PRICES)

    def subtotal(self) -> str:
        return self._text_of(ui.SUBTOTAL)

    def tax(self) -> str:
        return self._text_of(ui.TAX)

    def total(self) -> str:
        return self._text_of(ui.TOTAL)

    def finish(self) -> None:
        self._click(ui.FINISH)

    def _label(self, selector: str) -> str:
        return TRAILING_COLON.sub("", self._text_of(selector))
