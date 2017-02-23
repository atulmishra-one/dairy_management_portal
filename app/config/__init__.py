from .local import LocalConfig
from .production import ProductionConfig

app_config = {
    'development': LocalConfig,
    'production': ProductionConfig
}