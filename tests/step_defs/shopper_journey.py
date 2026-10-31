from dataclasses import dataclass

from saucedemo.context.scenario_context import ScenarioContext
from saucedemo.data import customer
from saucedemo.pages.cart_page import CartPage
from saucedemo.pages.checkout_info_page import CheckoutInfoPage
from saucedemo.pages.header_component import HeaderComponent
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.products_page import ProductsPage
from step_defs.assertions import expect_absent, expect_loaded, expect_text


@dataclass
class ShopperJourney:
    """Pré-condições reutilizáveis montadas pela UI, sempre a partir de um contexto novo (carrinho
    vazio). Cada etapa confirma que chegou onde deveria, para que uma falha de pré-condição não
    seja confundida com falha do comportamento sob teste.
    """

    context: ScenarioContext
    login_page: LoginPage
    products_page: ProductsPage
    header: HeaderComponent
    cart_page: CartPage
    checkout_info_page: CheckoutInfoPage

    def logged_in_on_products(self, username: str) -> None:
        self.context.username = username
        self.login_page.login_as(username)
        expect_loaded(
            self.products_page, f"Pré-condição: página de produtos após login de '{username}'"
        )

    def logged_in_with_empty_cart(self, username: str) -> None:
        self.logged_in_on_products(username)
        expect_absent(self.header.cart_badge(), "Pré-condição: carrinho vazio")

    def with_cart(self, username: str, products: list[str]) -> None:
        self.logged_in_with_empty_cart(username)
        self.products_page.add_all_to_cart(products)
        expect_text(
            self.header.cart_badge(),
            f"Pré-condição: contador do carrinho com {products}",
            str(len(products)),
        )

    def at_cart(self, username: str, products: list[str]) -> None:
        self.with_cart(username, products)
        self.open_cart()

    def open_cart(self) -> None:
        self.header.open_cart()
        expect_loaded(self.cart_page, "Pré-condição: carrinho aberto")

    def at_checkout_information(self, username: str, products: list[str]) -> None:
        self.at_cart(username, products)
        self.cart_page.checkout()
        expect_loaded(self.checkout_info_page, "Pré-condição: formulário do checkout")

    def with_checkout_information_filled(self, username: str, products: list[str]) -> None:
        self.at_checkout_information(username, products)
        self.checkout_info_page.fill(customer.DEFAULT)

    def at_checkout_overview(self, username: str, products: list[str]) -> None:
        self.with_checkout_information_filled(username, products)
        self.checkout_info_page.proceed()
