""" author: feezyhendrix

    main function botcore
 """

from time import sleep
from random import randint

from modules.config import Config
# importing generated info
# import modules.generateaccountinformation as generate_fake_id
from modules.identity.generator import generate_fake_id

from modules.storeusername import store
# from .activate_account import get_activation_url
# library import
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import re
import logging
# from fake_useragent import UserAgent

# from pymailutils import Imap

DEFAULT_AMOUNT_ACCOUNT = 5

class AccountCreator():

    def __init__(self):
        self.account_created = 0
        self.sockets = []
        self.url = 'https://www.instagram.com/accounts/emailsignup/'

        self.use_custom_proxy = Config["use_custom_proxy"]
        self.use_local_ip_address = Config["use_local_ip_address"]
        self.proxies_path = Config["proxy_file_path"] if self.use_custom_proxy else Config["proxy_url_path"]
        self.amount_of_account = range(0, Config["amount_of_account"] or DEFAULT_AMOUNT_ACCOUNT)

        self.__collect_sockets()


    def __collect_sockets(self):
        if self.use_custom_proxy:
            with open(self.proxies_path, 'r') as proxies_file:
                content = proxies_file.read()
                for socket_str in content.splitlines():
                    self.sockets.append(socket_str)
                proxies_file.close()
        else:
            content = requests.get(self.proxies_path)
            matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", content.text)
            revised_list = [m1.replace("<td>", "") for m1 in matches]
            for socket_str in revised_list:
                self.sockets.append(socket_str[:-5].replace("</td>", ":"))
            #TODO: Criar método para obter a lista de proxy utilizando a API de servicos.


    def __prepare_driver(self, options):
        pass

    def createaccount(self, proxy=None):
        chrome_options = webdriver.ChromeOptions()

        if proxy != None:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        # chrome_options.add_argument('headless')
        # ua = UserAgent()
        # user_agent = ua.random
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36"')
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument('window-size=640x480')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=Config['chromedriver_path'])
        print('Opening Browser')
        driver.get(self.url)

        print('Browser Opened')
        sleep(5)

        action_chains = ActionChains(driver)
        sleep(5)

        account_info = generate_fake_id(Config['name_set'],Config['country'],Config['gender'],("19","49")) # generate_fake_id.new_account()
        print(account_info['online_info']['email_address'])

        # fill the email value
        print('Filling email field')
        email_field = driver.find_element_by_name('emailOrPhone')
        action_chains.move_to_element(email_field)
        email_field.send_keys(str(account_info['online_info']['email_address']))
        sleep(2)

        # fill the fullname value
        print('Filling fullname field')
        fullname_field = driver.find_element_by_name("fullName")
        action_chains.move_to_element(fullname_field)
        fullname_field.send_keys(account_info['personal_info']['full_name'])
        sleep(2)

        # fill username value
        print('Filling username field')
        username_field = driver.find_element_by_name('username')
        action_chains.move_to_element(username_field)
        username_field.send_keys(account_info['online_info']['username'])
        sleep(2)

        # fill password value
        print('Filling password field')
        password_field = driver.find_element_by_name('password')
        action_chains.move_to_element(password_field)
        password_field.send_keys(account_info['online_info']["password"][::-1])
        sleep(2)

        sleep(2)
        submit = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[7]/div/button')
        action_chains.move_to_element(submit)

        sleep(2)
        submit.click()

        sleep(3)
        try:

            month_button = driver.find_element_by_xpath( '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select')
            month_button.click()
            month_button.send_keys(account_info["birthday"].split(" ")[0])
            sleep(1)
            day_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select')
            day_button.click()
            day_button.send_keys(account_info["birthday"].split[" "][1][:-1])
            sleep(1)
            year_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select')
            year_button.click()
            year_button.send_keys(account_info["birthday"].split[" "][2])

            sleep(2)
            next_button = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/div[6]/button')
            next_button.click()

        except Exception as e :
            pass


        sleep(4)
        # After the first fill save the account account_info
        store(account_info)

        """
            Currently buggy code.
        """
        # Activate the account
        # confirm_url = get_activation_url(account_info['email'])
        # logging.info("The confirm url is {}".format(confirm_url))
        # driver.get(confirm_url)

        driver.close()

    def creation_config(self):
        try:
            if self.use_local_ip_address == False:
                if self.use_custom_proxy == False:
                    for i in self.amount_of_account:
                        if len(self.sockets) > 0:
                            current_socket = self.sockets.pop(0)
                            try:
                                self.createaccount(current_socket)
                            except Exception as e:
                                print('Error!, Trying another Proxy {}'.format(current_socket))
                                self.createaccount(current_socket)

                else:
                    with open(Config['proxy_file_path'], 'r') as file:
                        content = file.read().splitlines()
                        for proxy in content:
                            amount_per_proxy = Config['amount_per_proxy']

                            if amount_per_proxy != 0:
                                print(f"Creating {amount_per_proxy} amount of users for this proxy")
                                for i in range(0, amount_per_proxy):
                                    try:
                                        self.createaccount(proxy)

                                    except Exception as e:
                                        print(f"An error has occurred: {e}")

                            else:
                                random_number = randint(1, 20)
                                print(f"Creating {random_number} amount of users for this proxy")
                                for i in range(0, random_number):
                                    try:
                                        self.createaccount(proxy)
                                    except Exception as e:
                                        print(e)
            else:
                for i in self.amount_of_account:
                    try:
                        self.createaccount()
                    except Exception as e:
                        print('Error!, Check its possible your ip might be banned')
                        self.createaccount()


        except Exception as e:
            print(e)


def runbot():
    account = AccountCreator()
    account.creation_config()
