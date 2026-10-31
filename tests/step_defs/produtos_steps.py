from typing import Final

from playwright.sync_api import expect
from pytest_bdd import given, then, when

from saucedemo.pages.action_buttons_component import ActionButtonsComponent
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.menu_component import MenuComponent
from saucedemo.pages.product_detail_page import ProductDetailPage
from saucedemo.pages.products_page import ProductsPage
from step_defs.assertions import expect_loaded, expect_text
from step_defs.shopper_journey import ShopperJourney
from step_defs.step_text import step, table_rows

NAME_COLUMN: Final = "produto"
PRICE_COLUMN: Final = "preco"
OPTION_COLUMN: Final = "opcao"


@given(step('que o usuário "{username:string}" está na página de produtos'))
def user_is_on_products_page(journey: ShopperJourney, username: str) -> None:
    journey.logged_in_on_products(username)


@given(step('que o usuário "{username:string}" ordenou os produtos por "{sort_option:string}"'))
def user_has_sorted_products(
    journey: ShopperJourney, products_page: ProductsPage, username: str, sort_option: str
) -> None:
    journey.logged_in_on_products(username)
    products_page.sort_by(sort_option)


@given(step('que o usuário "{username:string}" está no detalhe do produto "{product:string}"'))
def user_is_on_product_detail(
    journey: ShopperJourney, products_page: ProductsPage, username: str, product: str
) -> None:
    journey.logged_in_on_products(username)
    products_page.open_detail(product)


@given(step('que o usuário "{username:string}" está com o menu lateral aberto'))
def user_has_side_menu_open(journey: ShopperJourney, menu: MenuComponent, username: str) -> None:
    journey.logged_in_on_products(username)
    menu.open()


@when("ele acessa a página de produtos")
def accesses_products_page(products_page: ProductsPage) -> None:
    products_page.open()


@when(step('ele ordena os produtos por "{sort_option:string}"'))
def sorts_products(products_page: ProductsPage, sort_option: str) -> None:
    products_page.sort_by(sort_option)


@when(step('ele abre o detalhe de um produto e volta para a lista com "{back_label:string}"'))
def opens_any_detail_and_goes_back(
    products_page: ProductsPage, action_buttons: ActionButtonsComponent, back_label: str
) -> None:
    products_page.open_detail(products_page.product_names()[0])
    action_buttons.press(back_label)


@when(step('ele abre o detalhe do produto "{product:string}"'))
def opens_product_detail(products_page: ProductsPage, product: str) -> None:
    products_page.open_detail(product)


@when("ele abre o menu lateral")
def opens_side_menu(menu: MenuComponent) -> None:
    menu.open()


@then("os produtos são exibidos com nome e preço")
def products_are_displayed_with_name_and_price(
    products_page: ProductsPage, datatable: list[list[str]]
) -> None:
    _assert_product_list_matches(products_page, datatable)


@then("os produtos são exibidos na ordem")
def products_are_displayed_in_order(
    products_page: ProductsPage, datatable: list[list[str]]
) -> None:
    _assert_product_list_matches(products_page, datatable)


@then(step('a ordenação "{sort_option:string}" está selecionada'))
def sort_option_is_selected(products_page: ProductsPage, sort_option: str) -> None:
    expect_text(products_page.active_sort(), "Ordenação selecionada", sort_option)


@then(step('o detalhe exibe o nome "{name:string}" com o preço "{price:string}"'))
def detail_shows_name_and_price(detail_page: ProductDetailPage, name: str, price: str) -> None:
    expect_loaded(detail_page, "Página de detalhe carregada")
    expect(detail_page.name(), "Nome no detalhe").to_have_text(name)
    expect(detail_page.price(), "Preço no detalhe").to_have_text(price)


@then("as opções do menu são exibidas")
def side_menu_options_are_displayed(menu: MenuComponent, datatable: list[list[str]]) -> None:
    expected = [row[OPTION_COLUMN] for row in table_rows(datatable)]
    actual = menu.visible_options()
    assert actual == expected, f"Opções do menu lateral: {actual} != {expected}"


@then(step('o site "{url:string}" é exibido'))
def external_site_is_displayed(browser_navigation: BrowserNavigation, url: str) -> None:
    actual = browser_navigation.external_site_url()
    assert actual == url, f"URL do site externo: '{actual}' != '{url}'"


def _assert_product_list_matches(products_page: ProductsPage, datatable: list[list[str]]) -> None:
    """Compara a lista completa e ordenada. A coluna de preço só é verificada quando presente na
    tabela do cenário. Todas as divergências são reportadas de uma vez.
    """
    rows = table_rows(datatable)
    check_prices = PRICE_COLUMN in datatable[0]
    expected = [(row[NAME_COLUMN], row[PRICE_COLUMN] if check_prices else None) for row in rows]
    actual = [
        (product.name, product.price if check_prices else None)
        for product in products_page.products()
    ]
    assert actual == expected, f"Produtos exibidos (nome, preço) na ordem: {actual} != {expected}"
