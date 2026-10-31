from urllib.parse import urlparse

from saucedemo.config import settings
from saucedemo.pages.base_page import BasePage


class BrowserNavigation(BasePage):
    """Ações do próprio navegador: acesso direto por URL, histórico e recarregamento."""

    def open_path(self, path: str) -> None:
        self._open(path)

    def refresh(self) -> None:
        self.page.reload()

    def back(self) -> None:
        self.page.go_back()

    def open_over_http(self) -> None:
        """Acessa a raiz do site por HTTP (sem TLS), para verificar o redirecionamento."""
        self.page.goto(f"http://{urlparse(settings.base_url()).netloc}/")

    def url(self) -> str:
        return self.current_url()

    def path(self) -> str:
        return self.current_path()

    def external_site_url(self) -> str:
        """URL atual depois que a navegação saiu do domínio da aplicação (links externos)."""
        host = urlparse(settings.base_url()).netloc
        self.page.wait_for_url(lambda url: host not in url)
        return self.current_url()
