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
    users,
    groups
)

from app.views.api import (
    api_users,
    api_devices,
    api_tools,
    api_config,
    api_groups,
    api_backupjob
)

from app import models

db.create_all()

# Preload additional app config (from database) - Need to find a better way of doing this...
with app.app_context():
    try:
        Config.load_local_config()
    except:
        print("Error trying to load local config...")

app.register_blueprint(backup_jobs.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(settings.bp)
app.register_blueprint(users.bp)
app.register_blueprint(groups.bp)
app.register_blueprint(api_users.bp)
app.register_blueprint(api_devices.bp)
app.register_blueprint(api_tools.bp)
app.register_blueprint(api_config.bp)
app.register_blueprint(api_groups.bp)
app.register_blueprint(api_backupjob.bp)