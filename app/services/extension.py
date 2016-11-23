import flask_login
from flask_mail import Mail
from flask import current_app
from flask_migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from celery import task as ctask

from app.config import task


login_manager = flask_login.LoginManager()
sqlalchemy = SQLAlchemy()
migrate = Migrate()
mail = Mail()


task_server = Celery(__name__, broker=task.CELERY_BROKER_URL)
task_server.config_from_object(task)