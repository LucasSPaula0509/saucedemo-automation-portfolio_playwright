from typing import Any
from urllib.parse import urlparse

from playwright.sync_api import Locator, Page


class BasePage:
    """Ações e leituras de estado reutilizadas por todos os Page Objects.

    As esperas são as automáticas do Playwright (auto-wait até o timeout padrão do contexto);
    por isso não existem métodos de espera. As pages devolvem Locator (para os steps validarem
    com expect, que repete a leitura) ou estado já lido (texto, lista).
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def _open(self, path: str) -> None:
        self.page.goto(path)

    def _locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def _click(self, selector: str) -> None:
        self._locator(selector).click()

    def _type(self, selector: str, text: str) -> None:
        """Limpa o campo e digita o texto. Texto vazio mantém o campo vazio."""
        field = self._locator(selector)
        field.clear()
        if text:
            field.fill(text)

    def _select_by_visible_text(self, selector: str, option: str) -> None:
        self._locator(selector).select_option(label=option)

    def _text_of(self, selector: str) -> str:
        return self._locator(selector).inner_text().strip()

    def _texts_of(self, selector: str) -> list[str]:
        """Aguarda a lista aparecer e devolve o texto de todos os elementos."""
        elements = self._locator(selector)
        elements.first.wait_for()
        return [text.strip() for text in elements.all_inner_texts()]

    def _attribute_of(self, selector: str, attribute: str) -> str | None:
        return self._locator(selector).get_attribute(attribute)

    def _evaluate(self, script: str) -> Any:  # noqa: ANN401 - resultado livre do JavaScript
        return self.page.evaluate(script)

    def current_url(self) -> str:
        return self.page.url

    def current_path(self) -> str:
        return urlparse(self.page.url).path


class LoadablePage(BasePage):
    """Página que sabe dizer se está carregada: um elemento característico e o caminho da URL.

    Os steps validam os dois (as pages não fazem asserções).
    """

    path: str
    marker_selector: str

    def marker(self) -> Locator:
        return self._locator(self.marker_selector)
