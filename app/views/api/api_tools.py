from flask import Blueprint, request
from app import Config
from app.utilities import generic_responses, helpers
from app.utilities.netmiko_functions import get_netmiko_drivers
from app.models import ApiConfig
import os

bp = Blueprint("api_tools", __name__, url_prefix="/api/v1/tools")

@bp.route("/netmiko_drivers", methods=["GET"])
def netmiko_drivers():
    return get_netmiko_drivers()

@bp.route("/directory_tree", methods=["GET"])
def directory_tree():
    root_path = helpers.dir_to_list(Config().load_local_config()["backup_directory"])

    root_tree = [{
        "icon": "fa fa-folder",
        "nodes": root_path,
        "path": "",
        "text": root_path,
        "type": "folder"
    }]

    return generic_responses.data_response(root_tree)

@bp.route("/database_group_tree", methods=["GET"])
def database_group_tree():
    root_path = helpers.dir_to_list_no_files(Config().load_local_config()["backup_directory"])

    root_tree = [{
        "icon": "fa fa-folder",
        "nodes": root_path,
        "path": "",
        "text": root_path,
        "type": "folder"
    }]

    return generic_responses.data_response(root_tree)

@bp.route("/sync_database", methods=["GET"])
def database_sync():
    helpers.sync_database_folder_structure()

@bp.route("/get_config_file", methods=["POST"])
def get_config_file():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()

    if not "path" in post_data:
        return generic_responses.missing_field_response("path")

    app_api_config = Config().load_local_config()
    if not app_api_config:
        return generic_responses.message_response("No API Config found.")

    if not app_api_config["backup_directory"]:
        return generic_responses.message_response("No backup_directory set within ApiConfig.")

    path = post_data["path"]
    child_path = "/".join(path.split(";"))
    full_path = "{}{}".format(app_api_config["backup_directory"], child_path)

    with open(full_path, "r") as config_file:
        config = config_file.read()

    return generic_responses.data_response(config)
