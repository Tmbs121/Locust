import random
import re

from playwright.sync_api import Page, expect

import parse_user_credentials_from_csv
from parse_user_credentials_from_csv import LoginWithCreds


def test_go_to_home_page(page: Page):
    page.goto("http://172.23.176.159/opencart/upload")

    # Assertion: Expect a title "to contain" a certain substring
    expect(page).to_have_title(re.compile("Your Store"))


def test_navigate_to_login_form_and_proceed(page: Page, self=LoginWithCreds):
    page.goto("http://172.23.176.159/opencart/upload/index.php?route=account/login")
    expect(page.get_by_role("heading", name="Returning Customer")).to_be_visible()

    user_credentials = parse_user_credentials_from_csv.LoginWithCreds.read_creds_from_csv(self)
    credentials_pair = random.choice(list(user_credentials.items()))
    username = credentials_pair[0]
    password = credentials_pair[1]

    page.get_by_placeholder("E-Mail Address").click()
    page.get_by_placeholder("E-Mail Address").fill(username)
    page.get_by_placeholder("E-Mail Address").press("Tab")

    page.get_by_placeholder("Password").fill(password)
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_load_state("networkidle")
    expect(page.locator("#content").get_by_role("heading", name="My Account")).to_be_visible()

    page.get_by_role("link", name="Laptops & Notebooks").hover()
    page.get_by_text('Show All Laptops & Notebooks').click()
    expect(page.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()

    page.get_by_role("link", name="HP LP3065").first.click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()

    page.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(page.locator("#product-product div").filter(has_text="Success: You have added HP")
           .locator("i")).to_be_visible()

    page.go_back(wait_until="domcontentloaded")
    expect(page.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()

    page.get_by_role("link", name="MacBook Air").first.click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()

    page.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(page.locator("#product-product div").filter(has_text="Success: You have added MacBook Air")
           .locator("i")).to_be_visible()

    page.get_by_role("link", name="product comparison").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page.get_by_role("heading", name="Product Comparison")).to_be_visible()

    page.get_by_role("link", name="Remove").first.click()
    expect(page.get_by_text("Success: You have modified")).to_be_visible()

    page.get_by_role("link", name="MacBook Air").click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()

    page.locator("//div[@id='product-product']//div[@class='btn-group']//button[1]").click()
    expect(page.get_by_text("Success: You have added MacBook Air")).to_be_visible()

    page.locator("//span[normalize-space()='My Account']").click()
    page.get_by_role("link", name="Logout").click()
    expect(page.get_by_role("heading", name="Account Logout")).to_be_visible()
