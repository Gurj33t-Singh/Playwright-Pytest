import time
import pandas as pd
import csv, json
import re
from pages.Login import EmployeeLogin

LOCALIZATION_SOURCE_PATH = 'target/resources/source.json'
CONFIG_PATH = "config.json"

def get_env(conf_key=None):
    """Returns specific key value pair from env_config"""
    with open(CONFIG_PATH) as f:
        env_config = json.load(f)
    return env_config.get(conf_key) if conf_key else env_config

def get_creds(module):
    """Returns credentials of a specific user"""
    creds = get_env("credentials").get(module)
    return creds

def validate_regex(string_list):
    # 1. POSITIVE: Must contain at least one of these technical characters
    INCLUDE_PATTERN = re.compile(r'[_.]')

    # 2. NEGATIVE: Matches strings that are ONLY numbers, commas, spaces, dots, or %
    EXCLUDE_JUNK_PATTERN = re.compile(r'^[0-9\s,%.]+$')

    filtered_list = []
    for item in string_list:
        # Step A: Basic technical character check
        if INCLUDE_PATTERN.search(item):
            
            # Step B: Exclude pure tax/amount/number junk
            if not EXCLUDE_JUNK_PATTERN.match(item):
                
                # Step C: Smart Space Check
                if " " in item:
                    # If it has a space, it MUST have an underscore to be a key.
                    # This keeps "DSS_TB_PT (In Lac)" but drops "Enter House No."
                    if "_" in item:
                        filtered_list.append(item)
                else:
                    # No space? It's likely a standard key (like 'pb.testing')
                    filtered_list.append(item)
                    
    return filtered_list

def find_loc_codes(ui_strings, isTable = False, 
                   source_json_path=LOCALIZATION_SOURCE_PATH):
    
    if isTable:
        ui_strings = re.split(r'[\n\t]+', ui_strings)
        ui_strings = [item.strip() for item in ui_strings if item.strip()]
    
    # 1. Load the Source JSON
    with open(source_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    # validating against the regex first and then searching in source file later
    ui_strings = validate_regex(ui_strings)


    # 2. Create a set of all valid localized "messages"
    # We use a set for lightning-fast lookups
    valid_messages = {item['message'] for item in source_data}

    leaks = []

    # 3. Compare UI strings against the valid messages
    for string in ui_strings:
        # Check if the UI string is missing from the message whitelist
        if string not in valid_messages:
            leaks.append(string)
        # Else: it exists in 'message', so we skip it (localized)

    return list(set(leaks))

def normalize_ui_text(raw_text: str) -> list[str]:
    """
    Split a big inner_text blob into individual strings, trimming
    and dropping empties. Works for normal pages and table-ish layouts.
    """
    parts = re.split(r'[\n\t]+', raw_text)
    return [p.strip() for p in parts if p.strip()]

def collect_page_text(page, root_selector: str = "#root") -> list[str]:
    """
    Fetch all visible text under a root selector and normalize it.
    You can override root_selector per page (e.g. '#divToPrint', 'body', etc.).
    """
    root = page.locator(root_selector)
    root.wait_for(state="visible", timeout=30000)
    raw = root.inner_text()
    return normalize_ui_text(raw)

def write_csv(data, filename):
    # Convert the list to a DataFrame
    df = pd.DataFrame(data, columns=["Locales"])
    
    # Save to CSV
    df.to_csv('target/resources/'+filename, index=False, quoting=csv.QUOTE_ALL , encoding='utf-8')

def write_json(data, filename):
    with open('target/resources/'+filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_table_data(page: None):

    tables = page.locator("table.MuiTable-root:visible")
    tables.first.locator("tbody tr").first.wait_for(state="visible", timeout=30000)
    table_count = tables.count()
    print(f"Found {table_count} tables.")
    table_data = ''
    for i in range(table_count):
        current_table = tables.nth(i)
        first_row = current_table.locator("tbody tr").first
        drill_down_link = first_row.locator("td").nth(1).locator("span").first
        drill_down_link.click(timeout=30000)
        time.sleep(2)
        table_headers = current_table.locator("thead tr").inner_text()
        table_data = table_data + table_headers + current_table.inner_text() if current_table.inner_text() else table_data
    return table_data

def get_logged_in_context(
                        browser_chr,
                        login_url: str,
                        creds: dict,
                        language: str = "English",
                        latitude: float = 31.6340,
                        longitude: float = 74.8723,
                        ):
    # --- Launch Chromium ---
    context = browser_chr.new_context(
                                        permissions=["geolocation"],
                                        geolocation={"latitude": latitude, "longitude": longitude},
                                    )
    page = context.new_page()
    login_pom = EmployeeLogin(page)

    page.goto(login_url)
    page.wait_for_load_state("networkidle")
    login_pom.select_language(language)
    page.wait_for_load_state("networkidle")
    login_pom.login_employee(
        username=creds.get("username"),
        password=creds.get("password"),
        tenant_id=creds.get("tenantId"),
    )
    page.wait_for_url("**/employee/inbox")
    page.wait_for_load_state("networkidle")
    page.close()
    return context
