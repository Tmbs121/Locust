import re, random, Parse_User_Credentials_From_CSV
from playwright.sync_api import sync_playwright, Playwright, expect

def run(playwright: Playwright) -> None:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    # Initiate a user session. If we open several tabs in the current browser instance, all those tabs will be opened
    # within the same user session.
    context = browser.new_context()
    # Create a new page
    page = context.new_page()
    # Head over to OpenCart website
    page.goto("http://172.23.176.159/opencart/upload")
    
    # We better wait until the whole page loads before we can proceed with further actions.
    # wait_for_load_state("networkidle") means we'll be waiting until there's no network activity for at least 500 ms.
    # That would be a good sign that the page we are going to test has fully loaded.
    page.wait_for_load_state("networkidle")
    expect(page).to_have_title(re.compile("Your Store"))

    page.goto("http://172.23.176.159/opencart/upload/index.php?route=account/login")
    
    # Assert we've got to the login form page. There are two ways we can do assertions in a Playwright script.
    # We can do it the classic Python way using the assert keyword, it would look like this: 
    
    # assert page.is_visible("text=Returning Customer")
    
    # The second - and more preferable way - is the Playwright way of doing assertions and that is by using
    # expect with page locator and string for assertion followed by to_be_visible method.
    # The second way is a recommended option because the expect syntax makes Playwright retry the assertion for
    # several seconds, so it wouldn't fail straight away if the assertion condition is not met and that's the
    # behavior we'd probably prefer to see in the Playwright script.
    expect(page.get_by_role("heading", name="Returning Customer")).to_be_visible()
    
    # Retrieve from the 'Parse_User_Credentials_From_CSV' module the USER_CREDENTIALS dict
    # that contains all credentials parsed from csv file and then use random.choice to pick a
    # random credential pair from the parsed csv content.
    USER_CREDENTIALS = Parse_User_Credentials_From_CSV.LoginWithCredsFromCSV.readCredsFromCSV()
    credentials_pair = random.choice(list(USER_CREDENTIALS.items()))
    username = credentials_pair[0]
    password = credentials_pair[1]
    
    # Enter the username and password in the login form to log in to the user's profile 
    page.get_by_placeholder("E-Mail Address").click()
    page.get_by_placeholder("E-Mail Address").fill(username)
    page.get_by_placeholder("E-Mail Address").press("Tab")
    
    page.get_by_placeholder("Password").fill(password)
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_load_state("networkidle")
    expect(page.locator("#content").get_by_role("heading", name="My Account")).to_be_visible()
    
    # Navigate to the 'Laptops & Notebooks' section of the OC website
    page.get_by_role("link", name="Laptops & Notebooks").hover()
    page.get_by_text('Show All Laptops & Notebooks').click()
    expect(page.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()
    
    # Click one of the items available in the 'Laptops & Notebooks' section to open a page with a
    # detailed description of the first chosen product.
    page.get_by_role("link", name="HP LP3065").first.click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()
    
    # Add the first chosen product to the Comparison List
    # The line below is an example of finding a web element (Add to Compare list button) by xpath
    page.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(page.locator("#product-product div").filter(has_text="Success: You have added HP")
           .locator("i")).to_be_visible()
    
    # Go back to the "All Laptops and Notebooks" section of the website by clicking the [Back] button
    # in the browser. In the code line below, to wait for the page to load we use an optional argument for the
    # go_back method, namely wait_until="domcontentloaded". In many cases waiting until
    # DOM content is loaded is a better wait option than wait_for_load_state("networkidle").
    page.go_back(wait_until="domcontentloaded")
    expect(page.locator("#content").get_by_role("heading", name="Laptops & Notebooks")).to_be_visible()

    # Click another item available in the 'Laptops & Notebooks' section to open a page with a
    # detailed description of the second chosen product.
    page.get_by_role("link", name="MacBook Air").first.click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()
    
    # Add the second chosen product to the Comparison List
    # The line below is an example of finding a web element (Add to Compare list button) by xpath
    page.locator("//i[contains(@class, 'fa fa-exchange')]").click()
    expect(page.locator("#product-product div").filter(has_text="Success: You have added MacBook Air")
           .locator("i")).to_be_visible()
    
    
    # Open the compare list after adding 2 products there:
    page.get_by_role("link", name="product comparison").click()
    page.wait_for_load_state("domcontentloaded")
    expect(page.get_by_role("heading", name="Product Comparison")).to_be_visible()
    
    # Delete one of the products from the compare list:
    page.get_by_role("link", name="Remove").first.click()
    expect(page.get_by_text("Success: You have modified")).to_be_visible()
    
    # Go back to the product page of the product of choice (the one left in the compare list):
    page.get_by_role("link", name="MacBook Air").click()
    expect(page.get_by_role("link", name="Description")).to_be_visible()
    
    # Add the product of choice to the Wishlist:
    page.locator("//div[@id='product-product']//div[@class='btn-group']//button[1]").click()
    expect(page.get_by_text("Success: You have added MacBook Air")).to_be_visible()
    
    # Log out of the user profile
    page.locator("//span[normalize-space()='My Account']").click()
    page.get_by_role("link", name="Logout").click()
    expect(page.get_by_role("heading", name="Account Logout")).to_be_visible()

    
    context.close()
    browser.close()
    
    
# To run the Playwright test:
with sync_playwright() as playwright:
    run(playwright)