from typing import Final

import allure
from pytest_bdd import given, then, when

from saucedemo.data import page_titles, paths, products
from saucedemo.data.customer import Customer
from saucedemo.pages.action_buttons_component import ActionButtonsComponent
from saucedemo.pages.browser_navigation import BrowserNavigation
from saucedemo.pages.cart_page import CartPage
from saucedemo.pages.checkout_info_page import CheckoutInfoPage
from saucedemo.pages.checkout_overview_page import CheckoutOverviewPage
from saucedemo.pages.header_component import HeaderComponent
from saucedemo.utils import money
from saucedemo.utils.order_totals import OrderTotals
from step_defs.assertions import expect_loaded, expect_text
from step_defs.shopper_journey import ShopperJourney
from step_defs.step_text import step, table_rows

DEFAULT_PRODUCTS: Final = [products.BACKPACK]
FIELD_COLUMN: Final = "campo"
VALUE_COLUMN: Final = "valor"


@given(step('que o usuário "{username:string}" está no formulário de informações do checkout'))
def user_is_on_checkout_information(journey: ShopperJourney, username: str) -> None:
    journey.at_checkout_information(username, DEFAULT_PRODUCTS)


@given(
    step(
        'que o usuário "{username:string}" preencheu os dados do checkout com o produto '
        '"{product:string}" no carrinho'
    )
)
def user_filled_checkout_with_product(journey: ShopperJourney, username: str, product: str) -> None:
    journey.with_checkout_information_filled(username, [product])


@given(
    step(
        'que o usuário "{username:string}" preencheu os dados do checkout com os produtos '
        '"{product_list:string}" no carrinho'
    )
)
def user_filled_checkout_with_products(
    journey: ShopperJourney, username: str, product_list: str
) -> None:
    journey.with_checkout_information_filled(username, _split_products(product_list))


@given(step('que o usuário "{username:string}" está no resumo do pedido'))
def user_is_on_overview(journey: ShopperJourney, username: str) -> None:
    journey.at_checkout_overview(username, DEFAULT_PRODUCTS)


@given(
    step(
        'que o usuário "{username:string}" está no resumo do pedido '
        'com o produto "{product:string}"'
    )
)
def user_is_on_overview_with_product(journey: ShopperJourney, username: str, product: str) -> None:
    journey.at_checkout_overview(username, [product])


@given(step('que o usuário "{username:string}" está na página "{page_title:string}"'))
def user_is_on_checkout_page(
    journey: ShopperJourney,
    overview_page: CheckoutOverviewPage,
    header: HeaderComponent,
    username: str,
    page_title: str,
) -> None:
    journey.at_checkout_overview(username, DEFAULT_PRODUCTS)
    overview_page.finish()
    expect_text(header.page_title(), "Pré-condição: página atual", page_title)


@given(step('que o usuário "{username:string}" está no carrinho vazio'))
def user_is_on_empty_cart(journey: ShopperJourney, username: str) -> None:
    journey.logged_in_with_empty_cart(username)
    journey.open_cart()


@when(step('ele aciona "{label:string}" no carrinho'))
def presses_button_on_cart(
    journey: ShopperJourney, action_buttons: ActionButtonsComponent, label: str
) -> None:
    journey.open_cart()
    action_buttons.press(label)


@when(
    step(
        'ele continua informando nome "{first_name:string}", sobrenome "{last_name:string}" '
        'e CEP "{postal_code:string}"'
    )
)
def continues_with_customer_data(
    checkout_info_page: CheckoutInfoPage, first_name: str, last_name: str, postal_code: str
) -> None:
    checkout_info_page.submit(Customer(first_name, last_name, postal_code))


@when("ele visualiza o resumo do pedido")
def views_order_overview(checkout_info_page: CheckoutInfoPage) -> None:
    checkout_info_page.proceed()


@then(step('o formulário "{title:string}" é exibido'))
def checkout_form_is_displayed(
    checkout_info_page: CheckoutInfoPage, header: HeaderComponent, title: str
) -> None:
    expect_loaded(checkout_info_page, "Formulário do checkout carregado")
    expect_text(header.page_title(), "Título da página", title)


@then(step('o resumo "{title:string}" é exibido'))
def overview_is_displayed(
    overview_page: CheckoutOverviewPage, header: HeaderComponent, title: str
) -> None:
    expect_loaded(overview_page, "Resumo do pedido carregado")
    expect_text(header.page_title(), "Título da página", title)


@then("o resumo exibe as informações")
def overview_shows_information(
    overview_page: CheckoutOverviewPage, datatable: list[list[str]]
) -> None:
    info = overview_page.summary_info()
    expected = {row[FIELD_COLUMN]: row[VALUE_COLUMN] for row in table_rows(datatable)}
    actual = {field: info.get(field) for field in expected}
    assert actual == expected, f"Resumo do pedido: {actual} != {expected}"


@then(step('o resumo exibe "{subtotal:string}", "{tax:string}" e "{total:string}"'))
def overview_shows_totals(
    overview_page: CheckoutOverviewPage, subtotal: str, tax: str, total: str
) -> None:
    rule = OrderTotals.from_item_prices(overview_page.item_prices())
    allure.attach(rule.describe(), "Cálculo do pedido", allure.attachment_type.TEXT)
    shown_subtotal, shown_tax, shown_total = (
        overview_page.subtotal(),
        overview_page.tax(),
        overview_page.total(),
    )
    actual = {
        "Subtotal exibido": shown_subtotal,
        "Imposto exibido": shown_tax,
        "Total exibido": shown_total,
        "Subtotal pela regra": money.format_amount(money.parse(shown_subtotal)),
        "Imposto pela regra de 8%": money.format_amount(money.parse(shown_tax)),
        "Total pela regra": money.format_amount(money.parse(shown_total)),
    }
    expected = {
        "Subtotal exibido": subtotal,
        "Imposto exibido": tax,
        "Total exibido": total,
        "Subtotal pela regra": money.format_amount(rule.subtotal),
        "Imposto pela regra de 8%": money.format_amount(rule.tax),
        "Total pela regra": money.format_amount(rule.total),
    }
    assert actual == expected, f"Resumo do pedido (exibido x esperado e regra): {actual}"


@then("o carrinho é exibido")
def cart_is_displayed(cart_page: CartPage, header: HeaderComponent) -> None:
    expect_loaded(cart_page, "Carrinho carregado")
    expect_text(header.page_title(), "Título da página", page_titles.CART)


@then("o checkout não é iniciado")
def checkout_is_not_started(browser_navigation: BrowserNavigation) -> None:
    actual = browser_navigation.path()
    assert actual != paths.CHECKOUT_STEP_ONE, (
        f"Página após acionar Checkout com o carrinho vazio: '{actual}'"
    )


def _split_products(product_list: str) -> list[str]:
    return [product.strip() for product in product_list.split(",")]
