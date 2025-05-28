from ui.src.pages.product_one_page import ProductOnePage
from ui.src.pages.product_two_page import ProductTwoPage


class LaptopsNotebooksPage:

    def __init__(self, page):
        self.page = page
        self._laptops_and_notebooks_header = page.locator("//h2[normalize-space()='Laptops & Notebooks']")
        self._product_one_description = page.get_by_role("link", name="HP LP3065")
        # self._product_one_description = page.locator(f"//h4//a[contains(@href,"
        #                                              f"'http://172.23.176.159/opencart/upload/index.php?route=product"
        #                                              f"/product&path=18&product_id={self.product_id_1}')]")
        self._product_two_description = page.get_by_role("link", name="MacBook Air")

    @property
    def laptops_notebooks_header(self):
        return self._laptops_and_notebooks_header

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def click_product_one_description(self) -> ProductOnePage:
        self._product_one_description.first.click()
        return ProductOnePage(self.page)

    def click_product_two_description(self) -> ProductTwoPage:
        self._product_two_description.first.click()
        return ProductTwoPage(self.page)
