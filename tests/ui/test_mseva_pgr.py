
import re, time, pytest
from utils import helpers
from pages.LandingPage import EmpMonoUI
from pages.Pgr import *

BASE_URL = helpers.get_env("host")
LOC_FILENAME = "TestMsevaPgr.json"
# Accumulate *raw* UI strings for this module/class
_collected_ui_strings = []

class TestMsevaPgr:

    creds = helpers.get_creds(module="PGR")
    language = "English"
    complaint_no = None
    lme_assignee_name = "TESEMP0"

    # --- Fixtures ---
    @pytest.fixture(scope="class", autouse=True)
    def _write_loc_codes(self):
        yield
        leaks = helpers.find_loc_codes(_collected_ui_strings)
        helpers.write_json(leaks, LOC_FILENAME)

    @pytest.fixture(scope="class")
    def pgr_contexts(self, browser_chr):
        login_url = BASE_URL+"/employee/language-selection"

        csr_ctx = helpers.get_logged_in_context(
            browser_chr=browser_chr,
            login_url=login_url,
            creds=self.creds.get("CSR"),
            language=self.language,
        )
        gro_ctx = helpers.get_logged_in_context(
            browser_chr=browser_chr,
            login_url=login_url,
            creds=self.creds.get("GRO"),
            language=self.language,
        )
        lme_ctx = helpers.get_logged_in_context(
            browser_chr=browser_chr,
            login_url=login_url,
            creds=self.creds.get("LME"),
            language=self.language,
        )
        contexts = {"CSR": csr_ctx,
                   "GRO": gro_ctx,
                   "LME": lme_ctx}
        yield contexts
        csr_ctx.close()
        gro_ctx.close()
        lme_ctx.close()

    @pytest.fixture(scope="class")
    def csr_create_fix(self, pgr_contexts):
        context = pgr_contexts.get("CSR")
        page = context.new_page()

        emp_create_pgr_pom = EmpCreatePGR(page)
        emp_create_pgr_pom.navigateCreateComplaint(base_url=BASE_URL)

        emp_create_pgr_pom.fill_citizen_details(
            name="Test Name",
            mobile="9999999991",
            house="HN 123 ST 123",
            landmark="Tst Lndmrk",
            add_details="Add Info",
        )

        emp_create_pgr_pom.select_complaint_type(
            type_name="Animals",
            subType="Dead Animals",
            isSubType=True,
        )

        CSR_CRED = self.creds.get("CSR")
        emp_create_pgr_pom.select_city(city_code=CSR_CRED.get("tenantId"))
        emp_create_pgr_pom.select_locality(locality_name="Azad Nagar - WARD-1")
        emp_create_pgr_pom.submit_btn.click()

        page.wait_for_load_state("networkidle")
        complaint_no = emp_create_pgr_pom.get_complaint_no()
        page.close()

        assert complaint_no, "Complaint number was not captured."
        return complaint_no
    
    @pytest.fixture(scope="class")
    def gro_assign_fix(self, pgr_contexts, csr_create_fix):
        complaint_no = csr_create_fix
        context = pgr_contexts.get("GRO")
        page = context.new_page()
        page.goto(BASE_URL + "/employee")
        page.wait_for_load_state("networkidle")

        # --- POM Objects ---
        emp_pom = EmpMonoUI(page)
        emp_pgr_pom = EmpSearchComplaints(page)
        emp_pgr_summary_pom = EmpComplaintSummary(page)

        emp_pom.quick_action_option("Search Complaint")
        page.wait_for_load_state("networkidle")
        emp_pgr_pom.search_complaint(complaint_no)
        emp_pgr_summary_pom.assign_complaint(self.lme_assignee_name)
        page.close()
        return complaint_no

    # --- Test Cases ---
    @pytest.mark.parametrize(
                        ["citizen_data", "complaint_detail"],
                        [({"name": "Test Name", 
                          "mobile": "9999999991", 
                          "house": "HN 123", 
                          "landmark": "Tst Lndmrk", 
                          "add_details": "Add Info",
                          "tenantId": "pb.testing",
                          "locality": "Azad Nagar - WARD-1"}, 
                          {"type": "Animals",
                           "subType": "Dead Animals",
                           "isSubType": True})]
                           )
    @pytest.mark.pgr
    def test_pgr_createComplaint(self, pgr_contexts, citizen_data, complaint_detail):
        context = pgr_contexts.get("CSR")
        page = context.new_page()

        emp_pgr_pom = EmpCreatePGR(page)
        emp_pgr_pom.navigateCreateComplaint(base_url=BASE_URL)

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        emp_pgr_pom.fill_citizen_details(
            name=citizen_data["name"],
            mobile=citizen_data["mobile"],
            house=citizen_data["house"],
            landmark=citizen_data["landmark"],
            add_details=citizen_data["add_details"],
        )

        emp_pgr_pom.select_complaint_type(
            type_name=complaint_detail["type"],
            subType=complaint_detail["subType"],
            isSubType=complaint_detail["isSubType"],
        )
        
        emp_pgr_pom.select_city(citizen_data["tenantId"])
        emp_pgr_pom.select_locality(citizen_data["locality"])

        emp_pgr_pom.submit_btn.click()

        page.wait_for_load_state("networkidle")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        self.complaint_no = emp_pgr_pom.get_complaint_no()
        assert self.complaint_no, "Complaint number was not captured."

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)
        page.close()

    @pytest.mark.pgr
    def test_pgr_groUiNav(self, pgr_contexts):
        """
        This test is just verify the UI navigation
        """
        context = pgr_contexts.get("GRO")
        page = context.new_page()
        page.goto(BASE_URL + "/employee")
        page.wait_for_load_state("networkidle")

        emp_pom = EmpMonoUI(page)
        emp_pom.quick_action_option("Search Complaint")
        
        page.wait_for_load_state("networkidle")
        page.locator("#complaint-search-card").wait_for(state="visible")

        emp_pom.left_menu_home_btn.click()
        emp_pom.left_menu_selection("PGR-1")
        emp_pom.left_menu_selection("OPEN-COMPLAINTS-0")
        page.locator(".complaints-card-main-cont").first.wait_for(state="visible", timeout=50000)
        page.wait_for_load_state("networkidle")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        page.close()

    @pytest.mark.parametrize("assignee", ["TESEMP0"])
    @pytest.mark.pgr
    def test_pgr_empComplaintAssign(self, pgr_contexts, csr_create_fix, assignee):
        complaint_no = csr_create_fix
        context = pgr_contexts.get("GRO")
        page = context.new_page()

        page.goto(BASE_URL + "/employee")
        page.wait_for_load_state("networkidle")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        # --- POM Objects ---
        emp_pom = EmpMonoUI(page)
        emp_pgr_pom = EmpSearchComplaints(page)
        emp_pgr_summary_pom = EmpComplaintSummary(page)

        emp_pom.quick_action_option("Search Complaint")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)
        page.wait_for_load_state("networkidle")

        emp_pgr_pom.search_complaint(complaint_no)

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)
        emp_pgr_summary_pom.assign_complaint(assignee)

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        page.close()

    @pytest.mark.pgr
    def test_pgr_resolve(self, pgr_contexts, gro_assign_fix):
        complaint_no = gro_assign_fix
        context = pgr_contexts.get("LME")
        page = context.new_page()
        page.goto(BASE_URL + "/employee")
        page.wait_for_load_state("networkidle")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        # navigate to open complaints 
        landing_page_pom = EmpMonoUI(page)
        landing_page_pom.left_menu_selection("PGR-1")
        landing_page_pom.left_menu_selection("OPEN-COMPLAINTS-0")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        # navigate to complaint summary
        open_complaints_pom = EmpOpenComplaints(page)
        open_complaints_pom.search_open_lme_complaint(complaint_no)

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)

        # resolve complaint
        complaint_summary_pom = EmpComplaintSummary(page)
        complaint_summary_pom.lme_resolve_complaint()
        complaint_summary_pom.assigned_ack_card.wait_for(state="visible")

        captured_text = helpers.collect_page_text(page, "#root")
        _collected_ui_strings.extend(captured_text)
        page.close()
