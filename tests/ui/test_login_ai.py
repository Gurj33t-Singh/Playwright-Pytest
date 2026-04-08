import pytest
from pages.LoginTest import EmployeeLogin
from utils.healer import SmartHealer

BASE_URL = "https://url.lstate.gov.in"
username = "<username>"
password = "<password>"
tenant_id = "<state.city>"
language = "ENGLISH"

@pytest.fixture
def healer(page_chr):
    return SmartHealer(page_chr)

@pytest.mark.ui
@pytest.mark.smoke
def test_employee_login(page_chr, healer):
    login_url = f"{BASE_URL}/employee/language-selection"
    login_pom = EmployeeLogin(page_chr, healer)
    page_chr.goto(login_url)
    page_chr.wait_for_load_state("networkidle")
    login_pom.init_landingPageLocators()
    login_pom.select_language(language)
    page_chr.wait_for_load_state("networkidle")
    login_pom.init_loginPageLocators()
    login_pom.login_employee(username, password, tenant_id)
    # page_chr.wait_for_url("**/employee/inbox")
    page_chr.wait_for_load_state("networkidle")
    page_chr.wait_for_timeout(5000)
    page_chr.close()
