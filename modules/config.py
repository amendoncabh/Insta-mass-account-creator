"""
    author: feezyhendrix
    contrib: amendoncabh

    Configuration files

    NOTE: check Assets/proxies.txt to use your custom proxies.
 """
import os
import logging

from configparser import ConfigParser
from typing import Any

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, 'Assets' )

class Settings:
    """
    Configuration settings class from .ini file controler

    Returns:
        class: Configuration data
    """

    __CONFIG_FILENAME = os.path.join(BASE_DIR, 'ig-macs.ini')
    __DEFAULT_VALUES = {
        "settings": {
            "bot_type": 3, # Change to 2 to use python requests or 3 for scheduled job with selenium requests.
            "bot_timing_schedule": 5, # Timing interval to run a bot job task.
            "use_custom_proxy": False, # Default is False change to True to use a file containing multiple proxies of yours.
            "use_local_ip_address": False, # Default is False change to True to user your computers ip directly.
            "use_fake_email": True, # Set to use the fake mail service, default is True.
            "amount_of_account": 20, # Amount of account you want to create make sure it doesn't exceed 50 for better performance.
            "amount_per_proxy": 2, # This would be amount of account used if you have a you are using multiple proxies.
            "retry_times": 10, # Many times will try reload the account page for a proxy address.
            "proxy_file_path": os.path.join(ASSET_DIR, 'proxies.txt'), # Custom list of proxies defined file.
            "proxy_url_path": 'https://www.sslproxies.org/',
            "chromedriver_path": 'C://Program Files//Google//Chrome//Application//chromedriver.exe',  # chromedriver application path.
            "gender": 'random',
            "country": 'pt_br',
            "email_password": 'xxxxxxxxxxxxxxxx',
            "email_port": 993,
            "email_server": 'imap.gmail.com',
            "email_user": 'xxxxxxxxxxxxxxxx',
        }
    }

    def __init__(self) -> None:
        self.config = ConfigParser()

    def __getattribute__(self, __name: str) -> Any:
        return self.config["settings"][__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.config["settings"][__name] = __value

    def load(self) -> None:
        if os.path.isfile(self.__CONFIG_FILENAME):
            self.config.read(self.__CONFIG_FILENAME)
        else:
            self.config.read_dict(self.__DEFAULT_VALUES)
            self.save()

    def save(self) -> None:
        with open(self.__CONFIG_FILENAME, 'w') as config_file:
            self.config.write(config_file)
            config_file.close

Config = Settings()
