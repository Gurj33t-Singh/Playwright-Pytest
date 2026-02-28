from playwright.sync_api import Page

class EmpCreatePGR:
    
    def __init__(self, page: Page):
        
        self.page = page
        
        # --- Form Fields ---
        # Note: Using the container as a starting point as per your original script
        self.create_complaint_card = page.locator("#create-complaint-card")
        
        self.complainant_name_input = page.locator("#add-complaint")
        self.mobile_no_input = page.locator("#complainant-mobile-no")
        self.house_no_input = page.locator("#houseNo")
        self.landmark_input = page.locator("#landmark")
        self.additional_details_input = page.locator("[id='additional details']")

        # --- Complaint Type Popup ---
        self.complaint_type_trigger = page.locator("#complaint-type")
        self.complaint_list_card = page.locator(".list-main-card")
        self.complaint_type_search_input = page.locator("#complainttype-search")

        # --- City & Locality ---
        self.city_field_trigger = page.locator("#react-select-2-input")
        self.locality_field_trigger = page.get_by_text("#react-select-3-input")
        
        # --- Actions ---
        self.submit_btn = page.locator("#addComplaint-submit-complaint")

    def navigate(self, base_url: str):
        self.page.goto(f"{base_url}/employee/create-complaint")
        self.page.wait_for_load_state("networkidle")

    def fill_citizen_details(self, name: str, mobile: str, house: str, landmark: str, add_details: str):
        self.complainant_name_input.fill(name)
        self.mobile_no_input.fill(mobile)
        self.house_no_input.fill(house)
        self.landmark_input.fill(landmark)
        self.additional_details_input.fill(add_details)

    def select_complaint_type(self, 
                              type_name: str, 
                              subType: str,
                              isSubType: bool):
        self.complaint_type_trigger.click()
        self.complaint_list_card.wait_for(state="visible")
        self.complaint_type_search_input.fill(type_name)
        self.complaint_list_card.locator(f"[data-localization='{type_name}']").click()
        if isSubType:
            self.complaint_list_card.locator(f"[data-localization='{subType}']").click()

    def select_city(self, city_code: str):
        # The script shows clicking 'Select' inside the city field first
        self.city_field_trigger.click()
        self.city_field_trigger.get_by_role("textbox").fill(city_code)
        self.page.get_by_role("menuitem", name=city_code).click()

    def select_locality(self, locality_name: str):
        self.locality_field_trigger.click()
        self.locality_field_trigger.get_by_role("textbox").fill(locality_name)
        self.page.get_by_role("menuitem", name=locality_name).click()

