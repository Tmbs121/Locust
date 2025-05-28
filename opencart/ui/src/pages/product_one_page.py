from playwright.sync_api import expect


class ProductOnePage:

    def __init__(self, page):
        self.page = page
        self._product_one_description_link = page.get_by_role("link", name="Description")
        self._add_to_comparison_list_button = page.locator("//i[contains(@class, 'fa fa-exchange')]")
        self._success_alert_message = page.locator('.alert.alert-success.alert-dismissible')
        self._product_comparison_link = page.get_by_role("link", name="product comparison")
        self._wishlist_button = page.locator("//div[@id='product-product']//div[@class='btn-group']//button[1]")
        self._wishlist_link = page.get_by_role("link", name="wish list", exact=True)
        self.show_all_laptops_and_notebooks = page.get_by_role("link", name="Show All Laptops & Notebooks")

    @property
    def product_one_description_link(self):
        return self._product_one_description_link

    def click_add_to_comparison_list_button(self):
        self._add_to_comparison_list_button.click()
        expect(self._success_alert_message).to_be_visible()

    @property
    def success_alert_message_comparison(self):
        yield self._success_alert_message

    def click_add_to_wishlist_button(self):
        self._wishlist_button.click()

    @property
    def success_alert_message_wishlist(self):
        yield self._success_alert_message

    def click_back_button_in_the_browser(self):
        self.page.go_back()

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page
