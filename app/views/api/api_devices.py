from flask import Blueprint, request
from app.models import Device
from app.utilities import generic_responses, validators
from app import db

bp = Blueprint("api_devices", __name__, url_prefix="/api/v1/devices")

@bp.route("/", methods=["GET"])
def get_devices():
    devices = Device.query.all()
    return generic_responses.data_response([_device.as_dict() for _device in devices])

@bp.route("/", methods=["POST"])
def create_device():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["friendly_name", "ip", "netmiko_driver", "authentication_user"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)
    print(post_data)
    try:
        device = Device(**post_data)
    except Exception as error:
        return generic_responses.error_response(error)

    db.session.add(device)
    db.session.commit()
    return device.as_dict()

@bp.route("/<int:id>", methods=["GET"])
def get_device(id):
    device = Device.query.get(id)
    if not device:
        return generic_responses.message_response("Device {} does not exist.".format(id))

    return generic_responses.data_response([device.as_dict()])

@bp.route("/<int:id>", methods=["DELETE"])
def delete_device(id):
    device = Device.query.get(id)
    if not device:
        return generic_responses.message_response("Device {} does not exist.".format(id))

    db.session.delete(device)
    db.session.commit()
    return generic_responses.data_response([device.as_dict()])

@bp.route("/<int:id>", methods=["PATCH"])
def update_device(id):
    if not request.is_json:
        return generic_responses.BAD_JSON

    post_data = request.get_json()
    device = Device.query.get(id)
    try:
        for key,value in post_data.items():
            setattr(device, key, value)
    except Exception as error:
        return generic_responses.error_response(error)

    db.session.commit()
    return generic_responses.data_response([device.as_dict()])
