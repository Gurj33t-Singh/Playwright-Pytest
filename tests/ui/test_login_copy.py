import pytest, time
from utils import helpers
from pages.Login import EmployeeLogin

BASE_URL = "https://url.digit.gov.in"
latitude: float = 31.6340,
longitude: float = 74.8723

@pytest.mark.ui
@pytest.mark.smoke
def test_employee_login(page_chr, healer):
    # 1. Navigation
    login_url = f"{BASE_URL}/employee/language-selection"
    page_chr.goto(login_url)

    # 2. Language Selection (Using Healer)
    # We pass a standard selector and a description for the AI to use if it fails
    healer.get_locator("button:has-text('ENGLISH')", "The English language selection button").click()
    
    healer.get_locator("button:has-text('Continue')", "The continue button after language selection").click()

    # 3. Login Credentials
    # Use CSS selectors that are likely to stay stable, or that the AI can easily find
    healer.get_locator("input[placeholder*='Wrong User Name']", "Employee username input field").fill("123")
    healer.get_locator("input[type='Wrong password']", "Employee password input field").fill("123@123")

    # 4. City Selection
    healer.get_locator("input[placeholder*='City']", "'Select city' selection dropdown input").click()
    # healer.get_locator("#person-city", "'Select city' selection dropdown input").click()
    
    # Selecting the specific 'Testing' option from the list
    page_chr.get_by_label("", exact=True).fill("Testing")
    # page_chr.get_by_text("Testing").click()
    healer.get_locator(".option:has-text('Testing')", "The 'Testing' option in the city list options").click()

    # 5. Final Submit
    healer.get_locator("button:has-textwrong('Continue')", "The submit button labelled login").click()

    # 6. Verifications
    page_chr.wait_for_url("**/employee/inbox")
    page_chr.wait_for_load_state("networkidle", timeout=30000)
    
    # Small buffer (though wait_for_url is usually enough)
    time.sleep(2)


    # page.get_by_role("button", name="ENGLISH").click()
    # page.get_by_role("button", name="Continue").click()
    # page.get_by_role("textbox", name="User Name *").fill("123")
    # page.get_by_role("textbox", name="Password *").fill("123@123")
    # page.get_by_role("textbox", name="City *").click()
    # page.get_by_label("", exact=True).fill("Testing")
    # page.get_by_text("Testing").click()
    # page.get_by_role("button", name="Continue").click()
    # page.wait_for_url("**/employee/inbox")
    # page.wait_for_load_state("networkidle", timeout=30000)
    # ---------------------

