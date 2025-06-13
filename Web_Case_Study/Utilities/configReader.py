import os
from configparser import ConfigParser


def readConfig(section, key):
    config = ConfigParser()
    absolute_path = str(os.getcwd())
    config_file_list = [rf"{absolute_path}/Elements/careersPage.ini",
                        rf"{absolute_path}/Elements/entryPage.ini",
                        rf"{absolute_path}/Elements/positionsPage.ini",
                        rf"{absolute_path}/Elements/qaPage.ini",
                        ]

    config.read(config_file_list)

    return config.get(section, key)
