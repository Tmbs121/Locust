from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright) -> None:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    # Initiate a user session. If we open several tabs in the current browser instance, all those tabs will be opened
    # within the same user session.
    context = browser.new_context()
    # Create a new page
    page = browser.new_page()
    # Head over to OpenCart website
    page.goto("http://172.23.176.159/opencart/upload")
    
    # We better wait until the whole page loads before we can proceed with further actions.
    # wait_for_load_state("networkidle") means that we'll be waiting until there's no network activity for at least 500 ms.
    # That would be a good sign that the page we are going to test has fully loaded.
    page.wait_for_load_state("networkidle")
    
    #......................................................
    context.close()
    browser.close()
    
    
# To run the Playwright test:
with sync_playwright() as playwright:
    run(playwright)