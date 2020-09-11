from flask import Blueprint, render_template, request

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/", methods=["GET"])
def index():
    return render_template("users/index.html")