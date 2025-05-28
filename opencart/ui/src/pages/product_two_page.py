from ui.src.pages.compare_list_page import CompareListPage
from playwright.sync_api import expect


class ProductTwoPage:

    def __init__(self, page):
        self.page = page
        self._product_two_description_link = page.get_by_role("link", name="Description")
        self._add_to_comparison_list_button = page.locator("//i[contains(@class, 'fa fa-exchange')]")
        self._success_alert_message = page.locator("//div[@class='alert alert-success alert-dismissible']")
        self._product_comparison_link = page.get_by_role("link", name="product comparison")

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    @property
    def product_two_description_link(self):
        return self._product_two_description_link

    def click_add_to_comparison_list_button(self):
        self._add_to_comparison_list_button.click()
        expect(self._success_alert_message).to_be_visible()

    @property
    def success_alert_message_comparison(self):
        yield self._success_alert_message
        yield self._product_comparison_link

    def click_product_comparison_link(self) -> CompareListPage:
        self._product_comparison_link.click()
        return CompareListPage(self.page)
