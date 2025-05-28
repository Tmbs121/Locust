from playwright.sync_api import expect

from ui.src.pages.shopping_cart_page import ShoppingCartPage


class CompareListPage:

    def __init__(self, page):
        self.page = page
        self._remove_button = page.get_by_role("link", name="Remove").first
        self._product_comparison_header = page.locator("//h1[normalize-space()='Product Comparison']")
        self._add_to_cart_button = page.locator("//input[@value='Add to Cart']")
        self._success_alert_message_comp_list_modified = page.locator(
            "//div[@class='alert alert-success alert-dismissible']")
        self._shopping_cart_link = page.locator("//a[normalize-space()='shopping cart']")

    def click_remove_button(self):
        self._remove_button.click()

    @property
    def product_comparison_header(self):
        return self._product_comparison_header

    @property
    def success_alert_message_comp_list_modified(self):
        return self._success_alert_message_comp_list_modified

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def click_add_cart_button(self):
        self._add_to_cart_button.click()
        expect(self._shopping_cart_link).to_be_visible()

    def click_shopping_cart_link(self) -> ShoppingCartPage:
        self._shopping_cart_link.scroll_into_view_if_needed()
        self._shopping_cart_link.click()
        return ShoppingCartPage(self.page)
