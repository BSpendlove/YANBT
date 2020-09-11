import os
import json

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