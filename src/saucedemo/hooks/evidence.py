"""Evidências do navegador anexadas ao Allure."""

from datetime import datetime

import allure
from playwright.sync_api import ConsoleMessage, Error, Page


class BrowserConsole:
    """Registra o console do navegador (mensagens e erros não tratados da página)."""

    def __init__(self, page: Page) -> None:
        self.entries: list[str] = []
        page.on("console", self._on_console)
        page.on("pageerror", self._on_page_error)

    def _on_console(self, message: ConsoleMessage) -> None:
        self._record(message.type, message.text)

    def _on_page_error(self, error: Error) -> None:
        self._record("severe", error.message)

    def _record(self, level: str, text: str) -> None:
        self.entries.append(f"{datetime.now().isoformat()} {level.upper()} {text}")

    def text(self) -> str:
        return "\n".join(self.entries) if self.entries else "(console vazio)"


def screenshot(page: Page, name: str) -> None:
    allure.attach(page.screenshot(), name, allure.attachment_type.PNG)


def failure_context(page: Page, console: BrowserConsole, scenario_name: str) -> None:
    suffix = f" - {scenario_name}"
    allure.attach(page.url, f"URL{suffix}", allure.attachment_type.URI_LIST)
    allure.attach(page.content(), f"HTML{suffix}", allure.attachment_type.HTML)
    allure.attach(console.text(), f"Console do navegador{suffix}", allure.attachment_type.TEXT)
