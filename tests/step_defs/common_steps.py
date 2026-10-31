"""Passos usados por mais de uma funcionalidade."""

from pytest_bdd import then, when

from saucedemo.data import page_titles
from saucedemo.pages.action_buttons_component import ActionButtonsComponent
from saucedemo.pages.feedback_component import FeedbackComponent
from saucedemo.pages.header_component import HeaderComponent
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.menu_component import MenuComponent
from saucedemo.pages.products_page import ProductsPage
from step_defs.assertions import expect_absent, expect_loaded, expect_text
from step_defs.step_text import step


@when(step('ele aciona "{label:string}"'))
def press_button(action_buttons: ActionButtonsComponent, label: str) -> None:
    action_buttons.press(label)


@when(step('ele seleciona a opção "{option:string}" no menu lateral'))
def select_side_menu_option(menu: MenuComponent, option: str) -> None:
    menu.open()
    menu.select(option)


@when(step('ele seleciona a opção "{option:string}"'))
def select_open_menu_option(menu: MenuComponent, option: str) -> None:
    menu.select(option)


@then(step('a mensagem "{message:string}" é exibida'))
def message_is_displayed(feedback: FeedbackComponent, message: str) -> None:
    expect_text(feedback.message(), "Mensagem exibida ao usuário", message)


@then("a página de produtos é exibida")
def products_page_is_displayed(products_page: ProductsPage, header: HeaderComponent) -> None:
    expect_loaded(products_page, "Página de produtos carregada")
    expect_text(header.page_title(), "Título da página", page_titles.PRODUCTS)


@then("a página de login é exibida")
def login_page_is_displayed(login_page: LoginPage) -> None:
    expect_loaded(login_page, "Página de login carregada")


@then(step('o contador do carrinho exibe "{count:string}"'))
def cart_badge_shows(header: HeaderComponent, count: str) -> None:
    expect_text(header.cart_badge(), "Contador do carrinho", count)


@then("o contador do carrinho não é exibido")
def cart_badge_is_not_displayed(header: HeaderComponent) -> None:
    expect_absent(header.cart_badge(), "Contador do carrinho ausente")


@then(step('o botão do produto "{product:string}" exibe "{label:string}"'))
def product_button_shows(products_page: ProductsPage, product: str, label: str) -> None:
    expect_text(products_page.product_button(product), f"Botão do produto '{product}'", label)
