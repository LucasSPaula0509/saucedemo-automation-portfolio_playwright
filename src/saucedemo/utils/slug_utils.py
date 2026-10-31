def to_slug(product_name: str) -> str:
    """Converte o nome do produto no sufixo usado pelo saucedemo nos atributos data-test.

    Ex.: "Sauce Labs Backpack" -> "sauce-labs-backpack";
    "Test.allTheThings() T-Shirt (Red)" -> "test.allthethings()-t-shirt-(red)".
    """
    return "-".join(product_name.strip().lower().split())
