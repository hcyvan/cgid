import os
from enum import Enum

const = {
    'SRID': '4326'
}

ENV = Enum('Env', ('development', 'production', 'test'))
APP_TYPE = Enum('AppType', ('web_api', 'worker', 'channel'))


class BaseConfig:
    VERSION = '0.1'
    DEBUG = False
    SECRET_KEY = 'LifeIsBoring'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
    ENV = ENV.production


class DevConfig(BaseConfig):
    DEBUG = True
    ENV = ENV.development


class TestConfig(BaseConfig):
    DEBUG = True
    ENV = ENV.test


def get_config():
    config_map = dict(
        development=DevConfig,
        test=TestConfig,
        production=ProdConfig
    )
    return config_map[os.getenv('FLASK_ENV', 'development')]


def get_root():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_env():
    env = os.path.join(get_root(), 'env.py')
    if not os.path.exists(env):
        raise Exception('No env.py in the project')
    return env
