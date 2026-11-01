from saucedemo.pages.base_page import BasePage


class SecurityHeadersInspector(BasePage):
    """Lê os cabeçalhos da resposta do documento principal da própria navegação (page.goto), sem
    nenhuma requisição extra ou alterada.

    Restrito a Chrome/Edge para manter o mesmo escopo do projeto Java, que lia os cabeçalhos via
    Chrome DevTools Protocol.
    """

    def is_supported(self) -> bool:
        return self.browser_name() == "chromium"

    def browser_name(self) -> str:
        browser = self.page.context.browser
        return browser.browser_type.name if browser else "desconhecido"

    def document_response_headers(self, path: str) -> dict[str, str]:
        """Navega até path e devolve os cabeçalhos da resposta (nomes em minúsculas)."""
        response = self.page.goto(path)
        if response is None:
            raise RuntimeError(f"Resposta do documento não capturada: {path}")
        return dict(sorted(response.all_headers().items()))
