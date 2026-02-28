# Playwright Automation

UI test automation suite built with `pytest` + `playwright` for eGov employee flows, with localization-leak detection and JSON/CSV exports.

## What This Project Covers

- Employee portal login and language-selection flows
- Trade License landing-page localization checks
- Dashboard (DSS) localization checks
- Shared fixtures for browser/session/login setup
- Allure result generation

## Project Structure

- `tests/ui/`
- UI test cases (`test_login.py`, `test_tradelicence.py`, `test_dashboard.py`)
- `tests/api/`
- API tests (currently placeholder)
- `fixtures/browser_fixtures.py`
- Browser and page fixtures (`browser_chr`, `page_chr`)
- `fixtures/tl_ui_fixture.py`
- Logged-in Trade License context fixture (`tl_context`)
- `utils/helpers.py`
- Config readers, localization leak finder, output writers
- `config.json`
- Environment host and credential config
- `target/resources/`
- Localization output files (for example `TL_locales.json`, `DSS_locales.json`)
- `output/allure-results/`
- Raw Allure test results

## Prerequisites

- Python `3.10+` (recommended)
- `pip`
- Playwright browser binaries

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Install Playwright browser binaries.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Configuration

Update `config.json` before running tests:

- `host`: target application base URL
- `credentials.TL_EMP.username`
- `credentials.TL_EMP.password`
- other keys as needed by your environment

Example access in code:

- `helpers.get_env("host")`
- `helpers.get_creds("TL_EMP")`

## Running Tests

Run all tests:

```bash
pytest
```

Run only UI tests:

```bash
pytest -m ui
```

Run a single test file:

```bash
pytest tests/ui/test_tradelicence.py -v
```

Run a single test:

```bash
pytest tests/ui/test_tradelicence.py::test_tl_landing_page -v
```

## Localization Code Workflow

1. Test collects visible UI strings.
2. Strings are compared with source messages from:
   - `target/resources/source.json`
3. Missing keys/messages are filtered and exported.

Writers in `utils/helpers.py`:

- `write_json(...)` -> `target/resources/*.json`
- `write_csv(...)` -> `target/resources/*.csv`

## Fixtures Overview

`tests/conftest.py` registers fixture modules:

- `fixtures.browser_fixtures`
- `fixtures.tl_ui_fixture`

Fixture chain for logged-in TL scenarios:

- `browser_chr` -> creates browser
- `tl_context(browser_chr)` -> logs in once and yields authenticated context
- tests call `page = tl_context.new_page()`

## Reporting

`pytest.ini` is configured with:

- `--alluredir=output/allure-results`

After a run, generate/open report (if Allure CLI installed):

```bash
allure serve output/allure-results
```

## Notes

- Current UI tests are sync Playwright style.
- Keep secrets out of Git; avoid committing real credentials in `config.json`.
- Use markers (`ui`, `api`, `localization`, `smoke`) to scope executions.
