import pytest
from utils import helpers

BASE_URL = helpers.get_env("host")
USERNAME = helpers.get_creds("PGR").get("username")
PASSWORD = helpers.get_creds("PGR").get("password")

@pytest.fixture(scope="session")
def tl_context(browser_chr):
    ctx = browser_chr.new_context()
    page = ctx.new_page()
    page.goto(BASE_URL + "/digit-ui/employee/user/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("input[name='username']").wait_for(state="visible")

    # Employee Login
    page.locator("input[name='username']").fill(USERNAME)
    page.locator("input[name='password']").fill(PASSWORD)

    # City selection
    dropdown_wrapper = page.locator(".employee-select-wrap.login-city-dd")
    dropdown_wrapper.click()
    options_box = page.locator("#jk-dropdown-unique")
    options_box.wait_for(state="visible", timeout=5000)
    options_box.locator(".profile-dropdown--item").nth(1).click()

    page.locator("button[type='submit']").click()

    # Wait for navigation to employee landing page
    page.wait_for_url("**/digit-ui/employee")
    page.wait_for_load_state("networkidle")
    page.close()
    yield ctx
    ctx.close()
    
