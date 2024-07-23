import re
from playwright.sync_api import Page, expect


def test_Compare_Products_Add_to_Wishlist(page: Page):
    page.goto("http://172.23.176.159/opencart/upload")
    
    # Assertion: Expect a title "to contain" a certain substring
    expect(page).to_have_title(re.compile("Your Store"))
