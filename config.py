import os
import json

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "very-secure-secret-key"

    def __init__(self):
        self.DEFAULT_APP_CONFIG = {
            "version": "0.0.1",
            "repo": "https://github.com/BSpendlove/YANBT",
            "backup_directory": "backups"
        }

    def load_local_config(self):
        if not os.path.exists("app_settings.json"):
            with open("app_settings.json", "w") as appSettings:
                appSettings.write(json.dumps(self.DEFAULT_APP_CONFIG, indent=4))

        try:
            appSettings = json.loads(open("app_settings.json").read())
        except:
            appSettings = None

        if not appSettings:
            return self.write_config()
        return appSettings

    def write_config(self):
        with open("app_settings.json", "w") as appSettings:
            appSettings.write(json.dumps(self.DEFAULT_APP_CONFIG, indent=4))
        return self.load_local_config()