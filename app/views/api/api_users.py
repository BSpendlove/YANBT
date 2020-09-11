from flask import Blueprint, request
from app.models import User
from app.utilities import generic_responses, validators
from app import db

bp = Blueprint("api_users", __name__, url_prefix="/api/v1/users")

@bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return generic_responses.data_response([_user.as_dict() for _user in users])

@bp.route("/", methods=["POST"])
def create_user():
    if not request.is_json:
        return generic_responses.bad_json_response()

    post_data = request.get_json()
    validation, field = validators.valdiate_required_fields(["username", "password"], post_data)
    if not validation:
        return generic_responses.missing_field_response(field)

    try:
        user = User(**post_data)
    except Exception as error:
        return generic_responses.error_response(error)

    db.session.add(user)
    db.session.commit()
    return user.as_dict()

@bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return generic_responses.message_response("User {} does not exist.".format(id))

    return generic_responses.data_response([user.as_dict()])

@bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return generic_responses.message_response("User {} does not exist.".format(id))

    db.session.delete(user)
    db.session.commit()
    return generic_responses.data_response([user.as_dict()])

@bp.route("/<int:id>", methods=["PATCH"])
def update_user(id):
    if not request.is_json:
        return generic_responses.BAD_JSON

    post_data = request.get_json()
    user = User.query.get(id)
    try:
        for key,value in post_data.items():
            setattr(user, key, value)
    except Exception as error:
        return generic_responses.error_response(error)

    db.session.commit()
    return generic_responses.data_response([user.as_dict()])
