from ui.src.pages.user_profile_page import UserProfilePage


class LoginPage:
    def __init__(self, page):
        self.page = page
        self._new_customer_header = page.locator("//h2[normalize-space()='New Customer']")
        self.email_address = page.get_by_placeholder("E-Mail Address")
        self.password = page.get_by_placeholder("Password")

    @property
    def new_customer_header(self):
        return self._new_customer_header

    def wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")
        yield self.page

    def fill_email_address(self, username):
        self.email_address.click()
        self.email_address.clear()
        self.email_address.fill(username)

    def fill_password(self, password):
        self.password.click()
        self.password.clear()
        self.password.fill(password)

    def login_to_user_profile(self) -> UserProfilePage:
        self.password.press("Enter")
        return UserProfilePage(self.page)
