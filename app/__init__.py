from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.views import (
    backup_jobs,
    dashboard,
    devices,
    settings,
    users
)

from app.views.api import (
    api_users,
    api_devices,
    api_tools,
    api_config
)

from app import models

db.create_all()

app.register_blueprint(backup_jobs.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(settings.bp)
app.register_blueprint(users.bp)
app.register_blueprint(api_users.bp)
app.register_blueprint(api_devices.bp)
app.register_blueprint(api_tools.bp)
app.register_blueprint(api_config.bp)