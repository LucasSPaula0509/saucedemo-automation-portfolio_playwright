from typing import Final

from pytest_bdd import given, then, when

from saucedemo.data.rows import CartItemRow
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.cart_page import CartPage
from saucedemo.pages.header_component import HeaderComponent
from saucedemo.pages.product_detail_page import ProductDetailPage
from saucedemo.pages.products_page import ProductsPage
from step_defs.shopper_journey import ShopperJourney
from step_defs.step_text import step, table_rows

NAME_COLUMN: Final = "produto"
QUANTITY_COLUMN: Final = "quantidade"
PRICE_COLUMN: Final = "preco"


@given(step('que o usuário "{username:string}" está na página de produtos com o carrinho vazio'))
def user_is_on_products_with_empty_cart(journey: ShopperJourney, username: str) -> None:
    journey.logged_in_with_empty_cart(username)


@given(
    step(
        'que o carrinho do usuário "{username:string}" contém os produtos '
        '"{first:string}" e "{second:string}"'
    )
)
def cart_contains_two_products(
    journey: ShopperJourney, username: str, first: str, second: str
) -> None:
    journey.with_cart(username, [first, second])


@given(
    step('que o carrinho do usuário "{username:string}" contém apenas o produto "{product:string}"')
)
def cart_contains_only_product(journey: ShopperJourney, username: str, product: str) -> None:
    journey.with_cart(username, [product])


@given(step('que o carrinho do usuário "{username:string}" contém o produto "{product:string}"'))
def cart_contains_product(journey: ShopperJourney, username: str, product: str) -> None:
    journey.with_cart(username, [product])


@given(
    step(
        'que o usuário "{username:string}" está no detalhe do produto "{product:string}" '
        "com o carrinho vazio"
    )
)
def user_is_on_detail_with_empty_cart(
    journey: ShopperJourney, products_page: ProductsPage, username: str, product: str
) -> None:
    journey.logged_in_with_empty_cart(username)
    products_page.open_detail(product)


@given(
    step(
        'que o usuário "{username:string}" adicionou o produto "{product:string}" '
        "pela página de detalhe"
    )
)
def user_added_product_from_detail(
    journey: ShopperJourney,
    products_page: ProductsPage,
    detail_page: ProductDetailPage,
    username: str,
    product: str,
) -> None:
    journey.logged_in_with_empty_cart(username)
    products_page.open_detail(product)
    detail_page.add_to_cart()


@given(
    step(
        'que o usuário "{username:string}" adicionou os produtos "{first:string}" '
        'e "{second:string}"'
    )
)
def user_added_two_products(
    journey: ShopperJourney, username: str, first: str, second: str
) -> None:
    journey.with_cart(username, [first, second])


@given(step('que o usuário "{username:string}" está no carrinho'))
def user_is_on_cart(journey: ShopperJourney, username: str) -> None:
    journey.logged_in_on_products(username)
    journey.open_cart()


@when(step('ele adiciona o produto "{product:string}" ao carrinho'))
def adds_product_to_cart(products_page: ProductsPage, product: str) -> None:
    products_page.add_to_cart(product)


@when("ele adiciona ao carrinho os produtos")
def adds_products_to_cart(products_page: ProductsPage, datatable: list[list[str]]) -> None:
    products_page.add_all_to_cart([row[NAME_COLUMN] for row in table_rows(datatable)])


@when("ele adiciona o produto ao carrinho")
def adds_current_product_to_cart(detail_page: ProductDetailPage) -> None:
    detail_page.add_to_cart()


@when(step('ele remove o produto "{product:string}" pela lista de produtos'))
def removes_product_from_list(products_page: ProductsPage, product: str) -> None:
    products_page.remove_from_cart(product)


@when("ele volta para a lista de produtos")
def goes_back_to_product_list(detail_page: ProductDetailPage) -> None:
    detail_page.back_to_products()


@when("ele acessa o carrinho")
def opens_cart(header: HeaderComponent) -> None:
    header.open_cart()


@when(step('ele remove o produto "{product:string}" no carrinho'))
def removes_product_in_cart(journey: ShopperJourney, cart_page: CartPage, product: str) -> None:
    journey.open_cart()
    cart_page.remove(product)


@when("ele recarrega a página de produtos")
def reloads_products_page(browser_navigation: BrowserNavigation) -> None:
    browser_navigation.refresh()


@then("o carrinho exibe os itens")
def cart_shows_items(cart_page: CartPage, datatable: list[list[str]]) -> None:
    expected = [
        CartItemRow(row[QUANTITY_COLUMN], row[NAME_COLUMN], row[PRICE_COLUMN])
        for row in table_rows(datatable)
    ]
    actual = cart_page.items()
    assert actual == expected, f"Itens do carrinho: {actual} != {expected}"


@then(step('o carrinho exibe apenas o produto "{product:string}"'))
def cart_shows_only_product(cart_page: CartPage, product: str) -> None:
    actual = cart_page.item_names()
    assert actual == [product], f"Produtos no carrinho: {actual} != {[product]}"
