"""Fixtures de navegador e configuração (equivalente ao DriverFactory/DriverManager do Java)."""

from typing import Any

import pytest
from playwright.sync_api import BrowserContext, expect

from saucedemo.config import settings

# Navegador padrão do projeto Java: Chrome (o Chromium do Playwright é usado pelo canal "chrome").
DEFAULT_CHROMIUM_CHANNEL = "chrome"


def pytest_configure(config: pytest.Config) -> None:
    expect.set_options(timeout=settings.timeout_ms())


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """--base-url > variável BASE_URL > pyproject.toml."""
    return pytestconfig.getoption("--base-url") or settings.base_url()


@pytest.fixture(scope="session")
def browser_channel(pytestconfig: pytest.Config, browser_name: str) -> str | None:
    channel = pytestconfig.getoption("--browser-channel")
    if channel is None and browser_name == "chromium":
        return DEFAULT_CHROMIUM_CHANNEL
    return channel


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any], browser_channel: str | None
) -> dict[str, Any]:
    if browser_channel is None:
        return browser_type_launch_args
    return {**browser_type_launch_args, "channel": browser_channel}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    return {**browser_context_args, "viewport": settings.viewport()}


@pytest.fixture
def context(context: BrowserContext) -> BrowserContext:
    """Um BrowserContext novo por cenário (sessão limpa), com o timeout do projeto."""
    context.set_default_timeout(settings.timeout_ms())
    return context
