from flask import Blueprint, request
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
    tree = helpers.dir_to_list("backups")
    if not tree:
        return generic_responses.message_response("No entries in tree")

    return generic_responses.data_response(tree)

@bp.route("/get_config_file", methods=["POST"])
def get_config_file():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()

    if not "path" in post_data:
        return generic_responses.missing_field_response("path")

    app_api_config = ApiConfig.query.get(1)
    if not app_api_config:
        return generic_responses.message_response("No API Config found.")

    if not app_api_config.backup_directory:
        return generic_responses.message_response("No backup_directory set within ApiConfig.")

    path = post_data["path"]
    child_path = "/".join(path.split(";"))
    full_path = "{}{}".format(app_api_config.backup_directory, child_path)

    with open(full_path, "r") as config_file:
        config = config_file.read()

    return generic_responses.data_response(config)
