"""
Local and Testing configuration
"""

from .base import BaseConfig


class LocalConfig(BaseConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'dairy_manager'