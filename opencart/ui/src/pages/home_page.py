from ui.src.pages.login_page import LoginPage


class HomePage:

    def __init__(self, page):
        self.page = page
        self.my_account = page.locator("//span[normalize-space()='My Account']")
        self.login = page.locator("//a[normalize-space()='Login']")

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def navigate_to_login_page(self) -> LoginPage:
        self.my_account.click()
        self.login.click()
        return LoginPage(self.page)
