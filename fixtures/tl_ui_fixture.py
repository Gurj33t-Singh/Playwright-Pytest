import pytest
from utils import helpers

BASE_URL = helpers.get_env("host")

@pytest.fixture(scope="session")
def tl_context(browser_chr):
    tl_su_creds = helpers.get_creds("TL", "SU")
    if not tl_su_creds:
        pytest.skip("Missing credentials: TL.SU in config.json")

    username = tl_su_creds.get("username")
    password = tl_su_creds.get("password")
    if not username or not password:
        pytest.skip("Incomplete credentials: TL.SU username/password in config.json")

    ctx = browser_chr.new_context()
    page = ctx.new_page()
    page.goto(BASE_URL + "/digit-ui/employee/user/login")
    page.wait_for_load_state("domcontentloaded")
    page.locator("input[name='username']").wait_for(state="visible")

    # Employee Login
    page.locator("input[name='username']").fill(username)
    page.locator("input[name='password']").fill(password)

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
    
