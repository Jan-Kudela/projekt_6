from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        yield page

def cookie_bar_accept():
    page.goto("https://kytary.cz/")
    accept_button = page.locator(
        "#cpModal > div > div > div > div.btns > a.btn.btn-success"
        )
    accept_button.click()
    yield


def test_accept_cookies(page: Page):
    '''Testuje, zda po kliknuti na tlačítko "Povolit vše", zmizí cookie bar'''
    
    cookie_bar_accept()
    
    cookie_bar = page.locator("#modal-body")

    assert cookie_bar.is_visible() == False


def test_login_window(page: Page):
    '''Testuje, zda se po kliknuti na tlacitko Můj účet
      zobrazi prihlasovaci okno'''
    
    page.goto("https://kytary.cz/")
    cookies_ok = page.locator(
        "#cpModal > div > div > div > div.btns > a.btn.btn-success"
        )
    cookies_ok.click()

    account_button = page.locator(".m-icons a:nth-of-type(3) .desc")
    account_button.click()

    login_window = page.locator("#loginModal .modal-title")

    assert login_window.is_visible() == True


