from flask import Blueprint, request
from app import app
from app.models import Group
from app.utilities import generic_responses, helpers, validators
from app import db

bp = Blueprint("api_groups", __name__, url_prefix="/api/v1/groups")

@bp.route("/", methods=["GET"])
def get_groups():
    groups = Group.query.all()
    return generic_responses.data_response([_group.as_dict() for _group in groups])

@bp.route("/<int:id>", methods=["GET"])
def get_group(id):
    group = Group.query.get(id)
    if not group:
        return generic_responses.error_response("group {} does not exist.".format(id))

    return group.as_dict()

@bp.route("/", methods=["POST"])
def create_group():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["name", "folder_path"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)

    group = Group(**post_data)
    db.session.add(group)
    db.session.commit()
    helpers.sync_database_folder_structure()
    return group.as_dict()

@bp.route("/", methods=["DELETE"])
def delete_group():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["folder_path"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)

    group = Group.query.filter_by(folder_path=post_data["folder_path"]).first()
    if not group:
        return generic_responses.message_response("Group with path {} not found.".format(post_data["folder_path"]))
    db.session.delete(group)
    db.session.commit()
    helpers.delete_folder(group.folder_path)
    return generic_responses.data_response([group.as_dict()])

@bp.route("/get_members", methods=["POST"])
def get_group_members():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["folder_path"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)

    group = Group.query.filter_by(folder_path=post_data["folder_path"]).first()
    if not group:
        return generic_responses.message_response("Group with path {} not found.".format(post_data["folder_path"]))

    return generic_responses.data_response([group.as_dict()])