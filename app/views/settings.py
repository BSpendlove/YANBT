from flask import Blueprint, render_template

bp = Blueprint("settings", __name__, url_prefix="/settings")

@bp.route("/", methods=["GET"])
def index():
    return render_template("settings/index.html")
