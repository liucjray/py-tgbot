import os
from configparser import ConfigParser


def get_config():
    cfg = ConfigParser()
    cfg_path = (os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
    cfg.read(cfg_path)
    return cfg
