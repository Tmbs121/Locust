from ui.src.pages.laptops_notebooks_page import LaptopsNotebooksPage


class UserProfilePage:

    def __init__(self, page):
        self.page = page
        self._my_account_header = page.locator("//h2[normalize-space()='My Account']")
        self.laptops_and_notebooks = page.get_by_role("link", name="Laptops & Notebooks", exact=True)
        self.show_all_laptops_and_notebooks = page.get_by_role("link", name="Show All Laptops & Notebooks")

    @property
    def my_account_header(self):
        return self._my_account_header

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def hover_over_laptops_and_notebooks(self):
        self.laptops_and_notebooks.hover()

    def click_all_laptops_and_notebooks_section(self) -> LaptopsNotebooksPage:
        self.show_all_laptops_and_notebooks.click()
        return LaptopsNotebooksPage(self.page)
