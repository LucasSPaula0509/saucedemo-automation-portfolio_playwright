from playwright.sync_api import Locator

from saucedemo.data import paths
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import checkout_complete_ui


class CheckoutCompletePage(LoadablePage):
    path = paths.CHECKOUT_COMPLETE
    marker_selector = checkout_complete_ui.COMPLETE_HEADER

    def confirmation_message(self) -> Locator:
        return self._locator(checkout_complete_ui.COMPLETE_HEADER)
