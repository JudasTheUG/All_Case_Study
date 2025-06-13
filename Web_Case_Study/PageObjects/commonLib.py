import logging
import os
import time
import configparser
import inspect

from selenium.common import StaleElementReferenceException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Utilities import configReader
from Utilities.LogUtil import Logger

log = Logger(__name__, logging.INFO)


class CommonFunctions:
    wait = None
    last_opened_url = None
    base_url = ""
    second_url = ""

    _self = None

    def __new__(cls, driver):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 180)
        self.action = ActionChains(self.driver)

    def open(self, url):
        """
            open function records given url for further use
            and opens the same url using webdriver (chromedriver.exe)
            """
        self.last_opened_url = url
        self.driver.get(url)

    def site_is_open(self, keyword="none"):
        """
            site is open function controls url with given keyword to see if that url is the opened one
            :keyword is an optional parameter if it is not given last opened url is split by first "."(mostly after www)
            """
        if keyword == "none":
            control_part_of_url = self.last_opened_url.split(".")
            keyword = control_part_of_url[0]
            log.logger.info("Found keyword is : " + keyword)
        else:
            log.logger.info("Received keyword is : " + keyword)

        log.logger.info("current url : " + self.driver.current_url)
        if keyword in self.driver.current_url:
            assert True
        else:
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def is_element_visible(self, locator):
        """
            this function needs to be changed
            """
        element = self.element_finder(locator, 1)
        if element.is_displayed():
            log.logger.info(str(element) + " is visible on screen")
            assert True
        else:
            log.logger.info(str(element) + " is not visible on screen")
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def is_page_opened(self, my_page):
        """
            This function locates control element given in the ini page to validate the page is opened
            """
        try:
            if configReader.readConfig("control_element", my_page).startswith("//"):
                self.wait.until(
                    ec.presence_of_element_located((By.XPATH, (configReader.readConfig("control_element", my_page)))))
            elif configReader.readConfig("control_element", my_page).startswith("#"):
                self.wait.until(ec.presence_of_element_located(
                    (By.CSS_SELECTOR, (configReader.readConfig("control_element", my_page)))))
            else:
                self.wait.until(
                    ec.presence_of_element_located((By.ID, (configReader.readConfig("control_element", my_page)))))

            log.logger.info(str(my_page) + " has been opened")
            assert True
        except Exception as ex:
            print(str(ex))
            log.logger.info(str(my_page) + " could not be opened")
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def element_finder(self, locator, index=0):
        """
            this function used to find web elements with locator defined in Elements file
            :index is an optional parameter if send function returns a single web element
            if it is not send then function returns a web element list
            """
        element = None
        if index != 0:
            if configReader.readConfig("locators", locator).startswith("//"):
                element = self.driver.find_elements(By.XPATH, (configReader.readConfig("locators", locator)))[index - 1]
            elif configReader.readConfig("locators", locator).startswith("#"):
                element = self.driver.find_elements(By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))[index - 1]
            elif configReader.readConfig("locators", locator).startswith("document"):
                element = self.driver.execute_script("return " + configReader.readConfig("locators", locator))
            else:
                element = self.driver.find_elements(By.ID, (configReader.readConfig("locators", locator)))[index - 1]
            log.logger.info("Found an element named : " + str(locator))
        else:
            if configReader.readConfig("locators", locator).startswith("//"):
                element = self.driver.find_elements(By.XPATH, (configReader.readConfig("locators", locator)))
            elif configReader.readConfig("locators", locator).startswith("#"):
                element = self.driver.find_elements(By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))
            elif configReader.readConfig("locators", locator).startswith("document"):
                element = self.driver.execute_script("return " + configReader.readConfig("locators", locator))
            else:
                element = self.driver.find_elements(By.ID, (configReader.readConfig("locators", locator)))
            log.logger.info("Found multiple elements named : " + str(locator))
        return element

    def element_finder_by_attribute(self, locator, attribute, value):
        """
            this function used to find web elements with locator, and an attribute belongs to that element
            locator, attribute and value parameters past and after locating elements(with given locator) that has the given attribute
            we check its value with the given the value
            """
        element = None
        if configReader.readConfig("locators", locator).startswith("//"):
            elements = self.driver.find_elements(By.XPATH, (configReader.readConfig("locators", locator)))
        elif configReader.readConfig("locators", locator).startswith("#"):
            elements = self.driver.find_elements(By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))
        elif configReader.readConfig("locators", locator).startswith("document"):
            elements = self.driver.execute_script("return " + configReader.readConfig("locators", locator))
        else:
            elements = self.driver.find_elements(By.ID, (configReader.readConfig("locators", locator)))
        if len(elements) > 0:
            log.logger.info("Found multiple elements named : " + str(locator))
        else:
            log.logger.info("no element named : " + str(locator) + " has been found.")
        for item in elements:
            log.logger.info(item.text)
            if attribute.upper() == "TEXT" and item.text == str(value):
                log.logger.info("found item value :  " + item.text)
                log.logger.info("searched value :  " + str(value))
                element = item
                break
            elif str(item.get_attribute(attribute)) == str(value):
                element = item
                log.logger.info("found item value :  " + str(item.get_attribute(attribute)))
                log.logger.info("searched value :  " + str(value))
                break
        return element

    def element_click(self, locator, index):
        """
            This function uses element finder function to find the web element and clicks on the found element
            both :locator and :index parameters are mandatory because click function can be called on singe object
            """
        try:
            element = self.element_finder(locator, index)
            element.click()
            log.logger.info(str(locator) + " element clicked")
            assert True
        except StaleElementReferenceException:
            self.dynamic_wait_till_element_clickable(locator)
            self.element_click(locator, index)
        except Exception as ex:
            log.logger.info("exception : " + str(ex))
            log.logger.info(str(locator) + " element is not clickable")
            log.logger.info(inspect.currentframe().f_code.co_name)
            log.logger.info(str(inspect.currentframe().f_code.co_name))
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False


    @staticmethod
    def clear_text_field(element):
        """
            This function takes an element as parameter.
            on found element we send keys ctrl+a to choose all and delete key to delete any existing writings on that area
            """
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)

    def enter_text_in_textfield(self, value, locator, index=1):
        """
            This function uses element finder to find element we will enter given text
            and uses clear text field to clean existing entries
            then send :value parameter to the found element
            """
        try:
            element = self.element_finder(locator, index)
            self.clear_text_field(element)
            if value == "<PSR>":
                self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
            else:
                element.send_keys(value)
            log.logger.info(str(value) + " sent to " + str(locator) + " element")
            assert True
        except Exception as ex:
            log.logger.info("Couldn't fill the " + str(locator) + " element")
            log.logger.info(str(ex))
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False


    @staticmethod
    def wait_some_time(number_of):
        """
            This function is a static wait function that makes program wait until given number of seconds has passed
            """
        time.sleep(number_of)
        log.logger.info("waited " + str(number_of) + " seconds")

    def wait_until_page_is_fully_loaded(self):
        """
            This function uses javascript function to get document state of the page and checks if it is complete
            On general when a page is fully loaded page(document) sets its ready state as complete
            """
        try:
            self.wait.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
            log.logger.info("Page loaded successfully")
            assert True
        except:
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def dynamic_wait_till_element_visible(self, locator):
        """
            This function used to wait until element is visible on users screen
            """
        if configReader.readConfig("locators", locator).startswith("//"):
            self.wait.until(ec.visibility_of_element_located((By.XPATH, (configReader.readConfig("locators", locator)))))
        elif configReader.readConfig("locators", locator).startswith("#"):
            self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))))
        else:
            self.wait.until(ec.visibility_of_element_located((By.ID, (configReader.readConfig("locators", locator)))))

        log.logger.info("Waited : " + str(locator) + " is visible")


    def dynamic_wait_till_element_invisible(self, locator):
        """
            This function used to wait until element is invisible on users screen and waits 5 seconds before starting to check
            """
        try:
            if configReader.readConfig("locators", locator).startswith("//"):
                waiter = self.wait.until(ec.invisibility_of_element_located((By.XPATH, (configReader.readConfig("locators", locator)))))
            elif configReader.readConfig("locators", locator).startswith("#"):
                waiter = self.wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))))
            else:
                waiter = self.wait.until(ec.invisibility_of_element_located((By.ID, (configReader.readConfig("locators", locator)))))

            log.logger.info("Waited : " + str(locator) + " is invisible")

        except:
            log.logger.info(locator + " element is visible")
            assert True

    def dynamic_wait_till_element_clickable(self, locator):
        """
            This function used to wait until element is clickable
            """
        if configReader.readConfig("locators", locator).startswith("//"):
            self.wait.until(ec.element_to_be_clickable((By.XPATH, (configReader.readConfig("locators", locator)))))
        elif configReader.readConfig("locators", locator).startswith("#"):
            self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))))
        else:
            self.wait.until(ec.element_to_be_clickable((By.ID, (configReader.readConfig("locators", locator)))))

        log.logger.info("Waited : " + str(locator) + " can be clicked")

    def dynamic_wait_till_element_present(self, locator):
        """
            This function used to wait until element is present on page DOM;
            Page DOM is Elements tab on developer tools (page you enter by clicking on f12 or RMB and inspect on web browser)
            """
        if configReader.readConfig("locators", locator).startswith("//"):
            self.wait.until(ec.presence_of_element_located((By.XPATH, (configReader.readConfig("locators", locator)))))
        elif configReader.readConfig("locators", locator).startswith("#"):
            self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, (configReader.readConfig("locators", locator)))))
        else:
            self.wait.until(ec.presence_of_element_located((By.ID, (configReader.readConfig("locators", locator)))))

        log.logger.info("Waited : " + str(locator) + " is present")

    def dynamic_wait_till_element_not_present(self, element):
        """
            This function used to wait until element is not present on page DOM
            every second function checks page DOM to see if element is present if it is it calls itself again
            if it isn't present we end the function successfully
            """
        wait_time = WebDriverWait(self.driver, 5)
        try:
            if configReader.readConfig("locators", element).startswith("//"):
                waiter = wait_time.until(
                    ec.presence_of_element_located((By.XPATH, (configReader.readConfig("locators", element)))))
            elif configReader.readConfig("locators", element).startswith("#"):
                waiter = wait_time.until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, (configReader.readConfig("locators", element)))))
            else:
                waiter = wait_time.until(ec.presence_of_element_located((By.ID, (configReader.readConfig("locators", element)))))

            if waiter is not None:
                self.dynamic_wait_till_element_not_present(element)
            else:
                log.logger.info(element + " element is not present in Page DOM")
                assert True
        except:
            log.logger.info(element + " element is not present in Page DOM")
            assert True

    def hover_on(self, locator, index):
        """
            This function uses element finder function to find element by :locator
            Then hovers mouse indicator on that element
            """
        element = self.element_finder(locator, index)
        self.hover_on_element(element)

    def hover_on_element(self, element):
        """
            This function used to hovers mouse indicator on given :element
            """
        try:
            self.action.move_to_element(element).perform()
            log.logger.info("Moving to element: " + str(element))
            assert True
        except:
            log.logger.info("Couldn't move to element: " + str(element))
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def get_all_options(self, locator):
        """
            This function is uses element finder function to find Select element
            And used to get all options for that select element
            """
        select = Select(self.element_finder(locator, 1))
        all_options = select.options
        return all_options

    def get_selected_option(self, locator):
        """
            This function is uses element finder function to find Select element
            And used to get current selected option for that select element
            """
        select = Select(self.element_finder(locator, 1))
        selected_option = select.first_selected_option
        return selected_option


    def select_by_text(self, locator, value):
        """
            This function is uses element finder function to find Select element
            And used to choose an option by visible text :value
            """
        dropdown_menu = self.element_finder(locator, 1)
        select = Select(dropdown_menu)
        select.select_by_visible_text(value)
        time.sleep(0.5)  # for users to be able to see
        log.logger.info("Selecting from an element: " + str(locator) + " value selected as : " + str(value))

    def select_by_value(self, locator, value):
        """
            This function is uses element finder function to find Select element
            And used to choose an option by value attribute :value
            """
        dropdown_menu = self.element_finder(locator, 1)
        select = Select(dropdown_menu)
        select.select_by_value(value)
        log.logger.info("Selecting from an element: " + str(locator) + " value selected as : " + str(value))

    def scroll_into_view_by_element(self, element):
        """
            This Function takes an :element as a parameter and scrolls that element using basic java script code
            """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        log.logger.info("Scrolled to the element : " + str(element))

    def scroll_into_view(self, locator, index):
        """
            This function uses element finder function to find element by :locator
            and uses scroll into view by element function to scroll that element
            """
        element = self.element_finder(locator, index)
        self.scroll_into_view_by_element(element)

    def select_from_combobox(self, locator, attribute, value, replace_element_path=False):
        """
            This function is created selecting an item from combobox(listbox etc.)
            Before using this function we need to click on element to open element list
            After that this function will use dynamic wait till element present function to wait until element is present,
            and it uses element finder function to locate the element
            then uses scroll into view by element function to scroll that element then selects that element by clicking on it
            """
        self.dynamic_wait_till_element_present(locator)
        element = self.element_finder_by_attribute(locator, attribute, value)
        self.scroll_into_view_by_element(element)
        # for user to be able to see the scroll if necessary
        time.sleep(1)
        element.click()

    def check_value_in_input_area(self, locator, attribute, value):
        """
            After that this function will use dynamic wait till element present function to wait until element is present,
            and it uses element finder by attribute function to locate the element
            then check if we found any element if we found that means given value checks out
            """
        self.dynamic_wait_till_element_present(locator)
        element = self.element_finder_by_attribute(locator, attribute, value)
        if element is not None:
            log.logger.info("Values checks out")
            assert True
        else:
            log.logger.info("Values are different")
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False

    def is_element_exist(self, locator, attribute="none", value="default"):
        """
            This element uses element finder or element finder by attribute function according to given parameters
            attribute and value is optional parameters if it is given function uses element finder by attribute function
            otherwise uses element finder function
            Default value of element is none, so we check according to that
            """
        if attribute == "none":
            element = self.element_finder(locator)
            if not element:
                log.logger.info(str(locator) + " element is not exist in the page DOM")
                self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                assert False
            else:
                log.logger.info(str(locator) + " element is exist in the page DOM")
                assert True
        else:
            element = self.element_finder_by_attribute(locator, attribute, value)
            if element is not None:
                log.logger.info(str(locator) + " element is exist in the page DOM")
                assert True
            else:
                log.logger.info(str(locator) + " element is not exist in the page DOM")
                self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                assert False

    def is_element_not_exist(self, locator, attribute="none", value="default"):
        """
            This function si basically negative of is element exist function
            This element uses element finder or element finder by attribute function according to given parameters
            attribute and value is optional parameters if it is given function uses element finder by attribute function
            otherwise uses element finder function.
            Default value of element is none, so we check according to that
            """
        if attribute == "none":
            element = self.element_finder(locator)
            if not element:
                log.logger.info(str(locator) + " element is not exist in the page DOM")
                assert True
            else:
                log.logger.info(str(locator) + " element is exist in the page DOM")
                self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                assert False
        else:
            element = self.element_finder_by_attribute(locator, attribute, value)
            if element is None:
                log.logger.info(str(locator) + " element is not exist in the page DOM")
                assert True
            else:
                log.logger.info(str(locator) + " element is exist in the page DOM")
                self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                assert False

    def drag_and_drop(self, source, destination, src_index=1, dest_index=1):
        """
            This function finds elements with element finder function
            then uses drag and drop action from :source to :destination
            """
        src = self.element_finder(source, src_index)
        dest = self.element_finder(destination, dest_index)
        self.action.drag_and_drop(src, dest).perform()
        # self.action.click_and_hold(src).pause(1).move_to_element(dest).pause(1).release(src).pause(1).perform()
        time.sleep(1)  # static waiting is for user to see the action for performance it can be removed

    def change_tabs(self, index):
        """
        This function changes active on browser according to which tab users wants to open
        """
        if index - 1 == 0:
            self.driver.switch_to.window(self.driver.window_handles[0])
            log.logger.info("Main tab is opened")
            assert True
        elif index - 1 > 0:
            self.driver.switch_to.window(self.driver.window_handles[index - 1])
            log.logger.info("Tab " + str(index) + " is opened")
            assert True
        else:
            log.logger.info("Something went wrong check tab index on feature file")
            self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
            assert False


    def is_field_contains_searched_word(self, element, text, index=0, attribute=None):
        """
        This function uses element finder to finder web element and check its attribute value.
        Attribute considered as text and index considered as 1 if not given as parameters.
        """
        searched_field = self.element_finder(element, index)
        if attribute is None:
            if index!=0:
                if text in searched_field.text:
                    log.logger.info("Searched word : " + text + " found in " + element + " field")
                    assert True
                else:
                    log.logger.info("Searched word : " + text + " could not be found in " + element + " field")
                    self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                    assert False
            else:
                counter = 0
                for entry in searched_field:
                    counter += 1
                    if text in entry.text:
                        log.logger.info("Searched word : " + text + " found in " + element + " at index " + str(counter))
                    else:
                        log.logger.info("Searched word : " + text + " could not be found in " + element + " field")
                        self.take_whole_screenshot(image_save_name=inspect.currentframe().f_code.co_name)
                        assert False

                    assert True

        else:
            if index != 0:
                counter = 0
                for entry in searched_field:
                    counter += 1
                    result = text in str(entry.get_attribute(attribute))
                    if result:
                        log.logger.info(element + " field " + attribute + "  attribute contains " + text + " at index " + str(counter))
                        assert result
                    else:
                        log.logger.info(element + " field " + attribute + "  attribute does not contains " + text + " search word")
                        assert result

                assert counter == len(searched_field)
            else:
                result = text in str(searched_field.get_attribute(attribute))
                if result:
                    log.logger.info(element + " field " + attribute + "  attribute contains " + text + " search word")
                    assert result
                else:
                    log.logger.info(
                        element + " field " + attribute + "  attribute does not contains " + text + " search word")
                    assert result

    def take_screenshot_of_element(self, element, image_save_name):
        image_path = "./Screenshots/" + str(image_save_name) + ".png"
        if os.path.isfile(image_path):
            os.remove(image_path)
        ss_element = self.element_finder(element, 1)
        ss_element.screenshot(image_path)

    def take_whole_screenshot(self, image_save_name):
        image_path = "./Screenshots/" + str(image_save_name) + ".png"
        self.driver.save_screenshot(image_path)
