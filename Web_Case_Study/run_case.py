import json
import logging
import os
import time
from time import gmtime, strftime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from PageObjects.commonLib import CommonFunctions
from Utilities.LogUtil import Logger
from dotenv import load_dotenv

load_dotenv(".env.development")
log = Logger(__name__, logging.INFO)

driver=None
web_browser = os.environ["CHOSEN_BROWSER"]

site_url = "https://useinsider.com/"
second_site_url = "https://useinsider.com/careers/quality-assurance/"

def before_scenario():
    global driver
    if web_browser == "chrome":
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation'])
        option.add_argument('--lang=en-US')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-popup-blocking')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-add-to-shelf')
        option.add_argument('--disable-domain-reliability')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-blink-Features=AutomationControlled')
        option.add_argument('--js-flags=--max-old-space-size=6144')
        option.add_argument("--window-size=1920,1200")
        option.add_argument("--allow-insecure-localhost")
        option.add_argument("--log-level=3")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

    else:
        option = webdriver.FirefoxOptions()
        option.set_preference("intl.accept_languages", "en-US")
        option.add_argument("--width=1920")
        option.add_argument("--height=1200")
        option.add_argument("--log-level=3")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=option)

    driver.maximize_window()


def after_scenario():
    global driver
    # noinspection PyUnresolvedReferences
    driver.quit()
    driver = None

def main_scenario():
    global driver
    common = CommonFunctions(driver)
    # Step 1
    common.open(site_url)
    common.wait_until_page_is_fully_loaded()
    common.dynamic_wait_till_element_present("demo button")
    common.is_page_opened("entry page")
    # Step 2
    common.hover_on("Company dropdown", 1)
    common.element_click("Careers link", 1)
    common.wait_until_page_is_fully_loaded()
    common.is_page_opened("careers page")
    common.dynamic_wait_till_element_present("Teams")
    common.scroll_into_view("Teams", 1)
    common.is_element_visible("Teams")
    common.scroll_into_view("Locations", 1)
    common.is_element_visible("Locations")
    common.scroll_into_view("Life at insider", 1)
    common.is_element_visible("Life at insider")
    # Step 3
    common.open(second_site_url)
    common.wait_until_page_is_fully_loaded()
    common.dynamic_wait_till_element_present("See all QA jobs button")
    common.is_page_opened("qa page")
    common.element_click("See all QA jobs button", 1)
    common.wait_until_page_is_fully_loaded()
    common.is_page_opened("positions page")
    common.element_click(locator="location select", index=1)
    common.dynamic_wait_till_element_present("select options")
    common.select_from_combobox(locator="select options", attribute="text", value="Istanbul, Turkiye")
    common.element_click(locator="department select", index=1)
    common.dynamic_wait_till_element_present("select options")
    common.select_from_combobox(locator="select options", attribute="text", value="Quality Assurance")
    common.wait_until_page_is_fully_loaded()
    common.is_element_exist(locator="positions list item")
    # Step 4
    common.is_field_contains_searched_word(element="job location area", text="Istanbul, Turkiye")
    common.is_field_contains_searched_word(element="job department area", text="Quality Assurance")
    common.is_field_contains_searched_word(element="job title area", text="Quality Assurance")
    common.wait_until_page_is_fully_loaded()
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 2);")
    common.scroll_into_view("position title", 1)
    common.wait_until_page_is_fully_loaded()
    common.hover_on("positions list item", 1)
    common.element_click("View Role button", 1)
    common.change_tabs(2)
    common.wait_until_page_is_fully_loaded()
    common.site_is_open(keyword="lever")

if __name__ == '__main__':
    before_scenario()
    main_scenario()
    after_scenario()