"""
Production configuration
"""

from .base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/dairy_manager'



