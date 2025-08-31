from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        yield page


def test_cookies(page: Page):

    page.goto("https://kytary.cz/")
    decline_button = page.locator("a.btn.btn-success")
    decline_button.click()

    cookie_bar = page.locator("#cpModal > div > div > div")

    assert cookie_bar.is_visible() == False