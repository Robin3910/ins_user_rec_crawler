from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from random import randint, uniform
from time import time, sleep, localtime
import logging
import sqlite3

DEFAULT_IMPLICIT_WAIT = 1


class InstaDM(object):

    def __init__(self, username, password, headless=True, instapy_workspace=None, profileDir=None):
        self.selectors = {
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

        # mobile_emulation = {
        #     "userAgent": 'Mozilla/5.0 (Linux; Android 10.0; iPhone Xs Max Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/535.19'
        # }
        # options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(
            executable_path=CM().install(), options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(2000, 936)

        # Instapy init DB
        self.instapy_workspace = instapy_workspace
        self.conn = None
        self.cursor = None
        if self.instapy_workspace is not None:
            self.conn = sqlite3.connect(
                self.instapy_workspace + "InstaPy/db/instapy.db")
            self.cursor = self.conn.cursor()

            cursor = self.conn.execute("""
                SELECT count(*)
                FROM sqlite_master
                WHERE type='table'
                AND name='message';
            """)
            count = cursor.fetchone()[0]

            if count == 0:
                self.conn.execute("""
                    CREATE TABLE "message" (
                        "username"    TEXT NOT NULL UNIQUE,
                        "message"    TEXT DEFAULT NULL,
                        "sent_message_at"    TIMESTAMP
                    );
                """)

        try:
            self.driver.get('https://instagram.com/?hl=en')

            # 代码修改处
            cookies = self.extract_cookies(
                cookie="mid=YdkfTgALAAEkbmcPqBufmiKyV3D5; ig_did=734B6C43-E743-461E-AEEF-6A635AD5BAAB; ig_nrcb=1; datr=uDgKY0maEvUCH6O4VjE1-JLp; csrftoken=AChKcT1cFCePhygWaZKlIG10FOfRFd8A; ds_user_id=50932469833; shbid=5886\05450932469833\0541695640111:01f7f0b84f4be8d39b54c3b48f855b552fcfb1a01e7c5fc4f5fbb49973aee454aa69c42a; shbts=1664104111\05450932469833\0541695640111:01f79238102d2d42b24ad4408478876b24154b4988c111dabe8748ceb6bfdc9d63e47bc7; sessionid=50932469833%3AQWOHIbc9E2oCz5%3A6%3AAYcWck8gvNNdWFPkcnG5eQkkTnxxy0D4b98JykF5mg; dpr=1.25; ig_lang=en; rur=NAO\05450932469833\0541695742589:01f72e8b338134d3aed5116c2dd676e012d137b8e71df887f9d20e9ea1684f7b51bdf8a7; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%221837a74b0975cd-0a23d81b26b53f-26021c51-240000-1837a74b0987e8%22%2C%22%24device_id%22%3A%20%221837a74b0975cd-0a23d81b26b53f-26021c51-240000-1837a74b0987e8%22%2C%22site_type%22%3A%20%22similarweb%20extension%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.instagram.com%2Faccounts%2Fedit%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.instagram.com%22%7D")
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

            self.searchUser("kingjames")

        except Exception as e:
            logging.error(e)
            print(str(e))

    def login(self, username, password):
        # homepage
        self.driver.get('https://instagram.com/?hl=en')
        self.__random_sleep__(3, 5)
        if self.__wait_for_element__(self.selectors['accept_cookies'], 'xpath', 10):
            self.__get_element__(
                self.selectors['accept_cookies'], 'xpath').click()
            self.__random_sleep__(3, 5)
        if self.__wait_for_element__(self.selectors['home_to_login_button'], 'xpath', 10):
            self.__get_element__(
                self.selectors['home_to_login_button'], 'xpath').click()
            self.__random_sleep__(5, 7)

        # login
        logging.info(f'Login with {username}')
        self.__scrolldown__()
        if not self.__wait_for_element__(self.selectors['username_field'], 'name', 10):
            print('Login Failed: username field not visible')
        else:
            self.driver.find_element_by_name(
                self.selectors['username_field']).send_keys(username)
            self.driver.find_element_by_name(
                self.selectors['password_field']).send_keys(password)
            self.__get_element__(
                self.selectors['button_login'], 'xpath').click()
            self.__random_sleep__()
            if self.__wait_for_element__(self.selectors['login_check'], 'xpath', 10):
                print('Login Successful')
            else:
                print('Login Failed: Incorrect credentials')

    def createCustomGreeting(self, greeting):
        # Get username and add custom greeting
        if self.__wait_for_element__(self.selectors['name'], "xpath", 10):
            user_name = self.__get_element__(
                self.selectors['name'], "xpath").text
            if user_name:
                greeting = greeting + " " + user_name + ", \n\n"
        else:
            greeting = greeting + ", \n\n"
        return greeting

    def typeMessage(self, user, message):
        # Go to page and type message
        if self.__wait_for_element__(self.selectors['next_button'], "xpath"):
            self.__get_element__(
                self.selectors['next_button'], "xpath").click()
            self.__random_sleep__()

        for msg in message:
            if self.__wait_for_element__(self.selectors['textarea'], "xpath"):
                self.__type_slow__(self.selectors['textarea'], "xpath", msg)
                self.__random_sleep__()

            if self.__wait_for_element__(self.selectors['send'], "xpath"):
                self.__get_element__(self.selectors['send'], "xpath").click()
                self.__random_sleep__(3, 5)
                print('Message sent successfully')

    def sendMessage(self, user, message, greeting=None):
        logging.info(f'Send message to {user}')
        print(f'Send message to {user}')
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self.__random_sleep__(2, 4)

        try:
            self.__wait_for_element__(self.selectors['search_user'], "name")
            self.__type_slow__(self.selectors['search_user'], "name", user)
            self.__random_sleep__(1, 2)

            if greeting != None:
                greeting = self.createCustomGreeting(greeting)

            # Select user from list
            elements = self.driver.find_elements_by_xpath(
                self.selectors['select_user'].format(user))
            if elements and len(elements) > 0:
                elements[0].click()
                self.__random_sleep__()

                if greeting != None:
                    self.typeMessage(user, message)
                else:
                    self.typeMessage(user, message)

                if self.conn is not None:
                    self.cursor.execute(
                        'INSERT INTO message (username, message) VALUES(?, ?)', (user, message[0]))
                    self.conn.commit()
                self.__random_sleep__(5, 10)

                return True

            # In case user has changed his username or has a private account
            else:
                print(f'User {user} not found! Skipping.')
                return False

        except Exception as e:
            logging.error(e)
            return False

    def sendGroupMessage(self, users, message):
        logging.info(f'Send group message to {users}')
        print(f'Send group message to {users}')
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self.__random_sleep__(5, 7)

        try:
            usersAndMessages = []
            for user in users:
                if self.conn is not None:
                    usersAndMessages.append((user, message))

                self.__wait_for_element__(
                    self.selectors['search_user'], "name")
                self.__type_slow__(self.selectors['search_user'], "name", user)
                self.__random_sleep__()

                # Select user from list
                elements = self.driver.find_elements_by_xpath(
                    self.selectors['select_user'].format(user))
                if elements and len(elements) > 0:
                    elements[0].click()
                    self.__random_sleep__()
                else:
                    print(f'User {user} not found! Skipping.')

            self.typeMessage(user, message)

            if self.conn is not None:
                self.cursor.executemany("""
                    INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
                """, usersAndMessages)
                self.conn.commit()
            self.__random_sleep__(50, 60)

            return True

        except Exception as e:
            logging.error(e)
            return False

    def sendGroupIDMessage(self, chatID, message):
        logging.info(f'Send group message to {chatID}')
        print(f'Send group message to {chatID}')
        self.driver.get('https://www.instagram.com/direct/inbox/')
        self.__random_sleep__(5, 7)

        # Definitely a better way to do this:
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 2 + Keys.ENTER).perform()
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER).perform()

        if self.__wait_for_element__(f"//a[@href='/direct/t/{chatID}']", 'xpath', 10):
            self.__get_element__(
                f"//a[@href='/direct/t/{chatID}']", 'xpath').click()
            self.__random_sleep__(3, 5)

        try:
            usersAndMessages = [chatID]

            if self.__wait_for_element__(self.selectors['textarea'], "xpath"):
                self.__type_slow__(
                    self.selectors['textarea'], "xpath", message)
                self.__random_sleep__()

            if self.__wait_for_element__(self.selectors['send'], "xpath"):
                self.__get_element__(self.selectors['send'], "xpath").click()
                self.__random_sleep__(3, 5)
                print('Message sent successfully')

            if self.conn is not None:
                self.cursor.executemany("""
                    INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
                """, usersAndMessages)
                self.conn.commit()
            self.__random_sleep__(50, 60)

            return True

        except Exception as e:
            logging.error(e)
            return False

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
        self.__random_sleep__()
        self.__find_element_and_click(self.selectors["search_input_button"], "xpath")
        self.__random_sleep__()

        self.driver.find_element_by_xpath(
            self.selectors['search_input_area']).send_keys(username)
        self.__random_sleep__(10, 10)

        self.driver.find_element_by_xpath(
            self.selectors['search_input_area']).send_keys(Keys.ENTER)

        self.__random_sleep__()

        self.driver.find_element_by_xpath(
            self.selectors['search_input_area']).send_keys(Keys.ENTER)

