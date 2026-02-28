
import re, time, pytest
from utils import helpers

MODULE = "DSS"
BASE_URL = helpers.get_env("host")

@pytest.mark.ui
def test_tl_dashboard(tl_context):

    page = tl_context.new_page()
    page.goto(BASE_URL + "/digit-ui/employee")

    # Wait for navigation to employee landing page
    page.wait_for_load_state("networkidle")

    # Extract page text
    page.get_by_role("link", name="Dashboard").click()
    dss_body = page.locator("#divToPrint")
    page.wait_for_load_state("networkidle")
    dss_body.wait_for(state="visible", timeout=15000)
    locales = dss_body.inner_text()
    locales = re.split(r'[\n\t]+', locales)
    locales = [item.strip() for item in locales if item.strip()]

    # Find localization leaks
    loc_codes = helpers.find_loc_codes(locales)
    helpers.write_json(loc_codes, MODULE + '_locales.json')
    assert True
