
import re, time, pytest
from utils import helpers
from playwright.sync_api import expect
from pages.Login import EmployeeLogin
from pages.LandingPage import EmpMonoUI
from pages.Pgr import EmpCreatePGR

BASE_URL = helpers.get_env("host")
LOC_FILENAME = "TestMsevaPgr.json"

class TestMsevaPgr:

    USERNAME = helpers.get_creds("PGR").get("username")
    PASSWORD = helpers.get_creds("PGR").get("password")
    TENANT = helpers.get_creds("PGR").get("tenantId")
    CITY = helpers.get_creds("PGR").get("city")
    LANGUAGE = "English"
    loc_codes = []

    @pytest.fixture(scope="class", autouse=True)
    def pgr_emp_ctx_fixture(self, browser_chr):

        # returns employee ui login context

        LOGIN_URL = BASE_URL + "/employee/language-selection"

        context = browser_chr.new_context()
        page = context.new_page()
        EmpLoginPom = EmployeeLogin(page)

        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # Language-select page
        EmpLoginPom.select_language(self.LANGUAGE)
        page.wait_for_load_state("networkidle")

        # Employee Login
        EmpLoginPom.login_employee(username=self.USERNAME,
                                     password=self.PASSWORD,
                                     tenant_id=self.TENANT)

        # Wait for navigation to employee landing page
        page.wait_for_url("**/employee/inbox")
        page.wait_for_load_state("networkidle")
        page.close()
        yield context
        context.close()
        helpers.write_json(self.loc_codes, LOC_FILENAME)
  
    def test_pgr_empHomePageNav(self, pgr_emp_ctx_fixture):
        page = pgr_emp_ctx_fixture.new_page()
        page.goto(BASE_URL + "/employee")
        page.wait_for_load_state("networkidle")
        
        EmpPom = EmpMonoUI(page)

        EmpPom.left_menu_selection("PGR-1")
        EmpPom.left_menu_selection("CREATE-COMPLAINT-0")
        page.wait_for_load_state("networkidle")
        page.locator("#create-complaint-card").wait_for(state="visible")
        time.sleep(30)
        page.close()

    @pytest.mark.pgr
    def test_pgr_createComplaint(self, pgr_emp_ctx_fixture):
        page = pgr_emp_ctx_fixture.new_page()
        EmpPgrPom = EmpCreatePGR(page)

        # Create Complaint UI
        page.goto(BASE_URL + '/employee/create-complaint')
        page.wait_for_load_state("networkidle")
        
        # Create Complaint form
        EmpPgrPom.fill_citizen_details(name="Test Name",
                                       mobile="9999999991",
                                       house="HN 123 ST 123",
                                       landmark="Tst Lndmrk",
                                       add_details="Add Info")

        # Complaint type popup
        EmpPgrPom.select_complaint_type(type_name="Animals",
                                        subType="Dead Animals",
                                        isSubType=True)
        
        # page.locator("[id='complaint-type']").click()
        # page.locator("[id='complainttype-search']").fill("Dead Animals")
        # page.locator("[data-localization='Dead Animals']").click()

        # City selection dropdown 
        EmpPgrPom.select_city(self.TENANT)
        # city_field = page.locator("[id='city']")
        # city_field.get_by_text("Select").click()
        # city_field.get_by_role("textbox").fill("pb.testing")
        # page.get_by_role("menuitem", name="pb.testing").click()

        # Locality selection dropdown 
        EmpPgrPom.select_locality(locality_name="Azad Nagar - WARD-")
        # page.get_by_text("Choose Locality/Mohalla").click()
        # page.get_by_role("menuitem", name="Azad Nagar - WARD-").click()

        # Submit complaint
        EmpPgrPom.submit_btn.click()
        # page.locator("#addComplaint-submit-complaint").click()
        time.sleep(5)
        page.close()

