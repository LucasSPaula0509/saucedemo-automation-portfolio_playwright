"""Fixtures do navegador, das pages e do estado do cenário, e ciclo de vida dos cenários."""

import logging
from collections.abc import Generator
from typing import Any

import pytest
from playwright.sync_api import BrowserContext, Page, expect
from pytest_bdd.parser import Feature, Scenario

# Os steps ficam em step_defs/; importá-los aqui os registra para todas as features.
from step_defs.carrinho_steps import *  # noqa: F403
from step_defs.checkout_steps import *  # noqa: F403
from step_defs.common_steps import *  # noqa: F403
from step_defs.login_steps import *  # noqa: F403
from step_defs.produtos_steps import *  # noqa: F403
from step_defs.shopper_journey import ShopperJourney

from saucedemo.config import settings
from saucedemo.context.scenario_context import ScenarioContext
from saucedemo.pages.action_buttons_component import ActionButtonsComponent
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.cart_page import CartPage
from saucedemo.pages.checkout_complete_page import CheckoutCompletePage
from saucedemo.pages.checkout_info_page import CheckoutInfoPage
from saucedemo.pages.checkout_overview_page import CheckoutOverviewPage
from saucedemo.pages.feedback_component import FeedbackComponent
from saucedemo.pages.header_component import HeaderComponent
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.menu_component import MenuComponent
from saucedemo.pages.product_detail_page import ProductDetailPage
from saucedemo.pages.products_page import ProductsPage

LOG = logging.getLogger("saucedemo.hooks")

# Navegador padrão do projeto Java: Chrome (o Chromium do Playwright é usado pelo canal "chrome").
DEFAULT_CHROMIUM_CHANNEL = "chrome"


def pytest_configure(config: pytest.Config) -> None:
    expect.set_options(timeout=settings.timeout_ms())


# --- Navegador -----------------------------------------------------------------------------


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


# --- Estado do cenário e pages ---------------------------------------------------------------


@pytest.fixture
def scenario_context() -> ScenarioContext:
    return ScenarioContext()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def detail_page(page: Page) -> ProductDetailPage:
    return ProductDetailPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def header(page: Page) -> HeaderComponent:
    return HeaderComponent(page)


@pytest.fixture
def menu(page: Page) -> MenuComponent:
    return MenuComponent(page)


@pytest.fixture
def feedback(page: Page) -> FeedbackComponent:
    return FeedbackComponent(page)


@pytest.fixture
def action_buttons(page: Page) -> ActionButtonsComponent:
    return ActionButtonsComponent(page)


@pytest.fixture
def browser_navigation(page: Page) -> BrowserNavigation:
    return BrowserNavigation(page)


@pytest.fixture
def journey(
    scenario_context: ScenarioContext,
    login_page: LoginPage,
    products_page: ProductsPage,
    header: HeaderComponent,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
) -> ShopperJourney:
    return ShopperJourney(
        scenario_context, login_page, products_page, header, cart_page, checkout_info_page
    )


# --- Ciclo de vida -------------------------------------------------------------------------


def pytest_bdd_before_scenario(
    request: pytest.FixtureRequest, feature: Feature, scenario: Scenario
) -> None:
    LOG.info("Iniciando cenário: %s", scenario.name)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    report = yield
    if report.when == "call" or (report.when == "setup" and report.skipped):
        LOG.info("Cenário finalizado [%s]: %s", report.outcome.upper(), item.name)
    return report
