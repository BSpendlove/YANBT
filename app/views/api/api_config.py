from flask import Blueprint, request
from app.utilities import generic_responses, helpers
from app.models import ApiConfig
from app import db

bp = Blueprint("api_config", __name__, url_prefix="/api/v1/config")

@bp.route("/", methods=["GET"])
def api_config():
    app_api_config = ApiConfig.query.get(1)
    if not app_api_config:
        return generic_responses.message_response("No API Config found.")

    return generic_responses.data_response(app_api_config.as_dict())

@bp.route("/", methods=["PATCH"])
def api_config_save():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    app_api_config = ApiConfig.query.get(1)

    if not app_api_config:
        config_obj = ApiConfig(**post_data)
        db.session.add(config_obj)
        db.session.commit()
        return generic_responses.data_response(config_obj.as_dict())

    try:
        for key,value in post_data.items():
            setattr(app_api_config, key, value)
    except Exception as error:
        return generic_responses.error_response(error)

    db.session.commit()
    return generic_responses.data_response(app_api_config.as_dict())
    