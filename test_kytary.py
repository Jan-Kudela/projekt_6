from playwright.sync_api import Page, sync_playwright
import pytest

@pytest.fixture
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        yield page


def accept_cookies(page: Page):
    '''Funkce pro kliknuti na tlacitko "Povolit vše" v cookie baru'''
    
    accept_button = page.locator("#cpModal .btn-success")
    accept_button.click()


def necessary_cookies(page: Page):
    '''Funkce pro kliknuti na tlacitko "Povolit nezbytné" v cookie baru'''
    
    cookies_necessary = page.locator("text='Povolit nezbytné'")
    cookies_necessary.click()


def test_accept_cookies(page: Page):
    '''Testuje, zda po kliknuti na tlačítko "Povolit vše", zmizí cookie bar'''
    
    page.goto("https://kytary.cz/")

    accept_cookies(page)
    
    cookie_bar = page.locator("#modal-body")

    assert cookie_bar.is_visible() == False


def test_login_window(page: Page):
    '''Testuje, zda se po kliknuti na tlacitko Můj účet
      zobrazi prihlasovaci okno'''
    
    page.goto("https://kytary.cz/")
    necessary_cookies(page)

    account_button = page.locator(".m-icons a:nth-of-type(3) .desc")
    account_button.click()

    login_window = page.locator("#loginModal .modal-title")

    assert login_window.is_visible() == True


def test_hover_kytary(page: Page):
    '''Testuje, zda se po najetí myší na tlačítko Kytary v horizontálním menu
      zobrazi drop-down menu s kategoriemi'''
    
    page.goto("https://kytary.cz/")
    necessary_cookies(page)

    kytary_button = page.locator(
        "#categories > div > nav > ul > li:nth-child(1) > a > span.lbl"
    )
    kytary_button.hover()

    dropdown_menu = page.locator(
        "#categories > div > nav > ul > li:nth-child(1)"
        " > div > div > div.r6.hlnks > a:nth-child(3) > span.lbl"
    )
    assert dropdown_menu.is_visible() == True


def test_valid_error_message(page: Page):
    '''Testuje, zda se po zadání korektního emailu a špatného hesla 
    objeví validační chybová hláška v okně Přihlášení'''

    page.goto("https://kytary.cz/")
    necessary_cookies(page)

    account_button = page.locator(".m-icons a:nth-of-type(3) .desc")
    account_button.click()

    page.fill("#Login_LoginName", "karel@seznam.cz")
    page.fill("#Login_Password", "tohlehesloneuhadnu")
    
    button = page.locator("#loginModal input[type='submit']")
    button.press("Enter")
    validation_error = page.locator(".validation-error")

    assert validation_error.is_visible() == True

      

