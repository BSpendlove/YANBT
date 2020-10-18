from flask import Blueprint, render_template

bp = Blueprint("groups", __name__, url_prefix="/groups")

@bp.route("/", methods=["GET"])
def index():
    return render_template("groups/index.html")
