from playwright.sync_api import Page

class EmpMonoUI:

    def __init__(self, page: Page):
        self.page = page

        # profile edit/logout
        self.profile_icon = page.locator(".userSettingsInnerContainer")
        self.user_acc_info_dd = page.locator(".user-acc-info")
        self.edit_profile_btn = self.profile_icon.locator("#header-profile")
        self.logout_btn = self.profile_icon.locator("#header-logout")

        # logout popup
        self.logout_popup = page.locator(".logout-popup")
        self.logout_yes_btn = self.logout_popup.locator("#logout-yes-button")
        self.logout_no_btn = self.logout_popup.locator("#logout-no-button")

        # left menu options 
        self.left_menu = page.locator("#menu-container")
        
    def left_menu_selection(self, option_id: str):
        self.left_menu.locator(f'[id="{option_id}"]').click()

    def logout(self):
        self.profile_icon.click()
        self.user_acc_info_dd.wait_for(state="visible")
        self.logout_btn.click()

        self.logout_popup.wait_for(state="visible")
        self.logout_yes_btn.click()
        self.page.wait_for_load_state("networkidle")

