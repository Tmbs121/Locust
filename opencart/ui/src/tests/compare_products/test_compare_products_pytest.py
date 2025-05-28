from playwright.sync_api import expect

from ui.src.pages.home_page import HomePage


def test_compare_products(set_up_tear_down, username, password) -> None:
    page = set_up_tear_down
    home_p = HomePage(page)
    login_p = home_p.navigate_to_login_page()
    expect(login_p.new_customer_header).to_be_visible()
    login_p.fill_email_address(username)
    login_p.fill_password(password)
    user_profile_p = login_p.login_to_user_profile()
    expect(user_profile_p.my_account_header).to_be_visible()
    user_profile_p.hover_over_laptops_and_notebooks()
    laptops_notebooks_p = user_profile_p.click_all_laptops_and_notebooks_section()
    expect(laptops_notebooks_p.laptops_notebooks_header).to_have_text("Laptops & Notebooks")
    product_one_p = laptops_notebooks_p.click_product_one_description()
    expect(product_one_p.product_one_description_link).to_be_visible()
    product_one_p.click_add_to_comparison_list_button()
    product_one_p.click_back_button_in_the_browser()
    expect(laptops_notebooks_p.laptops_notebooks_header).to_be_visible()
    product_two_p = laptops_notebooks_p.click_product_two_description()
    expect(product_two_p.product_two_description_link).to_be_visible()
    product_two_p.click_add_to_comparison_list_button()
    compare_list_p = product_two_p.click_product_comparison_link()
    expect(compare_list_p.product_comparison_header).to_be_visible()
    compare_list_p.click_remove_button()
    expect(compare_list_p.success_alert_message_comp_list_modified).to_be_visible()
    compare_list_p.click_add_cart_button()
    shopping_cart_p = compare_list_p.click_shopping_cart_link()
    expect(shopping_cart_p.shopping_cart_header).to_be_visible()
    shopping_cart_p.change_quantity_of_products("2")
    shopping_cart_p.update_shopping_cart()
    shopping_cart_p.empty_shopping_cart()
    logout_p = shopping_cart_p.log_out_of_user_profile()
    expect(logout_p.account_logout_header).to_be_visible()
