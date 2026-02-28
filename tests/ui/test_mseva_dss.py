
import re, time, pytest
from utils import helpers
from playwright.sync_api import expect

BASE_URL = helpers.get_env("host")

class TestMsevaDSS:

    loc_codes = []

    @pytest.fixture(scope="class", autouse=True)
    def _teardown_write_loc_codes(self, request):
        """Class-scoped autouse fixture: after all tests in the class run,
        write the class variable `loc_codes` to a JSON file under target/.
        """
        yield
        helpers.write_json(self.loc_codes, 'TestMsevaDSS.json')

    @pytest.mark.ui
    @pytest.mark.localization
    def test_sure_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard')
        page.wait_for_load_state("networkidle")
        # Extract page text
        dss_body = page.locator("#divToPrint")
        dss_body.wait_for(state="visible", timeout=30000)
        locales = dss_body.inner_text()
        locales = locales.replace('\t', '\n')
        # Find localization leaks
        loc_codes = helpers.find_loc_codes(locales)
        self.loc_codes.extend(loc_codes)
        expect(dss_body).to_be_visible()

    @pytest.mark.ui
    @pytest.mark.localization
    def test_pt_dashboard_rev(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/propertytax')
        page.wait_for_load_state("networkidle")
        dss_body = page.locator("#divToPrint")
        table_row = dss_body.get_by_role("row").first
        table_row.wait_for(state="visible", timeout=30000)
        locales = dss_body.inner_text()
        # Find localization leaks
        loc_codes = helpers.find_loc_codes(locales, isTable=True)
        self.loc_codes.extend(loc_codes)
        expect(table_row).to_be_visible()

    @pytest.mark.ui
    @pytest.mark.localization
    def test_pt_dashboard_rev_tb(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/propertytax')
        body = page.locator("#divToPrint")
        body.wait_for(state="visible", timeout=30000)
        table_data = helpers.get_table_data(body)
        table_data = re.split(r'[\t\n]', table_data)
        table_data = helpers.find_loc_codes(table_data)
        self.loc_codes.extend(table_data)
        assert True

    @pytest.mark.ui
    @pytest.mark.localization
    def test_tl_dashboard_rev(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/tradelicense')
        page.wait_for_load_state("networkidle")
        dss_body = page.locator("#divToPrint")
        table_row = dss_body.get_by_role("row").first
        table_row.wait_for(state="visible", timeout=30000)
        locales = dss_body.inner_text()
        # Find localization leaks
        loc_codes = helpers.find_loc_codes(locales, isTable=True)
        self.loc_codes.extend(loc_codes)
        expect(table_row).to_be_visible()

    @pytest.mark.ui
    @pytest.mark.localization
    def test_tl_dashboard_rev_tb(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/tradelicense')
        page.wait_for_load_state("networkidle")
        body = page.locator("#divToPrint")
        body.wait_for(state="visible", timeout=30000)
        table_data = helpers.get_table_data(body)
        table_data = re.split(r'[\t\n]', table_data)
        table_data = helpers.find_loc_codes(table_data)
        self.loc_codes.extend(table_data)
        assert True

    @pytest.mark.ui
    @pytest.mark.localization
    def test_pgr_dashboard_rev(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/pgr')
        page.wait_for_load_state("networkidle")
        dss_body = page.locator("#divToPrint")
        table_row = dss_body.get_by_role("row").first
        table_row.wait_for(state="visible", timeout=30000)
        locales = dss_body.inner_text()
        # Find localization leaks
        loc_codes = helpers.find_loc_codes(locales, isTable=True)
        self.loc_codes.extend(loc_codes)
        expect(table_row).to_be_visible()

    @pytest.mark.ui
    @pytest.mark.localization
    def test_pgr_dashboard_rev_tb(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/pgr')
        page.wait_for_load_state("networkidle")
        body = page.locator("#divToPrint")
        body.wait_for(state="visible", timeout=30000)
        table_data = helpers.get_table_data(body)
        table_data = re.split(r'[\t\n]', table_data)
        table_data = helpers.find_loc_codes(table_data)
        self.loc_codes.extend(table_data)
        assert True

    @pytest.mark.ui
    @pytest.mark.localization
    @pytest.mark.smoke
    def test_noc_dashboard_rev_tb(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/noc')
        page.wait_for_load_state("networkidle")
        dss_body = page.locator("#divToPrint")
        dss_body.wait_for(state="visible", timeout=30000)
        dss_body.get_by_role("button").filter(has_text="DEPARTMENT").click()
        time.sleep(2)
        locales = dss_body.inner_text()
        locales = helpers.find_loc_codes(locales, isTable=True)
        self.loc_codes.extend(locales)
        assert True

