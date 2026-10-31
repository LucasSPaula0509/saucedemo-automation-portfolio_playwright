from playwright.sync_api import Locator

from saucedemo.pages.base_page import BasePage
from saucedemo.ui import header_ui


class HeaderComponent(BasePage):
    def cart_badge(self) -> Locator:
        """Contador do carrinho; o step valida o texto ou a ausência com expect."""
        return self._locator(header_ui.CART_BADGE)

    def open_cart(self) -> None:
        self._click(header_ui.CART_LINK)

    def page_title(self) -> Locator:
        return self._locator(header_ui.PAGE_TITLE)
