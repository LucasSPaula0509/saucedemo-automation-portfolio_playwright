from saucedemo.pages.base_page import BasePage
from saucedemo.ui import header_ui, menu_ui


class MenuComponent(BasePage):
    """Menu lateral (hambúrguer) disponível em todas as páginas autenticadas."""

    def open(self) -> None:
        self._click(header_ui.MENU_BUTTON)

    def visible_options(self) -> list[str]:
        return self._texts_of(menu_ui.OPTIONS)

    def select(self, option: str) -> None:
        self._click(menu_ui.option(option))
