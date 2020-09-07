from flask import Flask

app = Flask(__name__)

from views import (
    backup_jobs,
    dashboard,
    devices,
    settings,
    users
)

if __name__ == "__main__":
    app.register_blueprint(backup_jobs.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(devices.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(users.bp)
    app.run(host="0.0.0.0", port=5006, debug=True)
