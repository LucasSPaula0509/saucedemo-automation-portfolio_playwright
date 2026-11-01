from saucedemo.pages.base_page import BasePage
from saucedemo.security.cookie_attributes import CookieAttributes


class SessionCookieInspector(BasePage):
    """Lê cookies do navegador atual, sem enviar requisições ao site."""

    def cookie(self, name: str) -> CookieAttributes | None:
        for cookie in self.page.context.cookies():
            if cookie.get("name") == name:
                return CookieAttributes(
                    name=name,
                    secure=bool(cookie.get("secure")),
                    http_only=bool(cookie.get("httpOnly")),
                    same_site=cookie.get("sameSite"),
                )
        return None
