from playwright.sync_api import Page
from utils.healer import SmartHealer

class EmployeeLogin:

    def __init__(self, page: Page, healer: SmartHealer):
        self.page = page
        self.healer = healer # Store the healer instance
        
    def init_landingPageLocators(self):
        # --- Using the Healer for static-but-unreliable locators ---
        self.language_options = self.page.locator(".button-item") # Lists are usually fine
        self.lang_continue_btn = self.healer.get_locator("#continue-action", "The language selection continue button")
        
    def init_loginPageLocators(self):
        # Incorrect locators to verify the healingAI
        self.username_input = self.healer.get_locator("#test-employee-phone", "The employee phone/username input field")
        self.password_input = self.healer.get_locator("#test-employee-password", "The employee password input field")
        self.city_input = self.healer.get_locator("#test-person-city", "The city selection dropdown trigger")
        
        self.city_select_dialog = self.page.locator(".citipicker-dialog")
        self.city_select_input = self.page.locator("#city-picker-search")
        self.city_list = self.city_select_dialog.locator(".list-main-card")
        self.login_submit_btn = self.healer.get_locator("#login-submit-action", "The final login submit button")

    # --- ACTION METHODS ---
    
    def select_language(self, language: str):
        """Selects language and moves to the login screen."""
        self.language_options.filter(has_text=language).click()
        self.lang_continue_btn.click()

    def login_employee(self, username: str, password: str, tenant_id: str):
        """Fills login details, selects city, and submits."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        
        # City selection flow
        self.city_input.click()
        self.city_list.wait_for(state="visible")
        # self.city_select_input.fill("tenant_id")
        self.city_list.locator(f'[id="{tenant_id}"]').click()
        
        self.login_submit_btn.click()
