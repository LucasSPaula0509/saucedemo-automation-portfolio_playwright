from typing import Final

from saucedemo.ui import data_test
from saucedemo.utils.slug_utils import to_slug

INVENTORY_LIST: Final = data_test.of("inventory-list")
ITEM_NAMES: Final = data_test.of("inventory-item-name")
ITEM_PRICES: Final = data_test.of("inventory-item-price")
SORT_SELECT: Final = data_test.of("product-sort-container")
ACTIVE_SORT: Final = data_test.of("active-option")


def add_to_cart_button(product_name: str) -> str:
    return data_test.of(f"add-to-cart-{to_slug(product_name)}")


def remove_button(product_name: str) -> str:
    return data_test.of(f"remove-{to_slug(product_name)}")


def product_button(product_name: str) -> str:
    """Botão do produto, esteja ele no estado "Add to cart" ou "Remove"."""
    return f"button[data-test$='-{to_slug(product_name)}']"


def product_title(product_name: str) -> str:
    return f"xpath=//div[@data-test='inventory-item-name' and normalize-space()='{product_name}']"
