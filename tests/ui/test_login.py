import pytest
from utils import helpers

BASE_URL = helpers.get_env("host")
USERNAME = helpers.get_creds("TL").get("username")
PASSWORD = helpers.get_creds("TL").get("password")

@pytest.mark.ui
def test_language_selection(page_chr):

    # Language selection
    page_chr.goto(BASE_URL + "/digit-ui/employee/user/language-selection")

    # Get all available languages
    language_dd = page_chr.locator(".language-button-container button")
    language_dd.first.wait_for()
    languages = []
    for i in range(language_dd.count()):
        button_text = language_dd.nth(i).inner_text()
        languages.append(button_text)
    print("\nAvailable languages:", languages)
    
    # Language selection
    selected_locale = languages[0]
    print("\nSelected languages:", selected_locale)
    language_dd.get_by_text(selected_locale).click()
    page_chr.get_by_role("button").get_by_text("Continue").click()

    assert True

@pytest.mark.ui
def test_employee_login(page_chr):
    page_chr.goto(BASE_URL + "/digit-ui/employee/user/login")
    page_chr.wait_for_load_state("networkidle")
    # Employee Login
    page_chr.locator("input[name='username']").fill(USERNAME)
    page_chr.locator("input[name='password']").fill(PASSWORD)
    # City selection
    dropdown_wrapper = page_chr.locator(".employee-select-wrap.login-city-dd")
    dropdown_wrapper.click()
    options_box = page_chr.locator("#jk-dropdown-unique")
    options_box.wait_for(state="visible", timeout=5000)
    options_box.locator(".profile-dropdown--item").nth(1).click()

    page_chr.locator("button[type='submit']").click()
    # Wait for navigation to employee landing page
    page_chr.wait_for_url("**/digit-ui/employee")

    assert True
