import re
from playwright.sync_api import Page, expect


def test_Compare_Products_Add_to_Wishlist(page: Page):
    page.goto("http://172.23.176.159/opencart/upload")
    
    # Assertion: Expect a title "to contain" a certain substring
    expect(page).to_have_title(re.compile("Your Store"))
    
def nagivate_to_user_login_form(userLoginFormPage: Page):
    userLoginFormPage.goto("http://172.23.176.159/opencart/upload/index.php?route=account/login")
    expect(userLoginFormPage.get_by_role("heading", name="Returning Customer")).to_be_visible()
    
    USER_CREDENTIALS = Parse_User_Credentials_From_CSV.LoginWithCredsFromCSV.readCredsFromCSV()
    credentials_pair = random.choice(USER_CREDENTIALS)
    username = credentials_pair[0]
    password = credentials_pair[1]
    
    userLoginFormPage.get_by_placeholder("E-Mail Address").click()
    userLoginFormPage.get_by_placeholder("E-Mail Address").fill(username)
    userLoginFormPage.get_by_placeholder("E-Mail Address").press("Tab")
    
    userLoginFormPage.get_by_placeholder("Password").fill(password)
    userLoginFormPage.get_by_placeholder("Password").press("Enter")
    userLoginFormPage.wait_for_load_state("networkidle")
    expect(userLoginFormPage.locator("#content").get_by_role("heading", name="My Account")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="Laptops & Notebooks").hover()
    userLoginFormPage.get_by_text('Show All Laptops & Notebooks').click()
    expect(userLoginFormPage.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="HP LP3065").first.click()
    expect(userLoginFormPage.get_by_role("link", name="Description")).to_be_visible()
    
    
    userLoginFormPage.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(userLoginFormPage.locator("#product-product div").filter(has_text="Success: You have added HP")
           .locator("i")).to_be_visible()
    
    userLoginFormPage.go_back(wait_until="domcontentloaded")
    expect(userLoginFormPage.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="MacBook Air").first.click()
    expect(userLoginFormPage.get_by_role("link", name="Description")).to_be_visible()
    
    userLoginFormPage.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(userLoginFormPage.locator("#product-product div").filter(has_text="Success: You have added MacBook Air")
           .locator("i")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="product comparison").click()
    userLoginFormPage.wait_for_load_state("domcontentloaded")
    expect(userLoginFormPage.get_by_role("heading", name="Product Comparison")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="Remove").first.click()
    expect(userLoginFormPage.get_by_text("Success: You have modified")).to_be_visible()
    
    userLoginFormPage.get_by_role("link", name="MacBook Air").click()
    expect(userLoginFormPage.get_by_role("link", name="Description")).to_be_visible()
    
    userLoginFormPage.locator("//div[@id='product-product']//div[@class='btn-group']//button[1]").click()
    expect(userLoginFormPage.get_by_text("Success: You have added MacBook Air")).to_be_visible()
    
    userLoginFormPage.locator("//span[normalize-space()='My Account']").click()
    userLoginFormPage.get_by_role("link", name="Logout").click()
    expect(userLoginFormPage.get_by_role("heading", name="Account Logout")).to_be_visible()
