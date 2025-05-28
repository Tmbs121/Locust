from ui.src.pages.logout_page import LogoutPage
from playwright.sync_api import expect


class ShoppingCartPage:

    def __init__(self, page):
        self.page = page
        self._shopping_cart_header = page.locator("//h1[contains(text(),'Shopping Cart')]")
        self.my_account = page.locator("//span[normalize-space()='My Account']")
        self.logout = page.locator("//a[normalize-space()='Logout']")
        self._change_quantity_input_field = page.locator("//input[@class='form-control'][@size='1']")
        self._update_shopping_cart_button = page.locator("//i[@class='fa fa-refresh']")
        self._success_shopping_cart_modified_alert = page.locator("//div[@class='alert alert-success "
                                                                  "alert-dismissible']")
        self._empty_shopping_cart_button = page.locator("//button[@class='btn btn-danger']")
        self._continue_button_once_shopping_cart_was_cleared = page.locator("//a[@class='btn btn-primary']")

    @property
    def shopping_cart_header(self):
        return self._shopping_cart_header

    def log_out_of_user_profile(self) -> LogoutPage:
        self.my_account.scroll_into_view_if_needed()
        self.my_account.click()
        self.logout.click()
        return LogoutPage(self.page)

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def change_quantity_of_products(self, quantity):
        self._change_quantity_input_field.click()
        self._change_quantity_input_field.clear()
        self._change_quantity_input_field.fill(quantity)

    def update_shopping_cart(self):
        self._update_shopping_cart_button.click()
        expect(self._success_shopping_cart_modified_alert).to_be_visible()

    def empty_shopping_cart(self):
        delete_item_from_cart_buttons = self._empty_shopping_cart_button.all()
        for button in delete_item_from_cart_buttons:
            button.click()
        self.page.wait_for_timeout(2000)
        expect(self._continue_button_once_shopping_cart_was_cleared).to_be_visible()
