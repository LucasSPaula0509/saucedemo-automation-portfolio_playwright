from saucedemo.data import paths
from saucedemo.data.customer import Customer
from saucedemo.pages.base_page import LoadablePage
from saucedemo.ui import checkout_info_ui


class CheckoutInfoPage(LoadablePage):
    path = paths.CHECKOUT_STEP_ONE
    marker_selector = checkout_info_ui.FIRST_NAME

    def fill(self, customer: Customer) -> None:
        self._type(checkout_info_ui.FIRST_NAME, customer.first_name)
        self._type(checkout_info_ui.LAST_NAME, customer.last_name)
        self._type(checkout_info_ui.POSTAL_CODE, customer.postal_code)

    def proceed(self) -> None:
        self._click(checkout_info_ui.CONTINUE)

    def submit(self, customer: Customer) -> None:
        self.fill(customer)
        self.proceed()
