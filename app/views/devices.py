from flask import Blueprint, render_template

bp = Blueprint("devices", __name__, url_prefix="/devices")

@bp.route("/", methods=["GET"])
def index():
    return render_template("devices/index.html")
