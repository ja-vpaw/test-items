import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default="ru, en",
                     help="Choose preferred page language")

@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption("browser_name")
    language = request.config.getoption("language")

    def chrome_setup():
        opt = ChromeOptions()
        opt.add_experimental_option('w3c', False)
        opt.add_experimental_option('prefs', {'intl.accept_languages': language})
        browser = webdriver.Chrome(options=opt)
        return browser

    def firefox_setup():
        opt = FirefoxOptions()
        opt.add_argument('--browser')
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages" , language)
        browser = webdriver.Firefox(firefox_profile=firefox_profile, options=opt)
        return browser

    print("\nstart browser for test..")
    if browser_name == "chrome":
        browser = chrome_setup()
    elif browser_name == "firefox":
        browser = firefox_setup()
    else:
        print("Browser {} still is not implemented".format(browser_name))
        raise Exception

    yield browser

    print("\nquit browser..")
    browser.quit()
