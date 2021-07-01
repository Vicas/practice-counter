import configparser
import os

from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
CONFIG_PATH = DIR_PATH / 'config.ini'

def create_default_counter_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'counter_name': 'Practice Counter',
        'buttons': 'BUTTON1, BUTTON2',}
    config['BUTTON1'] = {
        'label': 'Success!',
        'hotkey': 1,
        'success': True,
        'color': '#03c2fc'}
    config['BUTTON2'] = {
        'label': 'Failure!',
        'hotkey': 2,
        'success': False,
        'color': '#ff525a'}

    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

    return config

# If there is a config file, load it. If a config file doesn't exist, write one
def get_config_file_or_default():
    if CONFIG_PATH.exists():
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config
    return create_default_counter_config()
