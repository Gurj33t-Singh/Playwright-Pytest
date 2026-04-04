import re, time, pytest
from utils import helpers
from playwright.sync_api import expect
from pages.Dss import *

BASE_URL = helpers.get_env("host")
LOC_FILENAME = "TestMsevaDSS.json"
# Accumulate *raw* UI strings for this module/class
_collected_ui_strings = []

class TestMsevaDSS:

    page_root_id = "#root"

    # --- Fixtures ---
    @pytest.fixture(scope="class", autouse=True)
    def _write_loc_codes(self):
        yield
        leaks = helpers.find_loc_codes(_collected_ui_strings)
        helpers.write_json(leaks, LOC_FILENAME)

    # --- Helpers ---
    def get_table_data(self, dss_pom, page, alt_table_key):
        """
        it iterates drill down tables
        and checks for alt tables like USAGE and BOUNDARY

        returns list of strings
        """
        loc_codes = []

        dss_pom.click_drilldown_tables()
        loc_codes.extend(helpers.collect_page_text(page, self.page_root_id))
        
        dss_pom.check_alt_tables(alt_table_key)
        loc_codes.extend(helpers.collect_page_text(page, self.page_root_id))
        
        return loc_codes

    # --- Test Cases ---
    @pytest.mark.ui
    @pytest.mark.localization
    def test_sure_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

    @pytest.mark.ui
    @pytest.mark.localization
    def test_overview_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/overview')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

        # --- Service Tab ---
        page.get_by_role("tab", name="SERVICE").click()
        page.wait_for_load_state("networkidle", timeout=2000)
        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

    @pytest.mark.ui
    @pytest.mark.localization
    @pytest.mark.smoke
    def test_pt_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/propertytax')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

        # --- Service Tab ---
        page.get_by_role("tab", name="SERVICE").click()
        page.wait_for_load_state("networkidle")
        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

    @pytest.mark.ui
    @pytest.mark.localization
    def test_tl_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/tradelicense')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

        # --- Service Tab ---
        page.get_by_role("tab", name="SERVICE").click()
        page.wait_for_load_state("networkidle")
        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

    @pytest.mark.ui
    @pytest.mark.localization
    def test_ws_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/ws')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

        # --- Service Tab ---
        page.get_by_role("tab", name="SERVICE").click()
        page.wait_for_load_state("networkidle")
        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "USAGE"))

    @pytest.mark.ui
    @pytest.mark.localization
    def test_pgr_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/pgr')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "DEPARTMENT"))

    @pytest.mark.ui
    @pytest.mark.localization
    def test_mcollect_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/mCollect')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "CATEGORY"))
    
    @pytest.mark.ui
    @pytest.mark.localization
    def test_noc_dashboard(self, page_chr):
        page = page_chr
        page.goto(BASE_URL + '/dashboard/noc')
        
        try:
            page.wait_for_selector(self.page_root_id, timeout=2000)
        except:
            # If it's blank/failed, force a refresh once
            print("Blank page, performing manual refresh...")
            page.reload(wait_until="networkidle")

        captured_text = helpers.collect_page_text(page, self.page_root_id)
        _collected_ui_strings.extend(captured_text)

        # --- DSS POM
        dss_product_pom = DssProductUi(page)
        # --- Drilldown and Alt-table texts ---
        _collected_ui_strings.extend(self.get_table_data(dss_product_pom, page, "DEPARTMENT"))

