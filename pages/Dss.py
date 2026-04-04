import time

from playwright.sync_api import Page

class DssProductUi:
    
    def __init__(self, page: Page):
        
        self.page = page
        
        # --- Data Tables ---
        self.tables = page.locator("table.MuiTable-root:visible")

    def click_drilldown_tables(self):

        # If no table appears in 5s, we assume there are none.
        try:
            self.tables.first.wait_for(state="visible", timeout=2000)
        except:
            print("No tables found on this page. Skipping drill-down.")
            return # Exit the method early
        
        table_count = self.tables.count()
        
        for t in range(table_count):
            self.tables.nth(t).scroll_into_view_if_needed(timeout=2000)
            current_table = self.tables.nth(t)
            # get first row of table
            first_row = current_table.locator("tbody tr").first
            # click the first hyperlink of row for drill down
            drill_down_link = first_row.locator("td").nth(1).locator("span").first
            # This ensures the element is in the viewport before interaction
            drill_down_link.scroll_into_view_if_needed()
            try:
                # Added a small 'force' click if the MUI table has transparent overlays
                drill_down_link.click(timeout=1000)
                # self.page.wait_for_timeout(500)
            except Exception as e:
                print(f"Table {t+1}: Click failed or timed out. Skipping. Error: {e}")
                continue # Move to the next table

    def check_alt_tables(self, table_key):
        """
        table_key: BOUNDARY, USAGE
        """
        t_buttons = self.page.get_by_role("button").filter(
                                                        has=self.page.get_by_text(table_key, exact=True)
                                                    )
        
        # If no alt buttons appears in 5s, we assume there are none.
        try:
            t_buttons.first.wait_for(state="visible", timeout=500)
        except:
            print("No buttons found with given keyword.")
            return # Exit the method early
        
        button_count = t_buttons.count()
        
        for b in range(button_count):
            # get first button by keyword
            first_button = t_buttons.nth(b)
            first_button.scroll_into_view_if_needed(timeout=2000)
            # Added a small 'force' click if the MUI has transparent overlays
            first_button.click(timeout=2000)
            # self.page.wait_for_timeout(2000)
