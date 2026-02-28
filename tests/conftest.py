# Import all fixtures from fixtures folder so they're available to tests
pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.tl_ui_fixture",
]
