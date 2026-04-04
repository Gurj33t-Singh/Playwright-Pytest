from playwright.sync_api import Error, Page, TimeoutError as PlaywrightTimeoutError

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
        self.left_menu_home_btn = self.left_menu.locator('#HOME-0')

        # quick action 
        self.quick_action_btn = page.locator(".quick-action-button").get_by_role("button")
        self.quick_action_dd = page.locator("#menu-list-grow").get_by_role("menuitem")
        
    def left_menu_selection(self, option_id: str):
        # Menu re-renders while expanding sections; re-locate and retry click.
        self.left_menu.wait_for(state="visible", timeout=15000)
        last_err = None
        for _ in range(4):
            target = self.left_menu.locator(f"#{option_id}").first
            try:
                target.wait_for(state="visible", timeout=8000)
                target.scroll_into_view_if_needed(timeout=5000)
                target.click(timeout=8000,
                             force=True #this is specifically for mac
                             )
                return
            except (PlaywrightTimeoutError, Error) as err:
                last_err = err
                self.page.wait_for_timeout(250)
        raise last_err

    def logout(self):
        self.profile_icon.click()
        self.user_acc_info_dd.wait_for(state="visible")
        self.logout_btn.click()

        self.logout_popup.wait_for(state="visible")
        self.logout_yes_btn.click()
        self.page.wait_for_load_state("networkidle")

    def quick_action_option(self, option_name):
        self.quick_action_btn.click()
        self.quick_action_dd.filter(has_text=option_name).click()
        
