from typing import Final

from saucedemo.ui import data_test
from saucedemo.utils.slug_utils import to_slug

CART_LIST: Final = data_test.of("cart-list")
ITEM_QUANTITIES: Final = data_test.of("item-quantity")
ITEM_NAMES: Final = data_test.of("inventory-item-name")
ITEM_PRICES: Final = data_test.of("inventory-item-price")
CONTINUE_SHOPPING: Final = data_test.of("continue-shopping")
CHECKOUT: Final = data_test.of("checkout")


def remove_button(product_name: str) -> str:
    return data_test.of(f"remove-{to_slug(product_name)}")
