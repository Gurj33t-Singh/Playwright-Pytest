import time, re
import pytest
from utils import helpers

BASE_URL = helpers.get_env("host")
MODULE = "TL"
USERNAME = helpers.get_creds(MODULE).get("username")
PASSWORD = helpers.get_creds(MODULE).get("password")

@pytest.mark.ui
def test_tl_landing_page(tl_context):

    page = tl_context.new_page()
    page.goto(BASE_URL + "/digit-ui/employee")
    page.wait_for_load_state("networkidle")

    # Extract page text
    body = page.locator("[id='root']")
    text = body.inner_text().split('\n')
    # Sidebar interaction
    sidebar = page.locator(".sidebar")
    sidebar.hover()
    # Sidebar click to expand (TL module)
    sidebar.locator("[data-for='jk-side-TRADE_LICENSE']").click()
    sidebar_text = sidebar.inner_text().split('\n')

    locales = text + sidebar_text

    print("\nLogged in page text:", text, type(text))
    print("\nSidebar text:", sidebar_text, type(sidebar_text))
    # loc_list = helpers.list_cleanup(text + sidebar_text)
    # print("\nFinal:", loc_list)

    # Find localization leaks
    loc_codes = helpers.find_loc_codes(locales)
    print("\nLocalization leaks:", loc_codes)
    helpers.write_json(loc_codes, MODULE + '_locales.json')

    assert True
    page.close()

@pytest.mark.ui
def test_demo(page_chr):

    # Language selection
    # page = context.new_page()
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
    locale = languages[0]
    print("\nSelected languages:", locale)
    language_dd.get_by_text(locale).click()
    page_chr.get_by_role("button").get_by_text("Continue").click()


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

    # Extract page text
    body = page_chr.locator("[id='root']")
    text = body.inner_text().split('\n')
    # Sidebar interaction
    sidebar = page_chr.locator(".sidebar")
    sidebar.hover()
    # Sidebar click to expand (TL module)
    sidebar.locator("[data-for='jk-side-TRADE_LICENSE']").click()
    sidebar_text = sidebar.inner_text().split('\n')

    body.locator(".employee-app-container").hover()
    page_chr.get_by_role("link", name="Dashboard").click()
    dss_body = page_chr.locator("#divToPrint")
    dss_body.wait_for(state="visible", timeout=15000)
    dss_text = dss_body.inner_text()
    dss_text = re.split(r'[\n\t]+', dss_text)
    dss_text = [item.strip() for item in dss_text if item.strip()]

    locales = text + sidebar_text + dss_text
    # Find localization leaks
    loc_codes = helpers.find_loc_codes(locales)
    print("\nLocalization leaks:", loc_codes)
    assert True
    page_chr.close()
