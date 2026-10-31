from saucedemo.data import paths
from saucedemo.data.rows import CartItemRow
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import cart_ui


class CartPage(LoadablePage):
    path = paths.CART
    marker_selector = cart_ui.CART_LIST

    def items(self) -> list[CartItemRow]:
        quantities = self._texts_of(cart_ui.ITEM_QUANTITIES)
        names = self._texts_of(cart_ui.ITEM_NAMES)
        prices = self._texts_of(cart_ui.ITEM_PRICES)
        return [
            CartItemRow(quantity, name, price)
            for quantity, name, price in zip(quantities, names, prices, strict=False)
        ]

    def item_names(self) -> list[str]:
        return self._texts_of(cart_ui.ITEM_NAMES)

    def remove(self, product_name: str) -> None:
        self._click(cart_ui.remove_button(product_name))

    def checkout(self) -> None:
        self._click(cart_ui.CHECKOUT)
