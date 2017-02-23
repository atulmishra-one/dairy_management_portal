from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_assets import Environment
from flask_assets import Bundle

from app.config import task


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
assets = Environment()

# Celery
task_server = Celery(__name__, broker=task.CELERY_BROKER_URL)
task_server.config_from_object(task)


# Assets
assets.register(
    'js_all',
    Bundle(
        'js/jquery-3.1.1.min.js',
        'js/bootstrap.min.js',
        filters='jsmin',
        output='packed.js'
    )
)

assets.register(
    'css_all',
    Bundle(
        'css/bootstrap.min.css',
        'css/style.css'
    )
)