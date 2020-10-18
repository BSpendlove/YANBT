from app import db
from datetime import datetime

class ApiConfig(db.Model):
    __tablename__ = "apiconfig"

    id = db.Column(db.Integer, primary_key=True)
    backup_directory = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return "<YANBT ApiConfig {}>".format(self.id)

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
        return "<YANBT User {}>".format(self.username)

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
    ip = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer)
    netmiko_driver = db.Column(db.String, nullable=False)
    authentication_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    config_command = db.Column(db.String)
    pre_commands = db.Column(db.String)
    assigned_group = db.Column(db.Integer, db.ForeignKey("group.id"))
    description = db.Column(db.String)
    notes = db.Column(db.String)

    def __repr__(self):
        return "<YANBT Device {}>".format(self.id)

    def as_dict(self):
        return {
            "id": self.id,
            "friendly_name": self.friendly_name,
            "ip": self.ip,
            "port": self.port,
            "netmiko_driver": self.netmiko_driver,
            "authentication_user": self.authentication_user,
            "config_command": self.config_command,
            "pre_commands": self.pre_commands,
            "assigned_group": Group.query.get(self.assigned_group).folder_path if self.assigned_group else None,
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
    name = db.Column(db.String, nullable=False)
    folder_path = db.Column(db.String, nullable=False, unique=True)
    is_root = db.Column(db.Boolean)
    is_child = db.Column(db.Boolean)
    child_root = db.Column(db.Integer)
    description = db.Column(db.String)
    devices = db.relationship("Device", backref="device", lazy='dynamic')
    backup_job = db.relationship("BackupJob", backref="backupjob", lazy='dynamic')

    def __repr__(self):
        return "<YANBT Group {}>".format(self.name)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "folder_path": self.folder_path,
            "description": self.description,
            "devices": [_device.as_dict_basic() for _device in self.devices] if self.devices else []
        }

class BackupJob(db.Model):
    __tablename__ = "backupjob"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    assigned_group = db.Column(db.Integer, db.ForeignKey("group.id"))
    active = db.Column(db.Boolean)
    start_date_time = db.Column(db.String)
    end_date_time = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    job_occur = db.Column(db.String)
    job_start_time = db.Column(db.String)

    def __repr__(self):
        return "<YANBT BackupJob {}>".format(self.id)

    def as_dict():
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "assigned_group": Group.query.get(self.assigned_group).folder_path if self.assigned_group else None,
            "active": self.active,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
            "created_at": self.created_at,
            "job_occur": self.job_occur,
            "job_start_time": self.job_start_time
        }

    
