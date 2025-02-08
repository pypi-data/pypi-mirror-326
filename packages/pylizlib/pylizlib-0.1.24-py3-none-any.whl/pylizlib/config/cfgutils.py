import configparser
import os
from typing import List


class CfgItem:
    def __init__(self, section: str, key: str, value: str | bool):
        self.section = section
        self.key = key
        self.value = value


class Cfgini:
    def __init__(self, path_to_ini):
        self.config = None
        self.path = path_to_ini

    def exists(self):
        return os.path.exists(self.path)

    def create(self, items: List[CfgItem] | None = None):
        self.config = configparser.ConfigParser()
        list_of_sections = set()

        for item in items:
            list_of_sections.add(item.section)

        for section in list_of_sections:
            self.config.add_section(section)

        for item in items:
            self.config.set(item.section, item.key, item.value)

        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)
            # print("Configuration file created in: ", self.path)
        except Exception as e:
            print("Error while creating configuration file: ", e)

    def read(self, section, key, is_bool=False):
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        if not self.config.has_section(section):
            print(f"Attenzione: La sezione '{section}' non esiste nel file INI.")
            return None
        if not self.config.has_option(section, key):
            print(f"Attenzione: La chiave '{key}' non esiste nella sezione '{section}'.")
            return None
        try:
            if is_bool:
                return self.config.getboolean(section, key)
            return self.config.get(section, key)
        except configparser.Error as e:
            print(f"Errore durante la lettura di '{key}' in '{section}': {e}")
            return None

    def write(self, section, key, value: str | bool):
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        if not self.config.has_section(section):
            self.config.add_section(section)
        if isinstance(value, bool):
            self.config.set(section, key, str(value))
        else:
            self.config.set(section, key, value)
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)



