import os, time, subprocess, random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


"""
Important links:
https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html
"""


class WebdriverChauffeurMixin(object):

    @property
    def soup(self, **kwargs):
        return BeautifulSoup(self.page_source, 'html.parser')

    def locate_element(self, search_text=None, xpath=None):
        if not xpath:
            xpaths = [
                "//input[@value='{text}']",
                "//button[normalize-space(text())='{text}']",
                "//a[child::span[normalize-space(text())='{text}']]",
                "//a[normalize-space(text())='{text}']",
                # "//button[contains(.,'{text}')]",
                # "//input[contains(.,'{text}')]",
                "//*[contains(@id,'{text}')]",
                "//*[contains(@class,'{text}')]",
                "//*[contains(.,'{text}')]",
            ]
        else:
            return self.find_element_by_xpath(xpath)
        try:
            return self.find_element_by_id(search_text)
        except:
            try:
                return self.find_element_by_name(search_text)
            except:
                try:
                    return self.find_element_by_class_name(search_text)
                except:
                    for path in xpaths:
                        try:
                            return self.find_element_by_xpath(path.format(text=search_text))
                        except:
                            pass
        return None

    @property
    def active_element(self):
        return self.switch_to_active_element()

    def tab_through(self):
        self.active_element.send_keys(Keys.TAB)

    def click_active_by_hitting_enter(self):
        self.active_element.send_keys(Keys.ENTER)

    def activate_hidden_element(self, search_text=None):
        action = webdriver.ActionChains(self)
        element = self.locate_element(search_text)
        action.move_to_element(element).click().perform()
        return element

    def access_link(self, search_text=None):
        element = self.locate_element(search_text)
        link  = element.get_attribute('href')
        self.get(link)

    def submit_form(self, search_text=None):
        form = self.locate_element(search_text)
        form.submit()

    def click_button(self, search_text=None, xpath=None):
        element = self.locate_element(search_text, xpath)
        try:
            element.click()
        except:
            self.mouse.move_to_element(element).click().perform()

    @property
    def mouse(self):
        return webdriver.ActionChains(self)

    def find_box_and_fill(self, value=None, search_text=None, xpath=None):
        """locate_element can take search text or xpath"""
        box = self.locate_element(search_text=search_text, xpath=xpath)
        try:
            box.clear()
        except:
            pass
        box.send_keys(value)

    def find_box_and_fill_as_person(self, search_text=None, value=None):
        box = self.locate_element(search_text)
        for character in value:
            box.send_keys(character)
            self.sleep_random(5, 12)

    def sleep_random(self, start, end):
        time.sleep(self.get_random_time(start, end))

    def get_random_time(self, start, end):
        diff = end - start
        random_num = int((random.SystemRandom(random.seed()).random()) * diff)
        actual_num = (random_num + start)
        return self.convert_num_to_secs(actual_num)

    def convert_num_to_secs(self, num):
        """takes a number like 89 and converts it to 0.89 seconds"""
        return (float(num)/float(100))

    def pick_select_box(self, search_text=None, value=None):
        element = self.locate_element(search_text)
        select_bot = Select(element)
        select_bot.select_by_value(value)

    def pick_radio_button(self, value):
        try:
            value.click()
        except AttributeError:
            element = self.locate_element(value)
            element.click()

    def cycle_through_tabs(self):
        self.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

    def open_new_tab(self):
        self.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

    def complete_field(self, selection, search_text):
        # TODO: the minor 'AI' function that tries to predict the value to input should be
        #       separate from the logic to make the selection
        #       (based on tag type like input, select, checkbox, etc)

        # selection can be True or False for checkbox, text for input box, etc
        try:
            selection = getattr(selection, search_text)
        except:
            pass
        if not isinstance(selection, bool):
             selection = str(selection)
        element = self.locate_element(search_text)
        tag_type = element.tag_name
        if tag_type == 'input':
            input_type = element.get_attribute('type')
            if input_type == 'checkbox':
                if selection:
                    self.click_anything(search_text)
            elif input_type in ['text', 'textarea', 'number']:
                self.find_box_and_fill(selection, search_text=search_text)
            else:
                raise Exception('Unknown input HTML element type')
        elif tag_type == 'select':
            if isinstance(selection, bool):
                selection = "1" if selection else "0"
            self.pick_select_box(value=selection, search_text=search_text)
        elif tag_type == 'textarea':
            self.find_box_and_fill(selection, search_text=search_text)
        else:
            if not selection:
                return None
            else:
                raise Exception('Unknown HTML element type')
        self.basic_sleep('short')

    def basic_sleep(self, length=None):
        if length == 'short':
            self.sleep_random(120, 250)
        elif length == 'long':
            self.sleep_random(700, 1000)
        else:
            self.sleep_random(300, 700)

    def wait(self, search_item=None):
        # search_type like id, name, xpath, etc
        BY_MAP = {
        'id': By.ID,
        'name': By.NAME,
        'class': By.CLASS_NAME,
        'xpath': By.XPATH,
        }
        HTML_ELEMENT_BY_STYLES = [By.ID, By.NAME, By.CLASS_NAME, By.XPATH]
        ready = False
        # since each check waits 0.2 seconds, the total wait time is WAIT_TIME * 5
        WAIT_TIME = 15 # seconds
        for i in range(int(WAIT_TIME * 5)):
            if ready == True:
                break
            for by_element in HTML_ELEMENT_BY_STYLES:
                try:
                    WebDriverWait(self, 0.2).until(EC.presence_of_element_located((by_element, search_item)))
                    ready = True
                    break
                except TimeoutException:
                    pass

    def text_is_on_page(self, text):
        return text in self.soup.encode_contents()


class ChromeDriver(WebdriverChauffeurMixin, webdriver.Chrome):
    pass


class FirefoxDriver(WebdriverChauffeurMixin, webdriver.Firefox):
    pass
