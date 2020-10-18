import os
import json
from app import Config
from app.models import ApiConfig, Group
import pathlib

def dir_to_list(dirname, path=os.path.pathsep):
    data = []
    for name in os.listdir(dirname):
        dct = {}
        dct['text'] = name
        dct['path'] = path + name

        full_path = os.path.join(dirname, name)
        if os.path.isfile(full_path):
            dct['type'] = 'file'
            dct['icon'] = 'fa fa-file-text-o'
        elif os.path.isdir(full_path):
            dct['type'] = 'folder'
            dct['nodes'] = dir_to_list(full_path, path=path + name + os.path.pathsep)
            dct['icon'] = 'fa fa-folder'
        data.append(dct)
    return data

def dir_to_list_no_files(dirname, path=os.path.pathsep):
    data = []
    for name in os.listdir(dirname):
        dct = {}
        dct['text'] = name
        dct['path'] = path.lower() + name.lower()

        full_path = os.path.join(dirname, name)
        if os.path.isfile(full_path):
            dct['type'] = 'file'
            dct['icon'] = 'fa fa-file-text-o'
        elif os.path.isdir(full_path):
            dct['type'] = 'folder'
            dct['nodes'] = [_node for _node in dir_to_list_no_files(full_path, path=path + name + os.path.pathsep) if _node["type"] == "folder"]
            dct['icon'] = 'fa fa-folder'
        data.append(dct)
    return data

def sync_database_folder_structure():
    base_directory = Config().load_local_config()["backup_directory"]
    groups = Group.query.all()

    for group in groups:
        folder_dir = "{}{}".format(base_directory, group.folder_path.replace(";", "/"))
        if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)

def delete_folder(folder_path):
    base_directory = Config().load_local_config()["backup_directory"]
    folder_dir = "{}{}".format(base_directory, folder_path.replace(";", "/"))
    path = pathlib.Path(folder_dir)
    path.rmdir()