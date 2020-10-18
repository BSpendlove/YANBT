from flask import Blueprint, request
from app.utilities import generic_responses, helpers, validators
from app import Config
from app import db

bp = Blueprint("api_config", __name__, url_prefix="/api/v1/config")

@bp.route("/", methods=["GET"])
def api_config():
    app_config = Config().load_local_config()
    return generic_responses.data_response(app_config)

@bp.route("/", methods=["PATCH"])
def api_config_save():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["backup_directory"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)

    app_settings = Config()
    app_settings.load_local_config() # Load current config which will store as DEFAULT_APP_CONFIG which we can then access, set and then call write_config() which will use DEFAULT_APP_CONFIG
    for k,v in post_data.items():
        if k in app_settings.DEFAULT_APP_CONFIG.keys():
            app_settings.DEFAULT_APP_CONFIG[k] = v

    return generic_responses.data_response(app_settings.write_config())