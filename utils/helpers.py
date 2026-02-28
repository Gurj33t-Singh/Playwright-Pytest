import time
import pandas as pd
import csv, json
import re

LOCALIZATION_SOURCE_PATH = 'target/resources/source.json'
CONFIG_PATH = "config.json"

def get_env(conf_key=None):
    """Returns specific key value pair from env_config"""
    with open(CONFIG_PATH) as f:
        env_config = json.load(f)
    return env_config.get(conf_key) if conf_key else env_config

def get_creds(user):
    """Returns credentials of a specific user"""
    creds = get_env("credentials")
    return creds.get(user)

def validate_regex(string_list):
    pattern = r'^(?![0-9\s,%.]+$).*[_.].*'
    # POSITIVE: Must contain at least one of these characters
    INCLUDE_PATTERN = re.compile(r'[_.]')

    # NEGATIVE: Matches strings that are ONLY numbers, commas, spaces, dots, or %
    # We use ^ and $ to ensure the ENTIRE string matches this "junk" profile
    EXCLUDE_NUMERIC_ONLY = re.compile(r'^[0-9\s,%.]+$')
    # return [item for item in string_list if re.search(pattern, item)]
    return [
        item for item in string_list 
        if INCLUDE_PATTERN.search(item) 
        and not EXCLUDE_NUMERIC_ONLY.match(item)
    ]

def find_loc_codes(ui_strings, 
                   isTable = False, 
                   source_json_path=LOCALIZATION_SOURCE_PATH):
    
    if isTable:
        ui_strings = re.split(r'[\n\t]+', ui_strings)
        ui_strings = [item.strip() for item in ui_strings if item.strip()]
    
    # 1. Load the Source JSON
    with open(source_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

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

    return validate_regex(leaks)

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
