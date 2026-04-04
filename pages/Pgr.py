import time

from playwright.sync_api import Page

class EmpCreatePGR:
    
    def __init__(self, page: Page):
        
        self.page = page
        
        # --- Create Complaint Form ---
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
        self.city_field_input = page.locator("#react-select-2-input")
        self.locality_field_input = page.locator("#react-select-3-input")
        
        # --- Actions ---
        self.submit_btn = page.locator("#addComplaint-submit-complaint")

    def navigateCreateComplaint(self, base_url: str):
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
        # self.complaint_type_search_input.fill(type_name)
        self.complaint_list_card.locator(f"[data-localization='{type_name}']").click()
        if isSubType:
            self.complaint_list_card.locator(f"[data-localization='{subType}']").click()

    def select_city(self, city_code: str):
        # The script shows clicking 'Select' inside the city field first
        # self.city_field_input.click()
        self.city_field_input.fill(city_code)
        self.page.get_by_role("menuitem", name=city_code).click()

    def select_locality(self, locality_name: str):
        # self.locality_field_input.click()
        self.locality_field_input.fill(locality_name)
        self.page.get_by_role("menuitem", name=locality_name).click()

    def get_complaint_no(self):
        return self.page.locator('[class="label-container complaint-number-value"]').inner_text().strip()

class EmpOpenComplaints:

    def __init__(self, page: Page):
        
        self.page = page

        self.unassigned_filter_btn = page.get_by_role("button").filter(has_text="UNASSIGNED")
        self.assigned_filter_btn = page.get_by_role("button").filter(has_text="ASSIGNED")
        self.complaint_card = page.locator(".complaint-card-wrapper")

        # --- LME Open Complaints UI ---
        self.lme_complaint_search_card = page.locator("#complaint-search-card")
        self.lme_complaint_id_input = page.locator("#complaint-no")
        self.lme_mobile_search_input = page.locator("#mobile-no")
        self.lme_search_btn = page.locator('button').filter(
            has=page.locator('[data-localization="SEARCH"]'))
        self.lme_clear_search_btn = page.locator('button').filter(
            has=page.locator('[data-localization="CLEAR SEARCH"]'))

    def open_complaint(self, complaint_id):
        """
        For GRO user, open complaints card directly looks for complaint_id and clicks on card.
        """
        self.complaint_card.locator(f'[data-localization="{complaint_id}]').click()

    def search_open_lme_complaint(self, complaint_no):
        self.lme_complaint_id_input.fill(complaint_no[-6:])
        self.lme_search_btn.click()
        self.page.locator(f'[data-localization="{complaint_no}"]').click()

class EmpSearchComplaints:

    def __init__(self, page: Page):
        
        self.page = page

        self.search_complaint_card = page.locator("#complaint-search-card")

        self.mobile_input = page.locator("#mobile-no")
        self.complaint_id_input = page.locator("#complaint-no")
        self.search_btn = page.locator('button').filter(
            has=page.locator('[data-localization="SEARCH"]'))
        self.clear_search_btn = page.locator('button').filter(
            has=page.locator('[data-localization="CLEAR SEARCH"]'))
        self.complaint_card_list = page.locator(".complaints-card-main-cont")

    def search_complaint(self, complaint_no):
        self.complaint_id_input.fill(complaint_no[-6:])
        self.search_btn.click()
        self.complaint_card_list.wait_for(state="visible")
        self.page.locator(f'[data-localization="{complaint_no}"]').click()

class EmpComplaintSummary:

    def __init__(self, page: Page):
        
        self.page = page

        self.complaint_detail_card = page.locator(".complaint-detail-full-width")

        self.comment_input = page.locator("#citizen-comment")
        self.assign_resolve_btn = page.locator("#actionTwo")
        self.reject_reassign_btn = page.locator("#actionOne")

        # --- Assignee list ui ---
        self.assignee_list = page.locator("#assignComplaint")
        self.assignee_search_input = page.locator("#employee-search")
        self.assign_confirm_btn = page.locator('button').filter(
            has=self.page.locator('[data-localization="ASSIGN"]'))
        
        # --- Assigned acknowledgement ui ---
        self.assigned_ack_card = page.locator(".success-message-inner-cont")

        # --- LME UI ---
        self.mark_resolved_btn = page.locator("#complaintresolved-submit-action")
        self.lme_resolve_form = page.locator("#complaintResolved")

    def assign_complaint(self, assignee_name):
        self.complaint_detail_card.wait_for(state="visible")
        self.assign_resolve_btn.click()
        self.page.locator(".employee-list-cont").wait_for(state="visible")
        self.page.locator(f'[data-localization="{assignee_name}"]').click()
        self.page.locator(".responsive-action-button").get_by_role("button").click()
        self.assigned_ack_card.wait_for(state="visible")
        
    def lme_resolve_complaint(self):
        self.assign_resolve_btn.click()
        self.lme_resolve_form.wait_for(state="visible")
        self.mark_resolved_btn.click()
