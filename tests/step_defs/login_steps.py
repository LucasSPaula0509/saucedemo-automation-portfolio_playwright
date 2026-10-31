from typing import Final

from pytest_bdd import given, then, when

from saucedemo.context.scenario_context import ScenarioContext
from saucedemo.data import menu_options
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.menu_component import MenuComponent
from step_defs.assertions import expect_loaded
from step_defs.shopper_journey import ShopperJourney
from step_defs.step_text import step

MASKED_INPUT_TYPE: Final = "password"


@given(step('que o usuário "{username:string}" está na página de login'))
def user_is_on_login_page(
    scenario_context: ScenarioContext, login_page: LoginPage, username: str
) -> None:
    scenario_context.username = username
    login_page.open()


@given("que o visitante está na página de login")
def visitor_is_on_login_page(login_page: LoginPage) -> None:
    login_page.open()


@given("que o visitante não está autenticado")
def visitor_is_not_authenticated() -> None:
    """Cada cenário começa num BrowserContext novo, sem cookies nem sessão."""


@given(step('que o usuário "{username:string}" está autenticado'))
def user_is_authenticated(journey: ShopperJourney, username: str) -> None:
    journey.logged_in_on_products(username)


@given(step('que o usuário "{username:string}" encerrou a sessão pelo menu lateral'))
def user_has_logged_out(
    journey: ShopperJourney, menu: MenuComponent, login_page: LoginPage, username: str
) -> None:
    journey.logged_in_on_products(username)
    menu.open()
    menu.select(menu_options.LOGOUT)
    expect_loaded(login_page, "Pré-condição: logout concluído")


@when(step('ele se autentica com a senha "{password:string}"'))
def authenticates_with_password(
    scenario_context: ScenarioContext, login_page: LoginPage, password: str
) -> None:
    login_page.login(scenario_context.username, password)


@when(step('ele tenta se autenticar com usuário "{username:string}" e senha "{password:string}"'))
def tries_to_authenticate(login_page: LoginPage, username: str, password: str) -> None:
    login_page.login(username, password)


@when(step('ele digita a senha "{password:string}"'))
def types_password(login_page: LoginPage, password: str) -> None:
    login_page.type_password(password)


@when(step('ele acessa diretamente a página "{path:string}"'))
def accesses_page_directly(browser_navigation: BrowserNavigation, path: str) -> None:
    browser_navigation.open_path(path)


@when("ele tenta retornar à página de produtos pelo histórico do navegador")
def goes_back_in_history(browser_navigation: BrowserNavigation) -> None:
    browser_navigation.back()


@then("o conteúdo do campo de senha é exibido mascarado")
def password_is_masked(login_page: LoginPage) -> None:
    actual = login_page.password_field_type()
    assert actual == MASKED_INPUT_TYPE, (
        f"Atributo 'type' do campo de senha: '{actual}' != '{MASKED_INPUT_TYPE}'"
    )
