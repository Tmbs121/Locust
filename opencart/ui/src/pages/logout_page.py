class LogoutPage:

    def __init__(self, page):
        self.page = page
        self._account_logout_header = page.locator("//h1[normalize-space()='Account Logout']")

    @property
    def account_logout_header(self):
        return self._account_logout_header

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page
