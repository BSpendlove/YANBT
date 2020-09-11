from app import db

class ApiConfig(db.Model):
    __tablename__ = "apiconfig"

    id = db.Column(db.Integer, primary_key=True)
    backup_directory = db.Column(db.String(), unique=True)

    def as_dict(self):
        return {
            "backup_directory": self.backup_directory
        }

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    devices = db.relationship("Device", backref="user", lazy='dynamic')

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)

    def as_dict(self, show_password=True):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password if show_password else "--hidden--",
            "devices": [_device.id for _device in self.devices]
        }

class Device(db.Model):
    __tablename__ = "device"

    id = db.Column(db.Integer, primary_key=True)
    friendly_name = db.Column(db.String)
    ip = db.Column(db.String)
    port = db.Column(db.Integer)
    netmiko_driver = db.Column(db.String)
    authentication_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    config_command = db.Column(db.String)
    pre_commands = db.Column(db.String)
    assigned_group = db.relationship("Group", backref="group", lazy='dynamic')
    description = db.Column(db.String)
    notes = db.Column(db.String)

    def __repr__(self):
        return "<Device {}>".format(self.id)

    def as_dict(self):
        print(self.authentication_user)
        return {
            "id": self.id,
            "friendly_name": self.friendly_name,
            "ip": self.ip,
            "port": self.port,
            "netmiko_driver": self.netmiko_driver,
            "authentication_user": self.authentication_user,
            "config_command": self.config_command,
            "pre_commands": self.pre_commands,
            "description": self.description,
            "notes": self.notes
        }

    def as_dict_basic(self):
        return {
            "id": self.id,
            "friendly_name": self.friendly_name,
            "ip": self.ip,
            "port": self.port
        }

class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    devices = db.Column(db.Integer, db.ForeignKey("device.id"))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group {}>".format(self.name)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "devices": [_device.as_dict_basic for _device in self.devices]
        }
