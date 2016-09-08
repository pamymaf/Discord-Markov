import configparser
import os

class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        if not config.read('config/config.ini', encoding='utf-8'):
            print("Config file not found")
            os._exit(1)  # Exit the script

        config = configparser.ConfigParser(interpolation=None)
        config.read('config/config.ini', encoding='utf-8')

        self.prefix = config.get('General', 'Prefix')
        self.token = config.get('General', 'Token')