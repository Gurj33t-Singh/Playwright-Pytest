from playwright.sync_api import Page

class EmployeeLogin:

    def __init__(self, page: Page):
        self.page = page
        
        # --- Language Selection Locators ---
        self.language_options = page.locator(".button-item")
        self.lang_continue_btn = page.locator("#continue-action")
        
        # --- Login Page Locators ---
        self.username_input = page.locator("#employee-phone")
        self.password_input = page.locator("#employee-password")
        self.city_input = page.locator("#person-city")
        
        # --- City Picker Locators ---
        self.city_select_dialog = page.locator(".citipicker-dialog")
        self.city_select_input = page.locator("#city-picker-search")
        self.city_list = self.city_select_dialog.locator(".list-main-card")
        
        # --- Main Action Button ---
        self.login_submit_btn = page.locator("#login-submit-action")

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
        # self.city_select_input.fill("tenant_id")
        self.city_list.locator(f'[id="{tenant_id}"]').click()
        
        self.login_submit_btn.click()
