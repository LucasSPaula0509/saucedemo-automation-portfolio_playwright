from saucedemo.data import passwords, paths
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import login_ui


class LoginPage(LoadablePage):
    path = paths.LOGIN
    marker_selector = login_ui.LOGIN_BUTTON

    def open(self) -> None:
        self._open(paths.LOGIN)

    def login(self, username: str, password: str) -> None:
        self._type(login_ui.USERNAME, username)
        self._type(login_ui.PASSWORD, password)
        self._click(login_ui.LOGIN_BUTTON)

    def login_as(self, username: str) -> None:
        """Atalho reutilizável para pré-condições: abre a tela de login e autentica pela UI."""
        self.open()
        self.login(username, passwords.DEFAULT)

    def type_password(self, password: str) -> None:
        self._type(login_ui.PASSWORD, password)

    def password_field_type(self) -> str | None:
        return self._attribute_of(login_ui.PASSWORD, "type")

    def password_field_autocomplete(self) -> str | None:
        return self._attribute_of(login_ui.PASSWORD, "autocomplete")
