import json
import logging
from random import randint
from time import time, sleep, localtime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM

DEFAULT_IMPLICIT_WAIT = 1


class InstaDM(object):

    def __init__(self, username, password, headless=True, instapy_workspace=None, profileDir=None):

        self.userDataMap = {}
        self.resultData = []
        self.resultData.append(["username", "fans", "desc", "country", "pic"])
        with open('infos/usernames.txt', 'r') as f:
            self.usernames = [line.strip() for line in f]
        f = open('infos/config.json', )
        self.botConfig = json.load(f)

        self.selectors = {
            "suggestedCollapseBtn": "//*[local-name() = 'svg' and @aria-label='Down chevron icon']",
            "countryInfoBtn": "//*[local-name() = 'svg' and @aria-label='Options']",
            "accountInfoBtn": "//button[text()='About this account' or text()='帐户简介']",
            "nextBtn": "//button[@aria-label='Next' or @aria-label='下一步']",
            "seeAllBtn": "//main/div/div[2]/div/a",
            "recUsersTitle": "//div[@role='presentation']//li/div/div/div/div/div[2]/div[1]/a/div",
            "fans_num": "//main/div/header/section/ul/li[2]/a/div/span",
            "desc": "//main/div/header/section/div[3]",
            "search_input_button": "//input[@placeholder='Search']/..",
            "search_input_area": "//input[@placeholder='Search']",
            "accept_cookies": "//button[text()='Accept']",
            "home_to_login_button": "//button[text()='Log In']",
            "username_field": "username",
            "password_field": "password",
            "button_login": "//button/*[text()='Log In']",
            "login_check": "//*[@aria-label='Home'] | //button[text()='Save Info'] | //button[text()='Not Now']",
            "search_user": "queryBox",
            "select_user": '//div[text()="{}"]',
            "name": "((//div[@aria-labelledby]/div/span//img[@data-testid='user-avatar'])[1]//..//..//..//div[2]/div[2]/div)[1]",
            "next_button": "//button/*[text()='Next']",
            "textarea": "//textarea[@placeholder]",
            "send": "//button[text()='Send']",
            "button_not_now": "//button[text()='Not Now']"
        }

        # Selenium config
        options = webdriver.ChromeOptions()

        if profileDir:
            options.add_argument("user-data-dir=profiles/" + profileDir)

        if headless:
            options.add_argument("--headless")

        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(
            executable_path=CM().install(), options=options)
        self.driver.set_window_position(0, 0)
        self.driver.maximize_window()

        try:
            self.driver.get('https://instagram.com/?hl=en')

            # 代码修改处
            cookies = self.extract_cookies(
                cookie=self.botConfig["cookie"])
            # cookie="mid=YdkfTgALAAEkbmcPqBufmiKyV3D5; ig_did=734B6C43-E743-461E-AEEF-6A635AD5BAAB; ig_nrcb=1; datr=uDgKY0maEvUCH6O4VjE1-JLp; csrftoken=AChKcT1cFCePhygWaZKlIG10FOfRFd8A; ds_user_id=50932469833; shbid=5886\05450932469833\0541695640111:01f7f0b84f4be8d39b54c3b48f855b552fcfb1a01e7c5fc4f5fbb49973aee454aa69c42a; shbts=1664104111\05450932469833\0541695640111:01f79238102d2d42b24ad4408478876b24154b4988c111dabe8748ceb6bfdc9d63e47bc7; sessionid=50932469833%3AQWOHIbc9E2oCz5%3A6%3AAYcWck8gvNNdWFPkcnG5eQkkTnxxy0D4b98JykF5mg; dpr=1.25; ig_lang=en; rur=NAO\05450932469833\0541695742589:01f72e8b338134d3aed5116c2dd676e012d137b8e71df887f9d20e9ea1684f7b51bdf8a7; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%221837a74b0975cd-0a23d81b26b53f-26021c51-240000-1837a74b0987e8%22%2C%22%24device_id%22%3A%20%221837a74b0975cd-0a23d81b26b53f-26021c51-240000-1837a74b0987e8%22%2C%22site_type%22%3A%20%22similarweb%20extension%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.instagram.com%2Faccounts%2Fedit%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.instagram.com%22%7D")
            # 代码结束

            year = localtime().tm_year + 1

            for key in cookies:
                cookie_dict = {
                    'domain': 'instagram.com',
                    'name': key,
                    'value': cookies[key],
                    "expires": 'Sat, 26 Aug ' + str(year) + ' 10:34:25 GMT',
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': True
                }
                self.driver.add_cookie(cookie_dict)

            self.driver.refresh()

            self.__random_sleep__(3, 5)
            if self.__wait_for_element__(self.selectors['button_not_now'], "xpath"):
                self.__get_element__(
                    self.selectors['button_not_now'], "xpath").click()
                self.__random_sleep__()
            while True:
                if not self.usernames:
                    break

                username = self.usernames.pop()
                self.searchUser(username)

        except Exception as e:
            logging.error(e)
            print(str(e))

    def __get_element__(self, element_tag, locator):
        """Wait for element and then return when it is available"""
        try:
            locator = locator.upper()
            dr = self.driver
            if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_id(element_tag))
            elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_name(element_tag))
            elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_xpath(element_tag))
            elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTOR, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_css_selector(element_tag))
            else:
                logging.info(f"Error: Incorrect locator = {locator}")
        except Exception as e:
            logging.error(e)
        logging.info(f"Element not found with {locator} : {element_tag}")
        return None

    def is_element_present(self, how, what):
        """Check if an element is present"""
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def __wait_for_element__(self, element_tag, locator, timeout=30):
        """Wait till element present. Max 30 seconds"""
        result = False
        self.driver.implicitly_wait(0)
        locator = locator.upper()
        for i in range(timeout):
            initTime = time()
            try:
                if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                    result = True
                    break
                elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                    result = True
                    break
                elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                    result = True
                    break
                elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTORS, element_tag):
                    result = True
                    break
                else:
                    logging.info(f"Error: Incorrect locator = {locator}")
            except Exception as e:
                logging.error(e)
                print(f"Exception when __wait_for_element__ : {e}")

            sleep(1 - (time() - initTime))
        else:
            print(
                f"Timed out. Element not found with {locator} : {element_tag}")
        self.driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
        return result

    def __type_slow__(self, element_tag, locator, input_text=''):
        """Type the given input text"""
        try:
            self.__wait_for_element__(element_tag, locator, 5)
            self.__wait_for_element__(element_tag, locator, 5)
            element = self.__get_element__(element_tag, locator)
            actions = ActionChains(self.driver)
            actions.click(element).perform()
            # element.send_keys(input_text)
            for s in input_text:
                element.send_keys(s)
                # sleep(uniform(0.005, 0.02))

        except Exception as e:
            logging.error(e)
            print(f'Exception when __typeSlow__ : {e}')

    def __random_sleep__(self, minimum=2, maximum=7):
        t = randint(minimum, maximum)
        logging.info(f'Wait {t} seconds')
        sleep(t)

    def __scrolldown__(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def teardown(self):
        self.driver.close()
        self.driver.quit()

    def extract_cookies(self, cookie=""):
        """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
        return cookies

    def __find_element_and_click(self, name, locator):
        if self.__wait_for_element__(name, locator):
            self.__get_element__(
                name, locator).click()
            self.__random_sleep__()

    def searchUser(self, username):
        userLink = f'https://www.instagram.com/{username}'
        # open new tab for fetch info
        newWindow = f'window.open("{userLink}")'
        self.driver.execute_script(newWindow)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[len(handles) - 1])
        self.__random_sleep__()

        try:
            self.__find_element_and_click(self.selectors["suggestedCollapseBtn"], "xpath")
            self.__random_sleep__()

            while self.__wait_for_element__(self.selectors["nextBtn"], "xpath", 5):
                self.__find_element_and_click(self.selectors["nextBtn"], "xpath")

                recUsersTitleList = self.driver.find_elements_by_xpath(self.selectors["recUsersTitle"])

                for i in recUsersTitleList:
                    self.userDataMap[i.text] = 1

                self.__random_sleep__()

            print("get recommend info finish|username: " + username)

            self.driver.close()
            self.driver.switch_to.window(handles[0])
        except Exception as e:
            print("get userinfo err|account is private|username: " + username + "|err info:" + str(e))
            return

    def getUserDetail(self):

        for i in self.userDataMap:
            print("get user detail info|username: " + i)
            userLink = f'https://www.instagram.com/{i}'
            # open new tab for fetch info
            newWindow = f'window.open("{userLink}")'
            self.driver.execute_script(newWindow)
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[len(handles) - 1])
            self.__random_sleep__()
            try:
                country = ""
                pic = ""
                fans = self.driver.find_element_by_xpath(
                    self.selectors['fans_num']).get_attribute("title")

                desc = self.driver.find_element_by_xpath(
                    self.selectors['desc']).get_attribute("textContent")

                self.__find_element_and_click(self.selectors["countryInfoBtn"], "xpath")
                self.__random_sleep__()
                self.__find_element_and_click(self.selectors["accountInfoBtn"], "xpath")

                self.resultData.append([i, fans, desc, country, pic])

                self.driver.close()
                self.driver.switch_to.window(handles[0])

            except Exception as e:
                print("get userinfo err|account is private|username: " + i + "|err info:" + str(e))
                return
