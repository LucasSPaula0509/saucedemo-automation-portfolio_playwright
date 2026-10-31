from playwright.sync_api import Locator

from saucedemo.data import paths
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import product_detail_ui


class ProductDetailPage(LoadablePage):
    path = paths.PRODUCT_DETAIL
    marker_selector = product_detail_ui.CONTAINER

    def name(self) -> Locator:
        return self._locator(product_detail_ui.NAME)

    def price(self) -> Locator:
        return self._locator(product_detail_ui.PRICE)

    def add_to_cart(self) -> None:
        self._click(product_detail_ui.ADD_TO_CART)

    def back_to_products(self) -> None:
        self._click(product_detail_ui.BACK_TO_PRODUCTS)
