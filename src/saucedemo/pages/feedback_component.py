from playwright.sync_api import Locator

from saucedemo.pages.base_page import BasePage
from saucedemo.ui import message_ui


class FeedbackComponent(BasePage):
    """Mensagens exibidas ao usuário: erros (login e checkout) e confirmação do pedido."""

    def message(self) -> Locator:
        return self._locator(message_ui.ANY_FEEDBACK)
