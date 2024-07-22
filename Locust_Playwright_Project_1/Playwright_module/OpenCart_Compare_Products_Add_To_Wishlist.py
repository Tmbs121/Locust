from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    # Create a new page
    page = browser.new_page()
    # Head over to OpenCart website
    page.goto("http://172.23.176.159/opencart/upload")
    
    
    browser.close()