from saucedemo.pages.base_page import BasePage
from saucedemo.ui import action_buttons_ui


class ActionButtonsComponent(BasePage):
    """Aciona botões de navegação pelo rótulo visível (ex.: "Finish", "Cancel", "Back Home")."""

    def press(self, label: str) -> None:
        self._click(action_buttons_ui.by_label(label))
