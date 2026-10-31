from playwright.sync_api import Locator

from saucedemo.data import paths
from saucedemo.data.rows import ProductRow
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import products_ui


class ProductsPage(LoadablePage):
    path = paths.INVENTORY
    marker_selector = products_ui.INVENTORY_LIST

    def open(self) -> None:
        self._open(paths.INVENTORY)

    def products(self) -> list[ProductRow]:
        names = self._texts_of(products_ui.ITEM_NAMES)
        prices = self._texts_of(products_ui.ITEM_PRICES)
        return [ProductRow(name, price) for name, price in zip(names, prices, strict=False)]

    def product_names(self) -> list[str]:
        return self._texts_of(products_ui.ITEM_NAMES)

    def sort_by(self, option: str) -> None:
        self._select_by_visible_text(products_ui.SORT_SELECT, option)

    def active_sort(self) -> Locator:
        return self._locator(products_ui.ACTIVE_SORT)

    def add_to_cart(self, product_name: str) -> None:
        self._click(products_ui.add_to_cart_button(product_name))

    def add_all_to_cart(self, product_names: list[str]) -> None:
        for product_name in product_names:
            self.add_to_cart(product_name)

    def remove_from_cart(self, product_name: str) -> None:
        self._click(products_ui.remove_button(product_name))

    def product_button(self, product_name: str) -> Locator:
        return self._locator(products_ui.product_button(product_name))

    def open_detail(self, product_name: str) -> None:
        self._click(products_ui.product_title(product_name))
