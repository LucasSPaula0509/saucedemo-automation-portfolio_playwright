from typing import Final

from saucedemo.ui import data_test

OPTIONS: Final = data_test.ending_with("-sidebar-link")
ALL_ITEMS: Final = data_test.of("inventory-sidebar-link")
ABOUT: Final = data_test.of("about-sidebar-link")
LOGOUT: Final = data_test.of("logout-sidebar-link")
RESET_APP_STATE: Final = data_test.of("reset-sidebar-link")

_OPTIONS_BY_LABEL: Final = {
    "All Items": ALL_ITEMS,
    "About": ABOUT,
    "Logout": LOGOUT,
    "Reset App State": RESET_APP_STATE,
}


def option(label: str) -> str:
    if label not in _OPTIONS_BY_LABEL:
        raise ValueError(
            f"Opção de menu sem locator mapeado: '{label}'. Mapeadas: {list(_OPTIONS_BY_LABEL)}"
        )
    return _OPTIONS_BY_LABEL[label]
